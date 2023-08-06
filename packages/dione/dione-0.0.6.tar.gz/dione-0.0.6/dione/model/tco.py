# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides the DIONE Total Cost of Ownership model `dsp`.
"""
import numpy as np
import schedula as sh

# Total Cost of Ownership Model definition.
dsp = sh.BlueDispatcher(name='Total Cost of Ownership Model')


def _projection_year2age(df, reverse=False):
    if reverse:
        names = ['projection_year' if k == 'age' else k for k in df.index.names]
    else:
        names = ['age' if k == 'projection_year' else k for k in df.index.names]
    df = df.reset_index()
    if reverse:
        df['projection_year'] = df.pop('age') + df['registration_year']
    else:
        df['age'] = df.pop('projection_year') - df['registration_year']
        df = df[df['age'] > 0]
    df.set_index(names, inplace=True)
    return df


@sh.add_function(dsp, True, True, outputs=['fleet_activity_cost'])
def calculate_fleet_activity_cost(
        fleet_energy, fleet_energy_cost, fleet_activity):
    """
    Calculates the fleet energy consumption per vehicle.

    :param fleet_energy:
        Fleet energy consumptions per vehicle.
    :type fleet_energy: pandas.Dataframe

    :param fleet_energy_cost:
        Energy consumption cost.
    :type fleet_energy_cost: pandas.Dataframe

    :param fleet_activity:
        Fleet average activity per vehicle.
    :type fleet_activity: pandas.Dataframe

    :return:
        Fleet average energy consumption cost per vehicle & age.
    :rtype: pandas.Series
    """
    fc, cc, fa = fleet_energy, fleet_energy_cost, fleet_activity
    df = (fc.stack() * cc.stack() * fa.stack()).dropna()
    df = df.unstack('mode').sum(axis=1)
    df.name = 'activity_cost'
    return _projection_year2age(df)['activity_cost']


@sh.add_function(dsp, True, True, outputs=['fleet_tech_cost'])
def calculate_fleet_tech_cost(
        fleet_residual_value, fleet_reduction_tech_cost,
        fleet_margin_tech_cost=1):
    """
    Calculates the fleet technology cost per vehicle & age.

    :param fleet_residual_value:
        Residual vehicle value.
    :type fleet_residual_value: pandas.Series

    :param fleet_reduction_tech_cost:
        Optimal fleet reductions and costs.
    :type fleet_reduction_tech_cost: pandas.Dataframe

    :param fleet_margin_tech_cost:
        Margin coefficient for vehicle value.
    :type fleet_margin_tech_cost: pandas.Series

    :return:
        Fleet technology cost per vehicle & age.
    :rtype: pandas.Series
    """
    # noinspection PyTypeChecker
    df = fleet_reduction_tech_cost['cost'] * (1 - fleet_residual_value)
    df *= fleet_margin_tech_cost
    df = df.dropna().unstack('age')
    df[0] = np.nan
    df = df[sorted(df.columns)]
    i = np.argmax(~np.isnan(df.values), axis=1) - 1
    df.values[np.arange(df.values.shape[0]), i] = 0
    df = df.sort_index(axis=1).diff(axis=1).iloc[:, 1:].stack()
    df.name = 'tech_cost'
    return df


@sh.add_function(dsp, True, True, outputs=['fleet_maintenance_cost_final'])
def calculate_fleet_maintenance_cost_final(
        fleet_maintenance_cost, fleet_maintenance_vat=0):
    """
    Calculates the fleet maintenance cost with vat per vehicle & age.

    :param fleet_maintenance_cost:
        Fleet maintenance cost per vehicle & age.
    :type fleet_maintenance_cost: pandas.Series

    :param fleet_maintenance_vat:
        Fleet maintenance vat per vehicle & age.
    :type fleet_maintenance_vat: pandas.Series

    :return:
        Fleet maintenance cost with vat per vehicle & age.
    :rtype: pandas.Series
    """
    return fleet_maintenance_cost * (1 + fleet_maintenance_vat)


@sh.add_function(dsp, True, True, outputs=['fleet_total_cost'])
def calculate_fleet_total_cost(
        fleet_activity_cost, fleet_maintenance_cost_final, fleet_tech_cost):
    """
    Calculates the fleet total cost of ownership per vehicle & age.

    :param fleet_activity_cost:
        Fleet average energy consumption cost per vehicle & age.
    :type fleet_activity_cost: pandas.Series

    :param fleet_maintenance_cost_final:
        Fleet maintenance cost with vat per vehicle & age.
    :type fleet_maintenance_cost_final: pandas.Series

    :param fleet_tech_cost:
        Fleet technology cost per vehicle & age.
    :type fleet_tech_cost: pandas.Series

    :return:
        Fleet total cost of ownership per vehicle & age.
    :rtype: pandas.Series
    """
    cost = fleet_activity_cost + fleet_maintenance_cost_final + fleet_tech_cost
    cost.name = 'total_cost'
    return cost.dropna()


@sh.add_function(dsp, True, True, outputs=['cumulative_cases'])
def get_cumulative_cases(fleet_total_cost):
    """
    Get index of cases for the cumulative results.

    :param fleet_total_cost:
        Fleet total cost of ownership per vehicle & age.
    :type fleet_total_cost: pandas.Series

    :return:
        Index of cases for the cumulative results.
    :rtype: pandas.MultiIndex
    """
    return fleet_total_cost.index


@sh.add_function(dsp, outputs=['fleet_cumulative_tech_cost'])
def calculate_fleet_cumulative_tech_cost(cumulative_cases, fleet_tech_cost):
    """
    Calculates the fleet cumulative technology cost per vehicle & age.

    :param cumulative_cases:
        Index of cases for the cumulative results.
    :type cumulative_cases: pandas.MultiIndex

    :param fleet_tech_cost:
        Fleet technology cost per vehicle & age.
    :type fleet_tech_cost: pandas.Series

    :return:
        Fleet cumulative technology cost per vehicle & age.
    :rtype: pandas.Series
    """
    return calculate_fleet_cumulative_total_cost(
        cumulative_cases, fleet_tech_cost, 'cumulative_tech_cost'
    )


@sh.add_function(dsp, outputs=['fleet_cumulative_activity_cost'])
def calculate_fleet_cumulative_activity_cost(
        cumulative_cases, fleet_activity_cost):
    """
    Calculates the fleet cumulative average energy consumption cost per vehicle.

    :param cumulative_cases:
        Index of cases for the cumulative results.
    :type cumulative_cases: pandas.MultiIndex

    :param fleet_activity_cost:
        Fleet average energy consumption cost per vehicle & age.
    :type fleet_activity_cost: pandas.Series

    :return:
        Fleet cumulative average energy consumption cost per vehicle & age.
    :rtype: pandas.Series
    """
    return calculate_fleet_cumulative_total_cost(
        cumulative_cases, fleet_activity_cost, 'cumulative_activity_cost'
    )


@sh.add_function(dsp, outputs=['fleet_cumulative_maintenance_cost'])
def calculate_fleet_cumulative_maintenance_cost(
        cumulative_cases, fleet_maintenance_cost_final):
    """
    Calculates the fleet cumulative maintenance cost per vehicle & age.

    :param cumulative_cases:
        Index of cases for the cumulative results.
    :type cumulative_cases: pandas.MultiIndex

    :param fleet_maintenance_cost_final:
        Fleet maintenance cost with vat per vehicle & age.
    :type fleet_maintenance_cost_final: pandas.Series

    :return:
        Fleet cumulative maintenance cost per vehicle & age.
    :rtype: pandas.Series
    """
    return calculate_fleet_cumulative_total_cost(
        cumulative_cases, fleet_maintenance_cost_final,
        'cumulative_maintenance_cost'
    )


@sh.add_function(dsp, outputs=['fleet_cumulative_total_cost'])
def calculate_fleet_cumulative_total_cost(
        cumulative_cases, fleet_total_cost, name='cumulative_total_cost'):
    """
    Calculates the fleet cumulative total cost of ownership per vehicle.

    :param cumulative_cases:
        Index of cases for the cumulative results.
    :type cumulative_cases: pandas.MultiIndex

    :param fleet_total_cost:
        Fleet total cost of ownership per vehicle & age.
    :type fleet_total_cost: pandas.Series

    :param name:
        Pandas series name.
    :type name: str

    :return:
        Fleet cumulative average energy consumption cost per vehicle & age.
    :rtype: pandas.Series
    """
    df = fleet_total_cost
    index = cumulative_cases.reorder_levels(df.index.names)
    df = df.loc[index].unstack('age').sort_index(axis=1).cumsum(axis=1).stack()
    df.name = name
    return df
