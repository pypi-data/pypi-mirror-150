# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It contains functions and a model `dsp` to parse the raw_input data.
"""
import functools
import numpy as np
import pandas as pd
import schedula as sh
from .excel import array2frame

#: Parsing Model.
dsp = sh.BlueDispatcher(name='parse_data', raises=True)
xl_data = [
    'reduction_tech_cost_params', 'incompatibility_tech',
    'include_exclude_tech', 'reduction_tech_cost_pareto',
    'fleet_reduction_tech_cost', 'fleet_registrations',
    'reduction_tech_cost_curves', 'fleet_energy_cost', 'fleet_tco',
    'fleet_energy', 'fleet_co2_references', 'fleet_energy_references',
    'fleet_targets', 'fleet_activity', 'reduction_tech_cost',
    'fleet_residual_maintenance'
]
model_data = [
    'optimal_pareto', 'fleet_maintenance_cost', 'fleet_residual_value',
    'fleet_activity_cost', 'fleet_tech_cost', 'fleet_total_cost',
    'fleet_cumulative_maintenance_cost', 'fleet_cumulative_tech_cost',
    'fleet_cumulative_activity_cost', 'fleet_cumulative_total_cost',
    'fleet_margin_tech_cost', 'fleet_maintenance_vat'
]
model_data.extend(set(xl_data) - {'fleet_residual_maintenance', 'fleet_tco'})


@sh.add_function(dsp, outputs=['extra'] + ['raw_%s' % k for k in xl_data])
def split_raw_data(raw_data):
    res = [sh.selector(set(raw_data) - set(xl_data), raw_data)]
    res.extend(
        raw_data[k] if k in raw_data else pd.DataFrame() for k in xl_data
    )
    return res


@sh.add_function(dsp, inputs=['extra'] + model_data, outputs=['inputs'])
def define_inputs(extra, *args):
    return sh.combine_dicts(extra, {
        k: v for k, v in zip(model_data, args) if v is not sh.EMPTY
    })


def _multi(x):
    if isinstance(x, str):
        x = x.strip(' ')
        if x.startswith('[') and x.endswith(']'):
            x = [v.strip(' ') for v in x[1:-1].split(',')]
            x = [v for v in x if v]
        if not x:
            x = []
    return x


def _parse_table(df, keys=(
        'powertrain', 'segment', 'registration_year', 'cost_type'
)):
    if not isinstance(df, pd.DataFrame):
        df = array2frame(df)
    df.dropna(how='all', inplace=True)
    df.dropna(how='all', axis=1, inplace=True)

    for k in () if df.empty else keys:
        df[k] = df[k].map(_multi)
        df = df.explode(k)
    return df


@sh.add_function(
    dsp, inputs=['raw_incompatibility_tech'], outputs=['incompatibility_tech']
)
def parse_incompatibility_tech(df, matrix=True):
    if isinstance(df, pd.DataFrame) and df.empty:
        return sh.EMPTY
    df = array2frame(df)
    df.set_index('technology', inplace=True)
    df.fillna(False, inplace=True)
    df.columns.name = 'technology'
    df = df.astype(bool)
    if matrix:
        df.values[:] = np.triu(df.values, 1)
    for _ in range(2):
        df.reset_index(inplace=True)
        df['technology'] = df['technology'].map(_multi)
        df = df.explode('technology')
        df.set_index('technology', inplace=True)
        df = df.T
    df.fillna(False, inplace=True)
    df = df.astype(bool).stack()
    df = df[df]
    df = df.append(df.swaplevel()).unstack()
    df.fillna(False, inplace=True)
    np.fill_diagonal(df.values, False)
    df = df | df.T
    return df.apply(lambda x: set(x.index[x]), axis=1)


@sh.add_function(
    dsp, function_id='parse_reduction_tech_cost_params',
    inputs=['raw_reduction_tech_cost_params'],
    outputs=['reduction_tech_cost_params']
)
def parse_cases(
        df, keys=('powertrain', 'segment', 'registration_year', 'cost_type'),
        how='all', name=None, dtype=None):
    if isinstance(df, pd.DataFrame) and df.empty:
        return sh.EMPTY
    keys = list(keys)
    df = _parse_table(df, keys)
    df.dropna(how=how, inplace=True)
    if not df.empty:
        dtype = dtype or {
            'age': float, 'registration_year': float, 'projection_year': float
        }
        df = df.astype(sh.selector(df.columns, dtype, allow_miss=True))
        df.set_index(keys, inplace=True)
        if name is not None:
            df.drop(name, errors='ignore', inplace=True, axis=1)
            df.columns.name = name
            if name in dtype:
                df.columns = df.columns.astype(dtype[name])
    return sh.EMPTY if df.empty else df


dsp.add_function(
    function_id='parse_reduction_tech_cost_curves',
    function=functools.partial(parse_cases, how='any'),
    inputs=['raw_reduction_tech_cost_curves'],
    outputs=['reduction_tech_cost_curves']
)
dsp.add_function(
    function_id='parse_reduction_tech_cost', inputs=['raw_reduction_tech_cost'],
    function=functools.partial(parse_cases, keys=(
        'powertrain', 'segment', 'registration_year', 'cost_type', 'technology'
    ), how='any'), outputs=['reduction_tech_cost']
)


@sh.add_function(
    dsp, inputs=['raw_include_exclude_tech'], outputs=['include_exclude_tech']
)
def parse_include_exclude_tech(df):
    keys = ['powertrain', 'segment', 'registration_year', 'cost_type']
    df = parse_cases(df, keys, name='technology')
    if df is not sh.EMPTY:
        return df.stack().dropna().astype(int)
    return df


@sh.add_function(
    dsp, inputs=['raw_reduction_tech_cost_pareto'],
    outputs=['reduction_tech_cost_pareto', 'optimal_pareto']
)
def parse_reduction_tech_cost_pareto(df):
    df = parse_cases(df, (
        'powertrain', 'segment', 'registration_year', 'cost_type'
    ))
    if df is not sh.EMPTY:
        df.set_index('technologies', append=True, inplace=True)
        if not df.empty:
            return df[['reduction', 'cost']], df.get('optimal', sh.EMPTY)
    return [df] * 2


dsp.add_function(
    function_id='parse_fleet_registrations',
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type'
    ), name='registration_year'),
    inputs=['raw_fleet_registrations'], outputs=['fleet_registrations']
)
dsp.add_function(
    function_id='parse_fleet_activity',
    function=functools.partial(parse_cases, name='mode', keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type',
        'perspective', 'registration_year', 'projection_year'
    )), inputs=['raw_fleet_activity'], outputs=['fleet_activity']
)
dsp.add_function(
    function_id='parse_fleet_energy',
    inputs=['raw_fleet_energy'],
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'registration_year',
        'cost_type', 'projection_year'
    ), name='mode'), outputs=['fleet_energy']
)
dsp.add_function(
    function_id='parse_fleet_energy_cost',
    inputs=['raw_fleet_energy_cost'],
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type',
        'perspective', 'registration_year', 'projection_year'
    ), name='mode'), outputs=['fleet_energy_cost']
)
dsp.add_function(
    function_id='parse_fleet_targets', inputs=['raw_fleet_targets'],
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'cost_type', 'registration_year'
    )), outputs=['fleet_targets']
)
dsp.add_function(
    function_id='parse_fleet_co2_references',
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type'
    ), name='emission'),
    inputs=['raw_fleet_co2_references'], outputs=['fleet_co2_references']
)
dsp.add_function(
    function_id='parse_fleet_energy_references',
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type',
        'registration_year', 'projection_year'
    ), name='mode'),
    inputs=['raw_fleet_energy_references'], outputs=['fleet_energy_references']
)

dsp.add_function(
    function_id='parse_fleet_reduction_tech_cost',
    inputs=['raw_fleet_reduction_tech_cost'],
    function=functools.partial(parse_cases, keys=(
        'scenario', 'fleet', 'registration_year', 'powertrain', 'segment',
        'cost_type'
    )), outputs=['fleet_reduction_tech_cost']
)


def parse_split_cases(df, keys, cols):
    df = parse_cases(df, keys)
    if df is not sh.EMPTY:
        return [df[k].dropna() if k in df else sh.EMPTY for k in cols]
    return [df] * len(cols)


dsp.add_function(
    function_id='parse_fleet_residual_maintenance',
    inputs=['raw_fleet_residual_maintenance'],
    function=functools.partial(parse_split_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type',
        'perspective', 'registration_year', 'age'
    ), cols=(
        'residual_value', 'maintenance_cost', 'maintenance_vat',
        'margin_tech_cost'
    )),
    outputs=[
        'fleet_residual_value', 'fleet_maintenance_cost',
        'fleet_maintenance_vat', 'fleet_margin_tech_cost'
    ]
)
dsp.add_function(
    function_id='parse_fleet_tco',
    inputs=['raw_fleet_tco'],
    function=functools.partial(parse_split_cases, keys=(
        'scenario', 'fleet', 'powertrain', 'segment', 'cost_type',
        'perspective', 'registration_year', 'age'
    ), cols=(
        'activity_cost', 'tech_cost', 'total_cost',
        'cumulative_maintenance_cost', 'cumulative_tech_cost',
        'cumulative_activity_cost', 'cumulative_total_cost'
    )),
    outputs=[
        'fleet_activity_cost', 'fleet_tech_cost', 'fleet_total_cost',
        'fleet_cumulative_maintenance_cost', 'fleet_cumulative_tech_cost',
        'fleet_cumulative_activity_cost', 'fleet_cumulative_total_cost'
    ]
)
