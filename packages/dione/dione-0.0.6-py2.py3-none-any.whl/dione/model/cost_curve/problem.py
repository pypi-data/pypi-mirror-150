# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides the DIONE Cost Curve Pareto problem.
"""
import numpy as np
from pymoo.core.problem import Problem as _Problem
from pymoo.core.repair import Repair as _Repair


class Repair(_Repair):
    """
    Repairs the individual solutions according to the incompatibility matrix.
    """

    def __init__(self, incompatibilities):
        super(Repair, self).__init__()
        self.incompatibilities = incompatibilities

    # noinspection PyPep8Naming
    def _do(self, problem, pop, **kwargs):
        inc = self.incompatibilities
        if inc:
            X = pop.get("X")
            for x in X:
                it = np.where(x)[0]
                np.random.shuffle(it)
                case = set(it)
                for i in it:
                    if i in inc and inc[i].intersection(case):
                        x[i] = False
                        case.remove(i)
            pop.set("X", X)
        return pop


class Problem(_Problem):
    """
    Defines the DIONE Cost Curve Pareto problem.
    """

    def __init__(self, reduction_tech_cost, **kwargs):
        n_techs, _ = reduction_tech_cost.shape
        self.reduction_tech_cost = reduction_tech_cost[:, None, :].T

        super(Problem, self).__init__(
            n_var=n_techs,
            n_obj=2,
            type_var=bool,
            **kwargs
        )

    # noinspection PyPep8Naming
    def _evaluate(self, X, out, *args, **kwargs):
        r, c = X * self.reduction_tech_cost
        f1 = np.sum(c, where=X, axis=1)
        f2 = np.prod(r, where=X, axis=1)
        out["F"] = np.column_stack([f2, f1])
