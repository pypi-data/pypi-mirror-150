# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides computational model `dsp`.

Sub-Modules:

.. currentmodule:: dione.model

.. autosummary::
    :nosignatures:
    :toctree: model/

    cost_curve
    cross_opt
    tco
"""
import schedula as sh
from . import cost_curve, cross_opt, tco

# Base Model definition.
dsp = sh.BlueDispatcher(name='Base Model')
dsp.add_dispatcher(
    cost_curve.dsp,
    inputs=[
        'reduction_tech_cost_params', 'incompatibility_tech', 'optimal_pareto',
        'reduction_tech_cost_pareto', 'include_exclude_tech', 'executor',
        'reduction_tech_cost_curves', 'reduction_tech_cost',
        'use_optimal_fitting'
    ],
    outputs=[
        'reduction_tech_cost_pareto', 'reduction_tech_cost_curves',
        'optimal_pareto'
    ],
    include_defaults=True
)
dsp.add_dispatcher(
    cross_opt.dsp,
    inputs=[
        'fleet_reduction_tech_cost', 'fleet_registrations', 'fleet_energy',
        'reduction_tech_cost_curves', 'fleet_energy_references', 'executor',
        'fleet_co2_references', 'fleet_targets', 'reduction_tech_cost_pareto',
        'optimal_pareto', 'use_curves'
    ],
    outputs=['fleet_reduction_tech_cost', 'fleet_energy'],
    include_defaults=True
)
dsp.add_dispatcher(
    tco.dsp,
    inputs=[
        'fleet_reduction_tech_cost', 'fleet_residual_value', 'fleet_total_cost',
        'fleet_activity_cost', 'fleet_activity', 'fleet_energy',
        'fleet_maintenance_cost', 'fleet_energy_cost', 'fleet_tech_cost',
        'fleet_margin_tech_cost', 'fleet_maintenance_vat'
    ],
    outputs=[
        'fleet_cumulative_maintenance_cost', 'fleet_activity_cost',
        'fleet_total_cost', 'fleet_cumulative_activity_cost',
        'fleet_cumulative_total_cost', 'fleet_tech_cost',
        'fleet_cumulative_tech_cost',
    ],
    include_defaults=True
)
