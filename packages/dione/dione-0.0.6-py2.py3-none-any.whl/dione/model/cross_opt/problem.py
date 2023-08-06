# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides the DIONE Cross Optimization problem.
"""
import numpy as np
from pymoo.core.problem import Problem as _Problem


class Problem(_Problem):
    """
    Defines the DIONE Cross Optimization problem.
    """

    def __init__(self, shares, factors, target, cost, **kw):
        self.cost = cost
        self.shares = shares
        self.limit = self.factors = None
        n_constr = target.size
        if n_constr:
            self.limit = np.sum(factors, axis=1) - target
            self.factors = factors.T[None, :, :]

        super(Problem, self).__init__(
            n_var=len(shares), n_obj=1, n_constr=n_constr, type_var=bool, **kw
        )

    # noinspection PyPep8Naming
    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = np.sum(self.cost(X) * self.shares, axis=1)[:, None]
        if self.limit is not None:
            out["G"] = self.limit - np.sum(X[:, :, None] * self.factors, axis=1)
