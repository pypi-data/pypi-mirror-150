# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It contains functions and a model `dsp` to render the graphs.
"""
import collections
import numpy as np
import pandas as pd
import schedula as sh
from itertools import cycle
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator

__graphs__ = collections.OrderedDict()
#: Graph Model.
dsp = sh.BlueDispatcher(name='Graph Model', raises=True)
__graphs__['cost_curves_graph'] = {'label': 'Cost Curves'}
__graphs__['cross_optimization_graph'] = {'label': 'Cross Optimization'}
__graphs__['tco_graph'] = {'label': 'Total Cost of Ownership'}


@sh.add_function(dsp, True, True, outputs=['cost_curves_graph'])
def render_cost_curves_graph(
        reduction_tech_cost_pareto=None, reduction_tech_cost_curves=None,
        optimal_pareto=None, fleet_reduction_tech_cost=None):
    """
    Renders the cost curves.

    :param reduction_tech_cost_pareto:
        Corrected technology combinations that maximize the reduction
        minimizing the implementation cost.
    :type reduction_tech_cost_pareto: pandas.Dataframe

    :param reduction_tech_cost_curves:
        Parameters of reduction/Cost curves.
    :type reduction_tech_cost_curves: pandas.Dataframe

    :param optimal_pareto:
        Optimal pareto front of technology combinations that maximize the CO2
        reduction minimizing the implementation cost.
    :type optimal_pareto: pandas.Dataframe

    :param fleet_reduction_tech_cost:
        Optimal fleet reductions and costs.
    :type fleet_reduction_tech_cost: pandas.Dataframe

    :return:
        The Cost curves graph.
    :rtype: plotly.Figure
    """
    plots = {}
    keys = ['powertrain', 'segment', 'registration_year', 'cost_type']
    palette = cycle(qualitative.Plotly)
    symbols = cycle([
        k for k in SymbolValidator().values[2::3] if k.endswith('-open')
    ])
    colors, markers = {}, {}
    legend = set()

    if reduction_tech_cost_curves is not None:
        df = reduction_tech_cost_curves.reset_index()
        colors.update({
            k: next(palette)
            for k in sorted(set(df['registration_year'].unique()) - set(colors))
        })
        from ..model.cost_curve import _reduction_tech_cost_function
        for (p, s, a, c), v in df.groupby(keys):
            name = '{}/{}'.format(int(a), c)
            legendgroup = '{}/{}/{}'.format(p, s, name)
            d = v.iloc[0]
            x = np.linspace(d.get('x_min', 0), d.get('x_max', 1), num=100)
            sh.get_nested_dicts(plots, 2, p, s, default=list).append({
                'x': x, 'y': _reduction_tech_cost_function(d, x),
                'mode': 'lines', 'legendgroup': legendgroup, 'name': name,
                'showlegend': legendgroup not in legend, 'line': {
                    'color': colors[a], 'width': 1
                }
            })
            legend.add(legendgroup)

    if reduction_tech_cost_pareto is not None:
        df = reduction_tech_cost_pareto.reset_index()
        colors.update({
            k: next(palette)
            for k in sorted(set(df['registration_year'].unique()) - set(colors))
        })
        for (p, s, a, c), v in df.groupby(keys):
            name = '{}/{}'.format(int(a), c)
            legendgroup = '{}/{}/{}'.format(p, s, name)
            sh.get_nested_dicts(plots, 0, p, s, default=list).append({
                'x': v['reduction'].values, 'y': v['cost'].values,
                'mode': 'markers', 'legendgroup': legendgroup, 'name': name,
                'opacity': 0.5, 'marker': {'color': colors[a], 'size': 3},
                'showlegend': legendgroup not in legend
            })
            legend.add(legendgroup)

        if optimal_pareto is not None:
            df = reduction_tech_cost_pareto[optimal_pareto]
            for (p, s, a, c), v in df.groupby(keys):
                name = '{}/{}'.format(int(a), c)
                legendgroup = '{}/{}/{}'.format(p, s, name)
                sh.get_nested_dicts(plots, 1, p, s, default=list).append({
                    'x': v['reduction'].values, 'y': v['cost'].values,
                    'mode': 'markers', 'legendgroup': legendgroup, 'name': name,
                    'showlegend': legendgroup not in legend, 'marker': {
                        'color': colors[a], 'size': 3
                    }
                })
                legend.add(legendgroup)

    if fleet_reduction_tech_cost is not None:
        df = fleet_reduction_tech_cost.reset_index()
        colors.update({
            k: next(palette)
            for k in sorted(set(df['registration_year'].unique()) - set(colors))
        })
        for (p, s, a, c, i, j), v in df.groupby(keys + ['scenario', 'fleet']):
            k = '{}/{}/{}/{}'.format(i, j, int(a), c)
            legendgroup = '{}/{}/{}/{}/{}'.format(p, s, i, int(a), c)
            if (i, j) not in markers:
                markers[(i, j)] = next(symbols)
            x, y = v.iloc[0][['reduction', 'cost']]
            sh.get_nested_dicts(plots, 3, p, s, default=list).append({
                'x': [x], 'y': [y], 'mode': 'markers',
                'legendgroup': legendgroup, 'name': k,
                'showlegend': legendgroup not in legend, 'marker': {
                    'symbol': markers[(i, j)], 'color': colors[a]
                }
            })
            legend.add(legendgroup)
    if not plots:
        return sh.NONE
    fig = go.Figure()
    visible = []
    first = True
    for (_, c, r), traces in sorted(sh.stack_nested_keys(plots)):
        for data in traces:
            fig.add_trace(go.Scatter(visible=first, **data))
            visible.append('{}/{}'.format(c, r))
        first = False
    visible = np.array(visible)
    keys = np.unique(visible)
    fig.update_layout(title_text=keys[0], updatemenus=[{
        'active': 0,
        'direction': "down",
        'pad': {"r": 10, "t": 10},
        'showactive': True,
        'x': 0,
        'xanchor': "left",
        'y': 1.1,
        'yanchor': "bottom",
        'buttons': [{
            'label': k,
            'method': "update",
            'args': [{"visible": k == visible, "title": k}]
        } for k in keys]
    }])
    return fig


@sh.add_function(dsp, True, True, outputs=['cross_optimization_graph'])
def render_cross_optimization_graph(
        fleet_reduction_tech_cost=None, fleet_energy=None):
    """
    Renders the Cross Optimization results.

    :param fleet_reduction_tech_cost:
        Optimal fleet reductions and costs.
    :type fleet_reduction_tech_cost: pandas.Dataframe

    :param fleet_energy:
        Fleet energy consumptions per vehicle.
    :type fleet_energy: pandas.Dataframe

    :return:
        The Cross Optimization graph.
    :rtype: plotly.Figure
    """
    return sh.NONE
    if fleet_reduction_tech_cost is None or fleet_energy is None:
        return sh.NONE
    keys = ['scenario', 'fleet', 'registration_year', 'powertrain', 'segment']
    shares = fleet_reduction_tech_cost['shares']
    df = (fleet_energy.stack() * shares).dropna().unstack(
        'mode'
    ).reorder_levels(keys)
    it = fleet_reduction_tech_cost[['reduction', 'cost']].mul(
        shares, axis=0
    ).groupby(keys[:-2]).sum().reorder_levels(keys[:-2])
    df['vehicle_cost'] = fleet_reduction_tech_cost['cost'].reorder_levels(keys)
    for k, v in it.items():
        df[k] = v
    return parcoords(df.reset_index().fillna(-1), keys, color='cost')


def parcoords(df, keys, color=None):
    uniques = {}
    for k in keys:
        df[k], uniques[k] = pd.factorize(df[k])
    dimensions = []
    for k, v in df.items():
        kv = {'label': k, 'values': v}
        if k in uniques:
            # noinspection PyTypeChecker
            kv['ticktext'] = ticktext = uniques[k]
            kv['tickvals'] = list(range(len(ticktext)))
        else:
            kv['range'] = [v.min(), v.max()]
        dimensions.append(kv)
    if df.empty:
        return sh.EMPTY
    line = {
        'colorscale': px.colors.sequential.Emrld[::-1],
        'showscale': True
    }
    if color in df.columns:
        line['color'] = df[color]
    return go.Figure(data=go.Parcoords(line=line, dimensions=dimensions))


@sh.add_function(dsp, True, True, outputs=['tco_graph'])
def render_tco_graph(fleet_cumulative_total_cost=None):
    """
    Renders the Total Cost of Ownership results.

    :param fleet_cumulative_total_cost:
        Fleet cumulative average consumption cost per vehicle & age.
    :type fleet_cumulative_total_cost: pandas.Dataframe

    :return:
        The Total Cost of Ownership graph.
    :rtype: plotly.Figure
    """
    if fleet_cumulative_total_cost is None:
        return sh.NONE
    return px.line(
        fleet_cumulative_total_cost.reset_index(), x='age',
        y='cumulative_total_cost',
        color='scenario', facet_col='segment', facet_row='powertrain',
        line_dash='fleet', animation_frame='registration_year'
    )
