# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides the DIONE Cost Curve model `dsp`.

Sub-Modules:

.. currentmodule:: dione.model.cost_curve

.. autosummary::
    :nosignatures:
    :toctree: cost_curve/

    problem
"""
import gc
import tqdm
import numpy as np
import pandas as pd
import schedula as sh
from ...utils import DummyExecutor

# Cost Curve Model definition.
dsp = sh.BlueDispatcher(name='Cost Curve Model')


def _define_cases(reduction_tech_cost, include_exclude_tech=None):
    df = reduction_tech_cost.copy()
    df['vary'] = True
    if include_exclude_tech is not None:
        df = df.loc[df.index.difference(
            include_exclude_tech[include_exclude_tech == -1].index
        )]
        df.loc[df.index.intersection(
            include_exclude_tech[include_exclude_tech == 1].index
        ), 'vary'] = False
    return df.sort_values('reduction', ascending=False)


def _tech2num(tech_names, incompatibility_tech):
    kk = {v: k for k, v in enumerate(tech_names)}
    inc = {
        kk[k]: {kk[i] for i in v if i in kk}
        for k, v in incompatibility_tech.items()
        if k in kk
    }
    return {k: v for k, v in inc.items() if v}


def _pareto_process(reduction_tech_cost, incompatibilities):
    from pymoo.algorithms.moo.rnsga2 import NSGA2
    from pymoo.factory import get_crossover, get_mutation
    from pymoo.optimize import minimize
    from .problem import Problem, Repair
    from pymoo.util.termination.default import \
        MultiObjectiveSpaceToleranceTermination
    problem = Problem(reduction_tech_cost)
    n = reduction_tech_cost.shape[0]
    if n <= 10:  # Brute force.
        termination = 'n_gen', 1
        i = 1 + (n - 1) // 8
        sampling = np.unpackbits(
            np.arange(2 ** n, dtype='>i%d' % i).view('%d,uint8' % i),
            axis=1
        ).astype(bool)[:, -n:]
        pop_size = sampling.shape[0]
    else:
        pop_size = max(n * 2 + 1 + 200, 1000)
        termination = MultiObjectiveSpaceToleranceTermination(
            tol=0.0025,
            nth_gen=5,
            n_last=50,
            n_max_gen=1000
        )
        sampling = np.ones((pop_size, n), bool)
        sampling[:n] = np.diag(np.ones(n)).astype(bool)
        sampling[-(n + 1):] = False
        full = range(n)
        for k, i in enumerate(full, 2):
            case = set(full) - incompatibilities.get(i, set())
            for j in full:
                if j in case and j in incompatibilities:
                    case -= incompatibilities[j]
            sampling[-k, list(case)] = True
    gc.collect()
    algorithm = NSGA2(
        pop_size=pop_size,
        sampling=sampling,
        crossover=get_crossover("bin_two_point"),
        mutation=get_mutation("bin_bitflip"),
        repair=Repair(incompatibilities),
        eliminate_duplicates=False
    )
    sol = minimize(problem, algorithm, termination, seed=1)
    sol.X, i = np.unique(sol.X, axis=0, return_index=True)
    return sol.F[i], sol.X


@sh.add_function(dsp, True, True, outputs=['reduction_tech_cost_pareto_raw'])
def calculate_reduction_tech_cost_pareto(
        reduction_tech_cost, incompatibility_tech, include_exclude_tech=None,
        executor=DummyExecutor()):
    """
    Finds the best technology combinations that maximize the reduction
    minimizing the implementation cost.

    :param reduction_tech_cost:
        List of technology reduction and implementation cost for each
        powertrain, segment, and registration_year year.
    :type reduction_tech_cost: pandas.Dataframe

    :param incompatibility_tech:
        Matrix of incompatible technologies.
    :param incompatibility_tech: pandas.Dataframe

    :param include_exclude_tech:
        List of technologies to be included (forced) or excluded from the
        optimization process defined for each powertrain, segment, and
        registration_year year.
    :type include_exclude_tech: pandas.Dataframe

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :return:
        Best technology combinations that maximize the reduction minimizing
        the implementation cost.
    :rtype: pandas.Dataframe
    """
    from sklearn.preprocessing import MaxAbsScaler
    keys = ['powertrain', 'segment', 'registration_year', 'cost_type']
    cases = _define_cases(reduction_tech_cost, include_exclude_tech)
    cases['reduction'] = 1 - cases['reduction']
    res = []
    it = tqdm.tqdm(cases.groupby(keys),
                   desc="load reduction_tech_cost_pareto_raw")
    for k, data in it:
        b = data['vary'].values
        df = data.loc[b, ['reduction', 'cost']]
        df = df[~((df['reduction'] == 1) & (df['cost'] == 0))] \
            .sort_values(['reduction', 'cost'], ascending=(False, True))
        i = np.where(df['reduction'] == 1)[0]
        if i.size > 1:
            df.iloc[i[1:], :] = np.nan
            df.dropna(inplace=True)
        tech_names = df.index.get_level_values('technology').values
        reduction_tech_cost = df[['reduction', 'cost']].values
        scl = MaxAbsScaler()
        reduction_tech_cost[:, 1] = scl.fit_transform(
            reduction_tech_cost[:, [1]]
        ).ravel()
        incompatibilities = _tech2num(tech_names, incompatibility_tech)
        b = ~b
        cb, rb, base_techs = 0, 1, []
        if b.any():
            df = data.loc[b, ['reduction', 'cost']]
            base_techs.extend(df.index.get_level_values('technology').values)
            cb = df['cost'].sum()
            rb = np.prod(df['reduction'])
        res.append((k, base_techs, tech_names, cb, rb, scl, executor.submit(
            _pareto_process, reduction_tech_cost, incompatibilities
        )))
    dfs = []
    it = tqdm.tqdm(res, desc="reduction_tech_cost_pareto_raw")
    for k, base_techs, tech_names, cb, rb, scl, fut in it:
        rc, comb = sh.await_result(fut)
        if not rc.flags.writeable:
            rc = np.copy(rc)
        rc[:, 1] = scl.inverse_transform(rc[:, [1]]).ravel()
        i = rc[:, 0].argmax()
        if rc[i, 0] < 1 and rc[i, 1] < 0:
            rc = np.append([[1, 0]], rc, axis=0)
            comb = np.append([np.zeros_like(comb[0, :])], comb, axis=0)
        if base_techs:
            rc[:, 1] += cb
            rc[:, 0] *= rb
        rc[:, 0] = 1 - rc[:, 0]
        df = pd.DataFrame(rc, columns=['reduction', 'cost'])
        df['technologies'] = [
            '[%s]' % ';'.join(sorted(base_techs + tech_names[x].tolist()))
            for x in comb
        ]
        df.drop_duplicates(inplace=True)
        df.sort_values('reduction', inplace=True)
        for i, j in zip(keys, k):
            df[i] = j
        dfs.append(df)
    del res
    df = pd.concat(dfs, axis=0)
    df.set_index(keys + ['technologies'], inplace=True)
    return df


@sh.add_function(dsp, True, True, outputs=['reduction_tech_cost_pareto'])
def correct_reduction_tech_cost_pareto(
        reduction_tech_cost_pareto_raw, reduction_tech_cost_params=None):
    """
    Corrects the pareto points.

    :param reduction_tech_cost_pareto_raw:
        Best technology combinations that maximize the reduction minimizing
        the implementation cost.
    :type reduction_tech_cost_pareto_raw: pandas.Dataframe

    :param reduction_tech_cost_params:
        Configuration parameters for reduction cost curves.
    :type reduction_tech_cost_params: pandas.Dataframe

    :return:
        Corrected technology combinations that maximize the reduction
        minimizing the implementation cost.
    :rtype: pandas.Dataframe
    """
    if reduction_tech_cost_params is None:
        return reduction_tech_cost_pareto_raw
    corrections = 'BA', 'BSC', 'TO', 'RCO2', 'RC'
    params, pareto = reduction_tech_cost_params, reduction_tech_cost_pareto_raw
    corrections = [k for k in params.columns if k in corrections]
    index = pareto.index.join(params.index, how='inner')
    index = index.droplevel('technologies').drop_duplicates()
    params = params.loc[index, corrections]
    if not params.empty:
        pareto = reduction_tech_cost_pareto_raw.copy()
        for k, v in params.iterrows():
            v = v.dropna()
            df = pareto.loc[k]
            x, y = df.values.T
            if 'BA' in v:
                y -= np.interp(v['BA'], x, y)
                x -= v['BA']
                b = x <= 0
                i = np.where(b, x, -np.inf).argmax()
                x[b] = y[b] = np.nan
                x[i] = y[i] = 0
            if 'BSC' in v:
                y -= v['BSC'] * 100 * x
            if 'TO' in v and v['TO'] != 0 and np.nanmax(x):
                x *= 1 - v['TO'] * x / np.nanmax(x)
            if 'RCO2' in v:
                x = 1 - (1 - x) * (1 - v['RCO2'])
            if 'RC' in v:
                y += v['RC']
            df['reduction'], df['cost'] = x, y
        pareto = pareto.dropna(axis=0)
    return pareto


def _best_pareto_task(p):
    from scipy.spatial import ConvexHull
    from scipy.spatial.qhull import QhullError
    gc.collect()
    n = p.shape[0]
    p = np.append(p, [(
        (p[:, 0].min() + p[:, 0].max()) / 2, p[:, 1].max() + 1
    )], axis=0)
    try:
        best = ConvexHull(p).vertices
    except QhullError:
        return np.arange(n)
    return best[best < n]


@sh.add_function(dsp, True, True, outputs=['optimal_pareto'])
def identify_optimal_pareto(
        reduction_tech_cost_pareto, executor=DummyExecutor()):
    """
    Identifies the optimal pareto front of technology combinations that maximize
    the reduction minimizing the implementation cost.

    :param reduction_tech_cost_pareto:
        Corrected technology combinations that maximize the reduction
        minimizing the implementation cost.
    :type reduction_tech_cost_pareto: pandas.Dataframe

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :return:
        Optimal pareto front of technology combinations that maximize the CO2
        reduction minimizing the implementation cost.
    :rtype: pandas.Dataframe
    """
    keys = ['powertrain', 'segment', 'registration_year', 'cost_type']
    it = [
        (df.index, executor.submit(
            _best_pareto_task, df.values
        ) if df.shape[0] > 2 else np.ones(df.index.shape[0], dtype=bool))
        for k, df in reduction_tech_cost_pareto.groupby(keys)
    ]
    res = pd.Series(
        False, index=reduction_tech_cost_pareto.index, name='optimal'
    )
    for index, i in tqdm.tqdm(it, desc="optimal_pareto"):
        res.loc[index[sh.await_result(i)]] = True
    return res


def _reduction_tech_cost_function(p, x):
    return p['A'] * x ** 2 + p['B'] * x + p['C'] + p['c'] / (x - p['x0'])


def _reduction_tech_cost_residual(pars, x, y):
    return _reduction_tech_cost_function(pars.valuesdict(), x) - y


def _fit_curve(p, xx, yy, method='leastsq'):
    import lmfit
    # noinspection PyUnresolvedReferences
    return lmfit.minimize(
        _reduction_tech_cost_residual, p, args=(xx, yy), nan_policy='omit',
        method=method
    ).params


def _fit_task(conf, x, y, is_optimal=True):
    import lmfit
    gc.collect()
    x_min = conf.get('x_min', {}).get('value', x[0])
    x_max = conf.get('x_max', {}).get('value', x[-1])
    if is_optimal:
        xx = np.linspace(x_min, x_max, num=1000)
        yy = np.interp(xx, x, y)
    else:
        xx, yy = x, y
    p = lmfit.Parameters()
    for k, kw in conf.items():
        if k in ('x_min', 'y_min', 'x_max', 'y_max'):
            continue
        p.add(k, **kw)
    if p['x0'].vary:
        p['x0'].vary = False
        p = _fit_curve(p, xx, yy, method='nelder')
        p['x0'].vary = True
    p = _fit_curve(p, xx, yy, method='nelder')
    p = _fit_curve(p, xx, yy, method='least_squares').valuesdict()
    p['x_min'], p['x_max'] = x_min, x_max
    p['y_min'], p['y_max'] = y.min(), y.max()
    p['MAE'] = np.mean(np.abs(_reduction_tech_cost_function(p, xx) - yy))
    return p


def _define_params_config(params=None):
    default = {
        'A': {'value': 0}, 'B': {'value': 0}, 'C': {'value': 0},
        'c': {'value': 0}, 'x0': {'value': 1, 'min': 0},
        'x_min': {}, 'y_min': {}, 'x_max': {}, 'y_max': {}
    }
    conf = {None: default}
    if params is not None:
        params = params[[k for k in params.columns if k in default]]
        for k, r in params.iterrows():
            sh.get_nested_dicts(conf, k).update({
                i: {'value': v, 'vary': False} for i, v in r.dropna().items()
            })
    return conf


@sh.add_function(dsp, True, True, outputs=['reduction_tech_cost_curves'])
def calculate_reduction_tech_cost_params(
        reduction_tech_cost_pareto, optimal_pareto,
        reduction_tech_cost_params=None, executor=DummyExecutor(),
        use_optimal_fitting=True):
    """
    Fits the parameters of reduction/Cost curves.

    :param reduction_tech_cost_pareto:
        Corrected technology combinations that maximize the reduction
        minimizing the implementation cost.
    :type reduction_tech_cost_pareto: pandas.Dataframe

    :param optimal_pareto:
        Optimal pareto front of technology combinations that maximize the CO2
        reduction minimizing the implementation cost.
    :type optimal_pareto: pandas.Dataframe

    :param reduction_tech_cost_params:
        Configuration parameters for reduction cost curves.
    :type reduction_tech_cost_params: pandas.Dataframe

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :param use_optimal_fitting:
        Use optimal pareto to fit the parameters of the reduction cost curves.
    :type use_optimal_fitting: bool

    :return:
        Parameters of reduction/Cost curves.
    :rtype: pandas.Dataframe
    """
    keys = ['powertrain', 'segment', 'registration_year', 'cost_type']
    params_config = _define_params_config(reduction_tech_cost_params)
    default, rc = params_config[None], reduction_tech_cost_pareto
    if use_optimal_fitting:
        rc = rc[optimal_pareto]
    res = {
        k: np.unique(df[['reduction', 'cost']].values, axis=0).T
        for k, df in rc.groupby(keys)
    }
    res = {
        k: executor.submit(
            _fit_task, sh.combine_nested_dicts(default, params_config.get(k)),
            *rc, is_optimal=use_optimal_fitting
        ) for k, rc in res.items() if rc.shape[1] > 1
    }

    # noinspection PyTypeChecker
    df = pd.DataFrame([
        sh.combine_dicts(sh.map_list(keys, *k), sh.await_result(v))
        for k, v in tqdm.tqdm(
            list(res.items()), desc="reduction_tech_cost_curves"
        )
    ])
    df.set_index(keys, inplace=True)
    return df
