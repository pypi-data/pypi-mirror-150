# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
Defines the file processing chain model `dsp`.

Sub-Modules:

.. currentmodule:: dione

.. autosummary::
    :nosignatures:
    :toctree: toctree/dione/

    model
    rw
    cli
    graph
    utils
"""
import glob
import os.path as osp
import schedula as sh
from dione._version import *
from dione import model
from dione.rw import read, write
from dione import graph

#: Processing Model.
dsp = sh.BlueDispatcher(name='Processing Model', raises=True)


@sh.add_function(dsp, True, True, outputs=['input_fs'])
def define_input_fs(input_fpaths=(), input_files=None):
    """
    Defines an input list for reading files.

    :param input_fpaths:
        Input file paths.
    :type input_fpaths: tuple[str]

    :param input_files:
        Input files.
    :type input_files: tuple[files]

    :return:
        Input list for reading files.
    :rtype: list[dict]
    """
    alist = []
    for v in input_fpaths:
        if osp.isdir(v):
            for p in glob.glob(osp.join(v, '*')):
                if osp.splitext(p)[1][1:].lower() in read.valid_extensions:
                    if not osp.basename(p).startswith('~'):
                        alist.append({'input_fpath': p})
        else:
            alist.append({'input_fpath': v})
    for i, v in enumerate(input_files or ()):
        alist[i]['input_file'] = v
    return alist


def merge_input_data(data):
    """
    Merges multiple input data into a single one.

    :param data:
        Data inputs.
    :type data: list[dict]

    :return:
        Input data.
    :rtype: dict
    """
    return sh.combine_dicts(*data)


dsp.add_function(
    function_id='read_input_data',
    function=sh.MapDispatch(read.dsp, constructor_kwargs={
        'outputs': ['inputs'], 'output_type': 'values'
    }),
    inputs=['input_fs'],
    outputs=['input_data'],
    filters=[merge_input_data],
    description='Reads input files.'
)


@sh.add_function(dsp, True, True, outputs=['executor'])
def define_executor(parallel=False):
    """
    Defines model inputs.

    :param parallel:
        Parallel execution configuration.
    :type parallel: bool|dict

    :return:
        Parallel executor.
    :rtype: schedula.utils.asy.executors.Executor
    """
    from .utils import DummyExecutor, RayExecutor, CacheExecutor
    if parallel is False:
        return CacheExecutor(DummyExecutor())
    elif parallel is True:
        parallel = {}
    return CacheExecutor(RayExecutor(parallel))


@sh.add_function(dsp, outputs=['inputs'])
def define_inputs(input_data, executor):
    """
    Defines model inputs.

    :param input_data:
        Input data from files.
    :type input_data: dict

    :param executor:
        Parallel executor.
    :type executor: schedula.utils.asy.executors.Executor

    :return:
        Model inputs.
    :rtype: dict
    """
    return sh.combine_dicts(input_data, {'executor': executor})


dsp.add_function(
    function=sh.SubDispatch(model.dsp), inputs=['inputs'], outputs=['outputs']
)
dsp.add_dispatcher(
    write.dsp,
    inputs=['outputs', 'output_fpath', 'template_fpath', 'demo_fpath'],
    outputs=['written', 'output_file', 'results', 'output_fpath']
)
dsp.add_function(
    function=sh.SubDispatch(graph.dsp),
    inputs=['outputs'],
    outputs=['graphs']
)

if __name__ == '__main__':
    dsp.register().plot(index=True)
