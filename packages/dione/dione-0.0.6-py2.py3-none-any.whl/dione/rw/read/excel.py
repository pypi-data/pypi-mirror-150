# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It contains functions to expand `xlref` parsing features.
"""
import xlref
from pandas.io.parsers import TextParser


def array2frame(x, **kw):
    return TextParser(x.tolist(), **kw).read()


# noinspection PyUnusedLocal
def dataframe(parent, x, **kw):
    return array2frame(x, **kw)


xlref.FILTERS['dataframe'] = dataframe
