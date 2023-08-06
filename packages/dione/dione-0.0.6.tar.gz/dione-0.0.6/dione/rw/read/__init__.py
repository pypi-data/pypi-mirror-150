# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It contains functions and a model `dsp` to read input files.
Sub-Modules:

.. currentmodule:: dione.rw.read

.. autosummary::
    :nosignatures:
    :toctree: read/

    excel
    parse
"""
import io
import xlref
import zipfile
import numpy as np
import os.path as osp
import schedula as sh
from .. import file_ext
from .parse import dsp as _parse

valid_extensions = [k for k in xlref.Ref._engines if k] + ['json']
#: Read Model.
dsp = sh.BlueDispatcher(name='read_data', raises=True)


@sh.add_function(dsp, outputs=['input_file'])
def read_file(input_fpath):
    """
    Load the input data as BinaryIO.

    :param input_fpath:
        Input file path.
    :type input_fpath: str

    :return:
        Input data as BinaryIO.
    :rtype: io.BytesIO
    """
    with open(input_fpath, 'rb') as f:
        return io.BytesIO(f.read())


# noinspection PyUnusedLocal
@sh.add_function(dsp, outputs=['raw_data'], input_domain=file_ext('bz2'))
def load_zip_data(input_fpath, input_file):
    """
    Load the input data as ZIP format.

    :param input_fpath:
        Input file path.
    :type input_fpath: str

    :param input_file:
        Input data as BinaryIO.
    :type input_file: io.BinaryIO

    :return:
        Raw Data.
    :rtype: dict
    """
    input_file.seek(0)
    import pyarrow.feather as feather
    res = {}
    with zipfile.ZipFile(input_file, compression=zipfile.ZIP_BZIP2) as z:
        for name in z.namelist():
            with z.open(name, mode='r') as f:
                if name == 'inputs':
                    import json
                    res.update(json.load(f))
                else:
                    df = feather.read_feather(f)
                    res[name] = np.append([df.columns], df.to_numpy(), axis=0)
    return res


# noinspection PyUnusedLocal
@sh.add_function(dsp, outputs=['raw_data'], input_domain=file_ext('json'))
def load_json_data(input_fpath, input_file):
    """
    Load the input data as JSON format.

    :param input_fpath:
        Input file path.
    :type input_fpath: str

    :param input_file:
        Input data as BinaryIO.
    :type input_file: io.BinaryIO

    :return:
        Raw Data.
    :rtype: dict
    """
    import json
    input_file.seek(0)
    return json.load(input_file)


@sh.add_function(
    dsp, outputs=['xlsx'],
    input_domain=file_ext(*(k for k in xlref.Ref._engines if k))
)
def load_xlsx(input_fpath, input_file):
    """
    Load the input data as JSON format.

    :param input_fpath:
        Input file path.
    :type input_fpath: str

    :param input_file:
        Input data as BinaryIO.
    :type input_file: io.BinaryIO

    :return:
        Excel File.
    :rtype: pandas.ExcelFile
    """
    import pandas as pd
    ext = osp.splitext(input_fpath.lower())[1][1:]
    engine = xlref.Ref._engines.get(ext, xlref.Ref._engines[None])
    input_file.seek(0)
    xl = pd.ExcelFile(io.BytesIO(input_file.read()), engine=engine)
    xl.sheet_indices = {k.lower(): i for i, k in enumerate(xl.sheet_names)}
    return xl


@sh.add_function(dsp, outputs=['raw_data'])
def load_xlsx_data(input_fpath, xlsx):
    """
    Load the input data as JSON format.

    :param input_fpath:
        Input file path.
    :type input_fpath: str

    :param xlsx:
        Excel File.
    :type xlsx: pandas.ExcelFile

    :return:
        Raw Data.
    :rtype: dict
    """
    from .excel import xlref
    ref = '%s#Inputs!B2:C_[{"fun": "dict", "value": "ref"}]' % osp.basename(
        input_fpath
    )
    parent = xlref.Ref('#A1')
    input_fpath = osp.abspath(input_fpath)
    parent.ref['fpath'] = input_fpath
    parent.cache[input_fpath] = parent.ref['xl_book'] = xlsx
    parent.cache.update({
        (xlsx, k): v.values
        for k, v in xlsx.parse(
            None, convert_float=False, **xlref.Ref._open_sheet_kw
        ).items()
    })
    return xlref.Ref(ref, parent=parent, cache=parent.cache).values


dsp.add_function(function=sh.SubDispatchFunction(
    _parse, 'parse_data', ['raw_data'], ['inputs']
), inputs=['raw_data'], outputs=['inputs'])
