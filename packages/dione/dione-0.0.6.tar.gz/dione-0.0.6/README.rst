.. _start-quick:

########################################################
DIONE:
########################################################
|pypi_ver| |travis_status| |cover_status| |docs_status|
|dependencies| |github_issues| |python_ver| |proj_license|

:release:       0.0.6
:date:          2022-02-14 11:30:00
:repository:    https://github.com/JRCSTU/dione
:pypi-repo:     https://pypi.org/project/dione/
:docs:          http://dione.readthedocs.io/
:wiki:          https://github.com/JRCSTU/dione/wiki/
:download:      http://github.com/JRCSTU/dione/releases/
:keywords:      fuel consumption, fleet, forecast
:developers:    .. include:: AUTHORS.rst
:license:       `EUPL 1.1+ <https://joinup.ec.europa.eu/software/page/eupl>`_

.. _start-intro:
.. _start-pypi:

What is DIONE?
==============
DIONE is a family of software applications that the JRC has been developing
since 2014 to support EU transport emission reduction policies. It is presently
employed to support road vehicle |CO2| emissions standards within EC’s Fit for
55 package. It has also been supporting the European Strategy for Low-Emission
Mobility.

The assessment of the costs of potential road vehicle |CO2| emissions standards
is carried out through the following computational modules:

- DIONE Cost Curve Module: Develops |CO2| reduction cost curves, applying an
  optimisation technique, which provide cost estimates associated with reaching
  a given |CO2| reduction for different vehicle segments and powertrains.
- DIONE Cross-Optimization and Energy Consumption Module: Identifies
  cost-optimal strategies to reach given emission targets and respective vehicle
  manufacturing costs, building on the cost curves. Cross-optimization outcomes
  can be used to assess the impact of different policy options on manufacturing
  costs for different manufacturer categories, contributing to the economic
  assessment.
- DIONE Total Cost of Ownership (TCO) Module: Computes total costs of ownership
  under different regulation options, summarizing the results from the previous
  steps and adding in operation and maintenance costs. Results allow assessing
  the societal costs associated with a policy option, as well as the costs for
  consumers (new vehicle buyers and second-hand vehicle buyers).

Installation
============
To install it use (with root privileges):

.. code-block:: console

    $ pip install dione

Or download the last git version and use (with root privileges):

.. code-block:: console

    $ python setup.py install

Install extras
--------------
Some additional functionality is enabled installing the following extras:

- cli: enables the command line interface.
- gui: enables the graphical user interface.
- plot: enables to plot the model process and its workflow.
- dev: installs all libraries plus the development libraries.

To install DIONE and all extras (except development libraries), do:

.. code-block:: console

    $ pip install 'dione[all]'

.. _end-quick:
.. _end-pypi:
.. _end-intro:
.. _start-guide:

Quick Start
===========
The following steps are basic commands to get familiar with DIONE procedural
workflow using both the GUI and the command line interface:

- `Run`_
- `Input Template`_
- `Data Rendering`_

.. note:: To open the GUI locally you have to execute the command `dione gui`
   from the command line. For more information regarding the gui command check
   the dedicated `documentation <_build/toctree/dione/dione.cli.html#dione-gui>`__::

Run
---
To run DIONE with some sample data you have to:

1. Generate a demo file to get familiar with the input data (for more info
   check the `link <_build/toctree/dione/dione.cli.html#dione-demo>`__)::

    ## Generate a demo file.
    $ dione demo

Or open the GUI and press **Downloads** and then **Demo**.

.. image:: _static/image/demo.png
   :width: 100%
   :alt: demo
   :align: center

2. Run DIONE and inspect the results in the ``./output`` folder.
   The workflow is plotted on the browser (for more info check the
   `link <_build/toctree/dione/dione.cli.html#dione-run>`__)::

    ## Run DIONE and open the output folder.
    $ dione run
    $ start ./output

Or open the GUI, upload the file and press **Run Simulation**.

.. image:: _static/image/run_simulation.png
   :width: 100%
   :alt: Run simulation
   :align: center

When the simulation is completed the user can download the results on his pc
(excel output file).

Input Template
--------------
To create an input file with your data you have to:

1. Generate an empty input template file (i.e., ``xxx.xlsx``)::

    ## Generate template file.
    $ dione template

Or download the template from the GUI by pressing **Downloads** and **Template**.

.. image:: _static/image/demo.png
   :width: 100%
   :alt: demo
   :align: center

2. Follow the instructions provided in the excel file to fill it in. The file is
   organized in three sections each one corresponding to one of the three module.

.. image:: _static/image/input_file.png
   :width: 100%
   :alt: Input template
   :align: center

Data Rendering
--------------
The user can also **Render Charts**, which means there is the possibility to
visualise graphs for all 3 modules: Cost Curves, Optimization, and TCO.
.. _end-guide:
.. _start-model:

Model Overview
==============
The model and its architecture are defined and designed according to the
procedural steps as shown in the diagram below.

.. dispatcher:: model
   :height: 600px
   :opt: index=True, body={'label': '"Model Overview"'}

    >>> from dione.model import dsp as model
    >>> model = model.register()


It consists of three blocks/steps that will be described in the following
sections:

- `Cost Curve Definition`_,
- `Cross Optimization and Energy Consumption`_, and
- `Total Cost of Ownership`_.


Cost Curve Definition
---------------------
Within an earlier `project <https://ec.europa.eu/clima/system/files/2017-11/ldv_co2_technologies_and_costs_to_2030_en.pdf>`_
commissioned by DG CLIMA, state-of-the-art and developing technologies were
identified, and their |CO2| reduction potentials and costs were quantified.
Starting from this data, JRC’s DIONE cost curve model develops |CO2| reduction
cost curves, which describe the mathematical relationship between |CO2|
reduction potentials and related costs for different powertrains and vehicle
segments.

The diagram below shows the procedural steps that the tool is performing.

.. dispatcher:: cost_curve
   :height: 600px
   :opt: index=True, body={'label': '"Cost Curve Model"'}

    >>> from dione.model.cost_curve import dsp as cost_curve
    >>> cost_curve = cost_curve.register()

In the first step, optimization is carried out to develop a cost curve to
identify cost-optimal packages of |CO2| reduction technologies. Then, several
transformation steps are applied to transform the solutions found. Finally, a
cost curve is fitted to the set of solutions. These steps are explained in the
following sections.

Identifying Optimal Technology Packages
***************************************
The scope of this step is to identify optimal technology packages for reducing
|CO2| emissions at minimum cost. Given the set of available |CO2| reduction
technologies, the problem consists of finding, among all possible packages
(i.e., combinations of these technologies or subsets of them), the set of
optimal configurations with minimal total costs and maximum total |CO2|
reduction. Each package found by the algorithm specifies a Pareto optimal
technology package, i.e., a combination of technologies that can be added to a
baseline vehicle to achieve a given emission reduction at the lowest possible
costs (or achieves the highest emission reduction at a given cost level).

Given a set of technologies :math:`T=\{t_1, ..., t_N\}`, each characterized by
its cost :math:`c_i`, |CO2| reduction :math:`r_i` and by a list of incompatible
technologies :math:`\{t_{ij}\}`, the problem consists of finding a set of all
feasible subsets of :math:`T` (in terms of compatibility between technologies),
called packages :math:`P_k`, which are Pareto-optimal according to the following
equations:

.. math::

    min \quad C(P_k) &= \sum_{t_i\in P_k} c_i\\
    max \quad R(P_k) &= 1 - \prod_{t_i\in P_k} (1-r_i)

where :math:`C(P_k)` and :math:`R(P_k)` are the total cost and the total |CO2|
reduction of the package :math:`P_k`.

The large numbers of possible optimization problems and the number of possible
combinations of technologies make the problem computationally difficult
(NP-hard). Moreover, available technologies are not always compatible,
i.e., not all technologies can be combined with each other. For example,
various engine downsizing technologies are available, but there would never be a
package containing more than one, which means a simple combinatorial approach
cannot be applied.

The DIONE cost curve model applies a multi-objective optimization algorithm to
solve the problem efficiently and make the algorithm adaptable to the changes in
input parameters that instantiate this problem.

The algorithm to solve the optimization problem is a hybrid system that uses
brute force optimization when there are less than ten technologies; otherwise,
it uses a Non-dominated Sorting Genetic Algorithm (i.e., `NSGA-II` implemented
by the library `pymoo`) with a default termination criteria. This approach is
very "fast" since every optimization requires about 20 seconds. Moreover, its
implementation on average requires 200Mb of RAM per optimization process, making
the code suitable to run on a normal personal computer.

Parameter Transformation
************************
Once a set of Pareto-optimal technology packages has been found for a given
year (i.e powertrain, vehicle segment, and cost scenario), some adjustments are
made to each point before fitting the cost curve. These transformations are needed
for:

- Baseline adjustment: Accounting for technologies that are already deployed in
  the reference year,
- Scaling for batteries: Handling battery cost (or |H2| storage cost) savings
  for `xEV`,
- Scaling for overlapping technologies: Avoiding that potentials covered by
  different technologies are double-counted, and
- Re-baseline `xEV`: setting `xEV` energy and |CO2| savings relative to
  reference year conventional vehicles.

These steps and their relative algorithms are described in a previous
`report <https://ec.europa.eu/clima/system/files/2017-11/ldv_co2_technologies_and_costs_to_2030_en.pdf>`_.

Optimal Pareto Front
********************
The raw Pareto cloud/front found in the previous step indicates the best
technology combinations at the vehicle level. Still, it is not the optimal
solution used at the fleet level.
A reasonable solution to reduce technology cost is a linear combination of two
technology packages for cost curves used at the fleet level. For example, if we
have 100 vehicles with package A and 100 with package B, the result at fleet
level is equal to the average point of |CO2| emissions reduction and the
implementation cost between the two packages. Hence, the optimal Pareto front
(the optimal packages' distribution) is defined in a discrete form by a series
of segments.

The optimal Pareto fronts are useful input for applications such as the
evaluation of different |CO2| reduction scenarios, e.g., for calculating the
costs associated with a certain |CO2| reduction target for vehicles, identifying
cost-minimizing distributions of |CO2| reduction efforts across different
vehicle types and technologies, and identifying maximum feasible |CO2|
reductions.

The `convex hull` algorithm implemented by the `scipy` library is used for
finding the optimal points that define the linear front from the raw Pareto
cloud.

Fitting Cost Curves
*******************
A continuous analytical form of the cost curves can be fitted based on the raw
Pareto cloud or the optimal Pareto front. Several functional forms of fitting
functions were tested, with the requirement for the fit to have a non-negative
second derivative. The functional form showing the required behavior is the
following:

.. math::

    y = Ax^2 + Bx + C + \frac{c}{x-x0}

where `A`, `B`, `C`, `c`, and `x0` are the unknown parameters to be fitted, and
`y` and `x` represent the implementation technology cost and the relative |CO2|
reduction.

The DIONE model allows fixing some or all unknown parameters and defines cost
curves distinguished by their fitting methods. The curves are:

- `cloud cost curve`: fitted using the raw Pareto cloud, and
- `optimal cost curve`: fitted using 1000 equally distributed points of the
  optimal Pareto front.

.. note:: The `optimal cost curve` is more stable because the raw Pareto cloud
   does not influence it.

The fitting algorithm used for fitting the parameters of the curves is an
adaptive multi-step algorithm that uses:

1. the Nelder method to solve non-linear least squares problem fixing
   :math:`x0=1` and using all other parameters equal to zero as initial guess,
2. the Nelder method using the previous solution as initial guess,
3. the Least-Squares minimization, using Trust Region Reflective method and the
   previous solution as initial guess.

Cross Optimization and Energy Consumption
-----------------------------------------
The DIONE Cross-Optimization Module is developed to determine the
cost-minimizing distribution of |CO2| and energy consumption reduction overall
powertrains and segments, given a |CO2| reduction target and fleet composition
scenario and the cost curves described above. The diagram below shows the
procedural steps that the tool is performing.

.. dispatcher:: cross_opt
   :height: 600px
   :opt: index=True, body={'label': '"Cross Optimization and Energy Consumption Model"'}

    >>> from dione.model.cross_opt import dsp as cross_opt
    >>> cross_opt = cross_opt.register()

The cost curves have positive first and second derivatives; this is a
mathematical problem with a unique solution. While transport and energy system
models operate at the fleet level, |CO2| targets need to be met at the
manufacturer or manufacturer group level.
Cross-optimization is thus developed to be feasible for subsets of the total
fleet.

The problem consists in finding the :math:`x_{i,m}` minimizing the overall
costs, respecting the |CO2| targets. Analytically, the cross-optimization
problem is formulated as follows:

.. math::

    min \quad C_{m,s} &= \sum_{i} p_{i,m,s} \cdot c_{i,m}(x_{i,m,s})\\
    s.t. \quad CO_{2\ m,s} &= \sum_{i} p_{i,m,s} \cdot CO_{2\ ref\ i,m,s}\cdot (1 - x_{i,m,s}) \leq CO_{2\ target\ m,s}\\

where :math:`C_{m,s}`, :math:`CO_{2\ m,s}`, and :math:`CO_{2\ target\ m,s}` are
the total cost, the total |CO2| emission and the |CO2| emission target for each
manufacturer :math:`m` and scenario :math:`s`; while :math:`p_{i,m,s}`,
:math:`x_{i,m,s}`, :math:`CO_{2\ ref\ i,m,s}`, and :math:`c_{i,m}` are
relatively the share, the |CO2| reduction, the reference |CO2| emission, and the
cost curve associated to each segment-powertrain for at each registration year
that belongs to a specific manufacturer and scenario.

The module uses the `Particle Swarm Optimization <https://pymoo.org/algorithms/soo/pso.html>`_
algorithm (i.e., PSO) to find the optimal points. Moreover, to improve the speed
performance, the algorithm reduces the cost curve solution space removing all
points with |CO2| reduction lower than the |CO2| reduction at minimum cost.

The conventional (:math:`EC_{i,m,s}`) and electric (:math:`EE_{i,m,s}`) energy
consumptions are calculated according to the following equations:

.. math::

    EC_{i,m,s} &= EC_{ref\ i,m,s}\cdot (1 - x_{i,m,s})\\
    EE_{i,m,s} &= EE_{ref\ i,m,s}\cdot (1 - x_{i,m,s})

where :math:`EC_{ref\ i,m,s}` and :math:`EE_{ref\ i,m,s}` are the reference
energy consumptions relative to the conventional and electric consumption.

Total Cost of Ownership
-----------------------
The DIONE total cost of ownership (TCO) module is designed to summarize the
different cost types over different time frames, thus assessing the economic
impacts of policy options from the perspective of vehicle end-users and society.
The diagram below shows the procedural steps that the tool is performing.

.. dispatcher:: tco
   :height: 600px
   :opt: index=True, body={'label': '"Total Cost of Ownership Model"'}

    >>> from dione.model.tco import dsp as tco
    >>> tco = tco.register()

The TCO (i.e., :math:`TotalCost`) is calculated as follows:

.. math::

    TotalCost = EnCost + OMCost + TechCost

where :math:`EnCost` is the total fuel and energy cost, :math:`OMCost` is the
operation and maintenance cost, and :math:`TechCost` is the manufacturing cost.
These parameters will be explained in the following sections.

Total Fuel and Energy Cost
**************************
Total fuel and energy cost (:math:`EnCost_{i,m,s,age}`) is calculated as the sum
over specific energy consumption times mileage times costs for each fuel type a
vehicle consumes. Indices for vehicle `age` and `projection_year` are introduced
to trace energy costs over the vehicle's lifetime, as vehicle activity varies
with its `projection_year`. Moreover, the `projection_year` index refers to the
energy costs in a given year. The `projection_year` and the `registration_year`
difference compute the index `age`. Thus, the two indices are equivalent.
Analytically, the total fuel and energy cost per vehicle type is calculated as
follows:

.. math::

    EnCost_{i,m,s,age} = EC_{i,m,s}\cdot MC_{i,m,s,age}\cdot Cost\_CE_{i,m,s,projection\_year} \\
    + EE_{i,m,s}\cdot ME_{i,m,s,age}\cdot Cost\_EE_{i,m,s,projection\_year}

where :math:`MC_{i,m,s,age}` and :math:`ME_{i,m,s,age}` are the mileage driven
as conventional and in electric mode; :math:`Cost\_CE_{i,m,s,projection\_year}`
is a parameter proportional to the fuel cost; and
:math:`Cost\_EE_{i,m,s,projection\_year}` is the energy cost.

Operation and Maintenance cost
******************************
Operation and maintenance costs (:math:`OMCost_{i,m,s,age}`) are
calculated as their cost plus VAT. The formula is the following:

.. math::

    OMCost_{i,m,s,age} = OM\_Base\_Cost_{i,m,s,age}\cdot (1 + OM\_VAT_{i,m,s,age})

where :math:`OM\_Base\_Cost_{i,m,s,age}` is the base maintenance cost without
VAT, and :math:`OM\_VAT_{i,m,s,age}` is the relative cost VAT.

Manufacturing cost
******************
Manufacturing costs (:math:`TechCost_{i,m,s,age}`) are based on the
Cross-Optimization calculations, i.e. the technology implementation cost. The
latter is augmented by a manufacturer margin factor
(:math:`TechMargin_{i,m,s,age}`) and distributed throughout the vehicle's
lifetime with a residual factor (:math:`TechResidual_{i,m,s,age}`) to consider
the manufacturing depreciation. Follows the formula to calculate the
manufacturing cost:

.. math::

    TechCost_{i,m,s,age} = c_{i,m}(x_{i,m,s})\cdot (1 - TechResidual_{i,m,s,age})\cdot TechMargin_{i,m,s,age}

.. _end-model:


.. _start-badges:
.. |travis_status| image:: https://travis-ci.org/JRCSTU/dione.svg?branch=master
    :alt: Travis build status
    :target: https://travis-ci.org/JRCSTU/dione

.. |cover_status| image:: https://coveralls.io/repos/github/JRCSTU/dione/badge.svg?branch=master
    :target: https://coveralls.io/github/JRCSTU/dione?branch=master
    :alt: Code coverage

.. |docs_status| image:: https://readthedocs.org/projects/dione/badge/?version=stable
    :alt: Documentation status
    :target: https://dione.readthedocs.io/en/stable/?badge=stable

.. |pypi_ver| image:: https://img.shields.io/pypi/v/dione.svg?
    :target: https://pypi.python.org/pypi/dione/
    :alt: Latest Version in PyPI

.. |python_ver| image:: https://img.shields.io/pypi/pyversions/dione.svg?
    :target: https://pypi.python.org/pypi/dione/
    :alt: Supported Python versions

.. |github_issues| image:: https://img.shields.io/github/issues/JRCSTU/dione.svg?
    :target: https://github.com/JRCSTU/dione/issues
    :alt: Issues count

.. |proj_license| image:: https://img.shields.io/badge/license-EUPL%201.1%2B-blue.svg?
    :target: https://raw.githubusercontent.com/JRCSTU/dione/master/LICENSE.txt
    :alt: Project License

.. |dependencies| image:: https://img.shields.io/requires/github/JRCSTU/dione.svg?
    :target: https://requires.io/github/JRCSTU/dione/requirements/?branch=master
    :alt: Dependencies up-to-date?
.. _end-badges:

.. _start-sub:
.. |CO2| replace:: CO\ :sub:`2`
.. |H2| replace:: H\ :sub:`2`
.. _end-sub: