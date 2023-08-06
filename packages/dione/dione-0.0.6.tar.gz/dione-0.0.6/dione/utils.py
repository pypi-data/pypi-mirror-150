# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
It provides some utils for models definitions.
"""
import os
import ray
import yaml
import hashlib
import schedula as sh
import os.path as osp
from schedula.utils.imp import Future

VERBOSE = os.environ.get('DIONE_VERBOSE', 'false').lower() == 'true'


class DummyExecutor(sh.ThreadExecutor):
    """
    Defines a Dummy parallel Executor.
    """

    def submit(self, func, *args, **kwargs):
        fut = Future()
        self.tasks[fut] = None
        self._target(lambda x: self._set_future(fut, x), func, args, kwargs)
        return fut


@ray.remote
def ray_exec(func, args, kwargs):
    return func(*args, **kwargs)


class RayTask:
    """
    Defines a Ray Task for shutdown the remote process.
    """

    def __init__(self, task, actor):
        self.task = task
        self.actor = actor

    def terminate(self):
        ray.kill(self.actor)
        try:
            self.task.terminate()
        except AttributeError:
            pass


class RayExecutor(sh.ThreadExecutor):
    """
    Defines a Ray parallel Executor.
    """

    def __init__(self, config=None, pool=None):
        super(RayExecutor, self).__init__()
        self.config = config or {}
        self.pool = pool

    def init(self):
        not ray.is_initialized() and ray.init(**self.config)
        if self.pool is None:
            from concurrent.futures import ThreadPoolExecutor
            self.pool = ThreadPoolExecutor(ray.available_resources().get(
                'CPU', 100
            ) * 2 + 4)

    def submit(self, func, *args, **kwargs):
        self.init()
        actor = ray_exec.remote(func, args, kwargs)
        fut, send = Future(), lambda res: self._set_future(fut, res)
        self.pool.submit(self._target, send, ray.get, (actor,), {})
        self.tasks[fut] = RayTask(None, actor)
        return fut


class CacheExecutor:
    def __init__(self, executor, path=None):
        self.executor = executor
        self.running = {}
        self.path = path or os.environ.get(
            'DIONE_CACHE', osp.join(osp.dirname(__file__), '.cache')
        )

    def save_res(self, fpath, fut):
        self.running.pop(fpath, None)
        try:
            res = fut.result()
        except Exception:
            return
        os.makedirs(osp.dirname(fpath), exist_ok=True)
        with open(fpath, 'w') as f:
            yaml.dump(res, f, Dumper=yaml.CDumper)

    @staticmethod
    def load_res(fpath):
        with open(fpath, 'r') as f:
            res = yaml.load(f, Loader=yaml.CLoader)
            if res is not None:
                fut = Future()
                fut.set_result(res)
                return fut

    def submit(self, func, *args, **kwargs):
        fpath = osp.join(self.path, func.__name__, '%s.yaml' % (
            hashlib.sha512(yaml.dump(
                (args, kwargs), sort_keys=True
            ).encode()).hexdigest()
        ))
        fut = None
        if osp.isfile(fpath):
            fut = self.load_res(fpath)
        fut = fut or self.running.get(fpath, None)
        if not fut:
            self.running[fpath] = fut = self.executor.submit(
                func, *args, **kwargs
            )
            fut.add_done_callback(lambda res: self.save_res(fpath, res))
        return fut
