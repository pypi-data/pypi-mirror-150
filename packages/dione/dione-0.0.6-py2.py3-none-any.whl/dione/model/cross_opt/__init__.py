# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides the DIONE Cross Optimization model `dsp`.

Sub-Modules:

.. currentmodule:: dione.model.cross_opt

.. autosummary::
    :nosignatures:
    :toctree: cross_opt/

    problem
"""
import gc
import tqdm
import functools
import numpy as np
import pandas as pd
import schedula as sh
from schedula.utils.asy import await_result
from ...utils import DummyExecutor

# Cross Optimization Model definition.
dsp = sh.BlueDispatcher(name='Cross Optimization Model')


@sh.add_function(dsp, outputs=['fleet_shares'])
def calculate_fleet_shares(
        fleet_registrations, reduction_tech_cost_curves, fleet_co2_references):
    """
    Calculate the fleet shares.

    :param fleet_registrations:
        Fleet vehicle registrations.
    :type fleet_registrations: pandas.Dataframe

    :param reduction_tech_cost_curves:
        Parameters of reduction/Cost curves.
    :type reduction_tech_cost_curves: pandas.Dataframe

    :param fleet_co2_references:
        Fleet CO2 emission at reference year.
    :type fleet_co2_references: pandas.Dataframe

    :return:
        Fleet shares.
    :rtype: pandas.Dataframe
    """
    shares = fleet_registrations.stack()
    index = shares.index.join(fleet_co2_references.index, how='inner')
    index = index.join(reduction_tech_cost_curves.index, how='inner')
    names = shares.index.names
    index = index.droplevel([k for k in index.names if k not in names])
    index = index[~index.duplicated(keep='first')]
    shares = shares.loc[index.reorder_levels(names)]
    shares = shares.unstack(['powertrain', 'segment'])
    shares = shares.div(shares.sum(axis=1), axis=0)
    return shares.unstack('registration_year').stack(['powertrain', 'segment'])


def _interpolate(points, x):
    return np.array([np.interp(v, *p) for p, v in zip(points, x.T)]).T


def _make_cost_func(params):
    if 'points' in params:
        cost = functools.partial(_interpolate, [v.T for v in params['points']])
    else:
        from ..cost_curve import _reduction_tech_cost_function
        cost = functools.partial(_reduction_tech_cost_function, params)
    return cost


def _opt_task(shares, factors, target, params):
    from .problem import Problem
    from pymoo.optimize import minimize
    from pymoo.util.normalization import denormalize
    from pymoo.algorithms.soo.nonconvex.pso import PSO
    gc.collect()
    cost = _make_cost_func(params)
    pop_size, xl, xu = 50, params['x_min'].ravel(), params['x_max'].ravel()
    problem = Problem(
        shares=shares, factors=factors, target=target, cost=cost, xl=xl, xu=xu
    )
    np.random.seed(1)
    x = np.random.random((pop_size, problem.n_var))
    x[0], x[-1] = 0, 1
    x = minimize(problem, algorithm=PSO(
        pop_size=pop_size, sampling=denormalize(x, xl, xu)
    ), seed=1, verbose=False).X
    return np.column_stack((x, cost(x).ravel()))


dsp.add_data('use_curves', False)


@sh.add_function(
    dsp, True, True, outputs=['fleet_reduction_tech_cost'],
    input_domain=lambda b, *args: not b
)
def calculate_fleet_reduction_tech_cost(
        use_curves, fleet_shares, reduction_tech_cost_pareto, optimal_pareto,
        fleet_targets, fleet_co2_references, executor=DummyExecutor()):
    """
    Calculate the optimal fleet reductions and costs.

    :param fleet_shares:
        Fleet shares.
    :type fleet_shares: pandas.Dataframe

    :param reduction_tech_cost_curves:
        Parameters of reduction/Cost curves.
    :type reduction_tech_cost_curves: pandas.Dataframe

    :param fleet_targets:
        Fleet emission targets.
    :type fleet_targets: pandas.Dataframe

    :param fleet_co2_references:
        Fleet CO2 emission at reference year.
    :type fleet_co2_references: pandas.Dataframe

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :return:
        Optimal fleet reductions and costs.
    :rtype: pandas.Dataframe
    """
    keys = ['scenario', 'fleet', 'cost_type', 'registration_year']
    s_keys = ['powertrain', 'segment']
    res, trgs = {}, fleet_targets.T
    f_ref = fleet_co2_references.unstack(s_keys)
    cost_curves = reduction_tech_cost_pareto[optimal_pareto].droplevel(
        'technologies'
    )
    tc_names = cost_curves.index.names
    for k, v in fleet_shares.stack().groupby(keys):
        index = v.index.droplevel(keys[:2]).reorder_levels(tc_names)
        shares, ref = v.values, f_ref.loc[k[:-1]].unstack(s_keys)[index]
        target = trgs.get(k, pd.Series()).dropna()
        ref = ref.loc[target.index].values
        factors, target = shares * ref, target.values
        points = cost_curves.loc[index].groupby(index.names)
        p = {
            i: j[['reduction', 'cost']].sort_values('reduction').values
            for i, j in points
        }
        p = [p[i] for i in index]
        i_min = [np.argmin(v[:, 1]) for v in p]
        p = {
            'points': p,
            'x_max': np.array([v[-1, 0] for v in p]),
            'x_min': np.array([v[i, 0] for v, i in zip(p, i_min)])
        }
        p['x_min'] = np.minimum(p['x_min'], p['x_max'] - .0000001)
        x = p['x_max']
        b = np.sum((1 - x) * factors, axis=1) <= target
        run = valid = b.all()
        if not run:
            b = np.isclose(ref[~b], 0).all(axis=0)
            run = b.any()
            if run:
                p['x_min'] = np.where(
                    b[None, :], p['x_min'], p['x_max'] - .0000001
                )
                target = np.array([])
        if run:
            fut = executor.submit(_opt_task, shares, factors, target, p)
        else:
            fut = np.column_stack((x, _make_cost_func(p)(x)))
        res[k] = v.index, valid, shares, fut
    dfs = []
    it = tqdm.tqdm(list(res.items()), desc="fleet_reduction_tech_cost")
    for k, (index, valid, shares, reduction_tech_cost) in it:
        df = pd.DataFrame(
            await_result(reduction_tech_cost), columns=['reduction', 'cost'],
            index=index
        )
        df['shares'] = shares
        df['valid'] = valid
        dfs.append(df.reset_index())
    return pd.concat(dfs, axis=0).set_index(keys + ['powertrain', 'segment'])


@sh.add_function(
    dsp, True, True, outputs=['fleet_reduction_tech_cost'],
    input_domain=lambda b, *args: b
)
def calculate_fleet_reduction_tech_cost_v1(
        use_curves, fleet_shares, reduction_tech_cost_curves, fleet_targets,
        fleet_co2_references, executor=DummyExecutor()):
    """
    Calculate the optimal fleet reductions and costs.

    :param fleet_shares:
        Fleet shares.
    :type fleet_shares: pandas.Dataframe

    :param reduction_tech_cost_curves:
        Parameters of reduction/Cost curves.
    :type reduction_tech_cost_curves: pandas.Dataframe

    :param fleet_targets:
        Fleet emission targets.
    :type fleet_targets: pandas.Dataframe

    :param fleet_co2_references:
        Fleet CO2 emission at reference year.
    :type fleet_co2_references: pandas.Dataframe

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :return:
        Optimal fleet reductions and costs.
    :rtype: pandas.Dataframe
    """
    keys = ['scenario', 'fleet', 'cost_type', 'registration_year']
    s_keys = ['powertrain', 'segment']
    res, trgs = {}, fleet_targets.T
    f_ref = fleet_co2_references.unstack(s_keys)
    tc_names = reduction_tech_cost_curves.index.names
    for k, v in fleet_shares.stack().groupby(keys):
        index = v.index.droplevel(keys[:2]).reorder_levels(tc_names)
        params = reduction_tech_cost_curves.loc[index]
        shares, ref = v.values, f_ref.loc[k[:-1]].unstack(s_keys)[params.index]
        target = trgs.get(k, pd.Series()).dropna()
        ref = ref.loc[target.index][v.index.droplevel([
                i for i in v.index.names if i not in ref.columns.names
        ])].values
        factors, target = shares * ref, target.values
        p = {i: j.values[None, :] for i, j in params.items()}
        x_min, x_max = params['x_min'].values, params['x_max'].values
        x = x_min[None, :] + np.linspace(0, 1, 10000)[:, None] * (x_max - x_min)
        i_min = np.maximum(np.argmin(_make_cost_func(p)(x), axis=0) - 1, 0)
        p['x_min'] = np.array([v[i] for i, v in zip(i_min, x.T)])
        x = params['x_max'].values
        b = np.sum((1 - x) * factors, axis=1) <= target
        run = valid = b.all()
        if not run:
            b = np.isclose(ref[~b], 0).all(axis=0)
            run = b.any()
            if run:
                p['x_min'] = np.where(
                    b[None, :], p['x_min'], p['x_max'] - .0000001
                )
                target = np.array([])
        if run:
            fut = executor.submit(_opt_task, shares, factors, target, p)
        else:
            fut = np.column_stack((x, _make_cost_func(p)(x)))
        res[k] = v.index, valid, shares, fut
    dfs = []
    it = tqdm.tqdm(list(res.items()), desc="fleet_reduction_tech_cost")
    for k, (index, valid, shares, reduction_tech_cost) in it:
        df = pd.DataFrame(
            await_result(reduction_tech_cost), columns=['reduction', 'cost'],
            index=index
        )
        df['shares'] = shares
        df['valid'] = valid
        dfs.append(df.reset_index())
    return pd.concat(dfs, axis=0).set_index(keys + ['powertrain', 'segment'])


@sh.add_function(dsp, outputs=['fleet_energy'])
def calculate_fleet_energy(
        fleet_reduction_tech_cost, fleet_energy_references):
    """
    Calculates the fleet energy consumptions per vehicle.

    :param fleet_reduction_tech_cost:
        Optimal fleet reductions and costs.
    :type fleet_reduction_tech_cost: pandas.Dataframe

    :param fleet_energy_references:
        Fleet energy consumption at reference year.
    :type fleet_energy_references: pandas.Dataframe

    :return:
        Fleet energy consumptions per vehicle.
    :rtype: pandas.Dataframe
    """
    df = (1 - fleet_reduction_tech_cost['reduction'])
    return (df * fleet_energy_references.stack()).dropna().unstack('mode')
