# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import os
import re
import time
import threading
import subprocess
import os.path as osp
from .db import DatabaseConnector
from .config import conf
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()
processes = {}
lock = threading.Lock()
_re_version = re.compile(r'version\s*(\d+\.\d+\.\d+)')


def get_dione_version():
    out = subprocess.run(["dione", "--version"], capture_output=True).stdout
    return _re_version.search(out.decode()).group(1)


def update_runs(process, conn):
    if 'process' in process:
        returncode = process['process'].returncode
        if returncode == 0:
            status, output = statuses['COMPLETED'], process['output']
        elif returncode is None:
            status, output = statuses['RUNNING'], None
        else:
            status, output = statuses['ERROR'], None
    else:
        status, output = process['status'], process['output']
    conn.cursor.execute(
        "UPDATE runs "
        "SET status=%s, output=%s, log=%s, dione_version=%s "
        "WHERE hash=%s AND action=%s AND "
        "(status=%s OR status=%s) AND "
        "(dione_version=%s OR dione_version IS NULL)",
        (status, output, process['log'], process['version'], process['name'],
         actions['RUN'], statuses['RUNNING'], statuses['PENDING'],
         process['version'])
    )
    conn.cnx.commit()


def cmd_run(process_id, name, version=None, parallel=False):
    logs, dione_version = "{}.txt".format(process_id), None
    os.makedirs(conf['cron']['logs_folder'], exist_ok=True)
    if version is None:
        dione_version = get_dione_version()
    version = version or dione_version
    process_k = actions['RUN'], name, version
    oname = '{}-{}.xlsx'.format(version, name)
    with lock, DatabaseConnector() as conn:
        if process_k in processes:
            update_runs(processes[process_k], conn)
            return
        process = processes[process_k] = {
            'id': process_id, 'output': oname, 'log': None,
            'name': name, 'version': version
        }
        if osp.isfile(osp.join(conf['cron']['outputs_folder'], oname)):
            process['status'] = statuses['COMPLETED']
        else:
            stdout = open(osp.join(conf['cron']['logs_folder'], logs), "w")
            process['log'] = logs
            process['version'] = dione_version or get_dione_version()
            process['output'] = oname = '{}-{}.xlsx'.format(
                process['version'], name
            )
            print('running', process_k)
            args = [
                "dione", "run",
                osp.join(conf['cron']['inputs_folder'], '%s.xlsx' % name),
                '-o', osp.join(conf['cron']['outputs_folder'], oname)
            ]
            if parallel:
                args.append('-p')
            process['process'] = subprocess.Popen(
                args, stdout=stdout, stderr=stdout
            )

    if 'process' in process:
        process['process'].wait()
        print('done', process_k)

    with lock, DatabaseConnector() as conn:
        update_runs(processes.pop(process_k, None), conn)


actions = {
    'RUN': 1,
    'EXTRACTION': 2,
    'SAVE': 3
}
statuses = {
    'PENDING': 1,
    'RUNNING': 2,
    'ABORT': 3,
    'ERROR': 4,
    'COMPLETED': 5,
    'DELETED': 6
}


def run_step(parallel=True):
    with lock and DatabaseConnector() as conn:
        # UPDATE RUNNING/COMPLETED/ERROR
        for k, v in processes.items():
            if k[0] == actions['RUN']:
                update_runs(v, conn)
        process = {'version': get_dione_version()}
        conn.cursor.execute(
            "SELECT hash, min(id), dione_version FROM runs "
            "WHERE action=%s AND (status=%s OR status=%s) AND "
            "(dione_version=%s OR dione_version IS NULL) "
            "GROUP BY hash",
            (actions['RUN'], statuses['RUNNING'], statuses['PENDING'],
             process['version'])
        )
        for name, process_id, version in conn.cursor.fetchall():
            process['name'] = name
            conn.cursor.execute(
                "SELECT status, output, log FROM runs "
                "WHERE hash=%s AND action=%s AND "
                "(status=%s OR status=%s) AND dione_version=%s "
                "LIMIT 1",
                (process['name'], actions['RUN'], statuses['COMPLETED'],
                 statuses['ERROR'], process['version'])
            )
            match = conn.cursor.fetchone()
            if match and osp.isfile(
                    osp.join(conf['cron']['outputs_folder'], match[1])):
                process['status'], process['output'], process['log'] = match
                update_runs(process, conn)
            elif (actions['RUN'], name, version) not in processes:
                executor.submit(cmd_run, process_id, name, version, parallel)
        if processes:
            # ABORT RUN
            conn.cursor.execute(
                "UPDATE runs SET dione_version=%s "
                "WHERE status=%s AND dione_version IS NULL",
                (process['version'], statuses['ABORT'])
            )
            conn.cursor.execute(
                "SELECT runs.action, runs.hash, runs.dione_version "
                "FROM runs, ("
                "   SELECT hash, dione_version "
                "   FROM runs WHERE action=%s AND status=%s"
                ") AS aborts "
                "WHERE runs.action=%s "
                "AND runs.hash=aborts.hash AND "
                "(runs.dione_version=aborts.dione_version) AND "
                "(runs.status=%s OR runs.status=%s OR runs.status=%s)"
                "GROUP BY runs.hash, runs.dione_version "
                "HAVING count(DISTINCT(runs.status))=1",
                (actions['RUN'], statuses['ABORT'], actions['RUN'],
                 statuses['ABORT'], statuses['RUNNING'], statuses['PENDING'])
            )
            for k in conn.cursor.fetchall():
                if k in processes:
                    p = processes.pop(k).get('process')
                    if p:
                        p.terminate()
                        print('killed', k)
        conn.cnx.commit()


if __name__ == '__main__':
    while True:
        time.sleep(1)
        run_step()
