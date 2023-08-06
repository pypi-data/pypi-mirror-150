# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
r"""
Define the command line interface.

.. click:: dione.cli:cli
   :prog: dione
   :show-nested:

"""
import click
import logging
import click_log
import schedula as sh
import dione
from dione._version import __version__

log = logging.getLogger('dione.cli')


class _Logger(logging.Logger):
    def setLevel(self, level):
        super(_Logger, self).setLevel(level)
        frmt = "%(asctime)-15s:%(levelname)5.5s:%(name)s:%(message)s"
        logging.basicConfig(level=level, format=frmt)
        rlog = logging.getLogger()
        # because `basicConfig()` does not reconfig root-logger when re-invoked.
        rlog.level = level
        logging.captureWarnings(True)


logger = _Logger('cli')
click_log.basic_config(logger)
_process = dione.dsp


@click.group(
    'dione', context_settings=dict(help_option_names=['-h', '--help']),
    invoke_without_command=True
)
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    """
    dione command line tool.
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(gui)


@cli.command('template', short_help='Generates sample template file.')
@click.argument(
    'output-file', default='template.xlsx', required=False,
    type=click.Path(writable=True)
)
@click_log.simple_verbosity_option(logger)
def template(output_file='template.xlsx'):
    """
    Writes a sample template OUTPUT_FILE.

    OUTPUT_FILE: dione input template file (.xlsx). [default: ./template.xlsx]
    """
    return _process({'template_fpath': output_file}, ['written'])


@cli.command('model', short_help='Displays the model process.')
@click.option(
    '-o', '--output-dir', help='Output directory.',
    type=click.Path(writable=True, dir_okay=True)
)
@click_log.simple_verbosity_option(logger)
def model(output_dir=None):
    """
    Plots the model process.
    """
    # noinspection PyUnresolvedReferences
    return _process.register().plot(directory=output_dir, index=True)


@cli.command('demo', short_help='Generates a demo file.')
@click.argument(
    'output-file', default='demo.xlsx', required=False,
    type=click.Path(writable=True)
)
@click_log.simple_verbosity_option(logger)
def demo(output_file='demo.xlsx'):
    """
    Writes sample demo files into OUTPUT_FOLDER.

    OUTPUT_FOLDER: Folder path. [default: ./demo.xlsx]
    """
    return _process({'demo_fpath': output_file}, ['written'])


def _parse_kv(x):
    k, v = x.strip().split('=')
    return k, eval(v) if v.isdigit() or v in ('True', 'False') else v


@cli.command('run', short_help='Run model.')
@click.argument('input-file', type=click.Path(exists=True), nargs=-1)
@click.option(
    '-o', '--output-file', help='Output file.', default='output.xlsx',
    type=click.Path(writable=True), show_default=True
)
@click.option('--workflow', '-w', is_flag=True, help='Plot process workflow.')
@click.option('--parallel', '-p', is_flag=True, help='Parallel execution.')
@click.option(
    '--ray-config', '-r', multiple=True,
    type=click.types.FuncParamType(_parse_kv),
    help='Ray init configuration.')
@click_log.simple_verbosity_option(logger)
def run(input_file, output_file='output.xlsx', workflow=False, parallel=False,
        ray_config=None):
    """
    Run the model using the data defined into the INPUT_FILE.

    INPUT_FILE: Input file (format: .xlsx, .json).

    OUTPUT_FILE: Output file (format: .xlsx, .json).
    """
    # noinspection PyUnresolvedReferences
    func = _process.register()
    parallel, ray_shutdown = dict(ray_config) or (parallel and {}), False
    if isinstance(parallel, dict):
        import ray
        ray_shutdown = not ray.is_initialized()
    try:
        result = func({
            'input_fpaths': input_file, 'output_fpath': output_file,
            'parallel': parallel
        }, ['written'])
    except sh.DispatcherError as ex:
        log.exception(ex)
        result = func.solution

    if ray_shutdown:
        import ray
        ray.is_initialized() and ray.shutdown()
    import pandas as pd
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    if workflow:
        site = result.plot(index=True, view=False).site(view=True)
        import time
        while True:
            try:
                time.sleep(1)
            except KeyError:
                site.shutdown()
    assert output_file is sh.NONE or 'written' in result


@cli.command('gui', short_help='Open the gui.')
@click.option(
    '-H', '--host', help='Hostname to listen on.', default='127.0.0.1',
    type=str, show_default=True
)
@click.option(
    '-P', '--port', help='Port of the webserver.', default=5000, type=int
)
@click.option('--parallel', '-p', is_flag=True, help='Parallel execution.')
@click.option(
    '--ray-config', '-r', multiple=True,
    type=click.types.FuncParamType(_parse_kv),
    help='Ray init configuration.')
@click_log.simple_verbosity_option(logger)
def gui(host='127.0.0.1', port=0, parallel=False, ray_config=None):
    """
    Open the gui.
    """
    from dione.gui import GUI
    debug = logger.level == logging.DEBUG
    parallel, ray_shutdown = dict(ray_config) or (parallel and {}), False
    if isinstance(parallel, dict):
        import ray
        ray_shutdown = not ray.is_initialized()
        ray_shutdown and ray.init(**parallel)

    site = GUI(host=host, port=port, inputs={'parallel': parallel})
    if debug:
        from dione.gui import app
        app.inputs = site.inputs
        app.run_server(**site.get_port(debug=True))
    else:
        import webbrowser
        site.run()
        webbrowser.open(site.url)
        import time
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            pass
        site.shutdown()

    if ray_shutdown:
        import ray
        ray.is_initialized() and ray.shutdown()


@cli.command('cron', short_help='Run cron.')
@click.option('--parallel', '-p', is_flag=True, help='Parallel execution.')
@click.option(
    '--ray-config', '-r', multiple=True,
    type=click.types.FuncParamType(_parse_kv),
    help='Ray init configuration.')
@click_log.simple_verbosity_option(logger)
def cron(parallel=False, ray_config=None):
    """
    Open the gui.
    """
    parallel, ray_shutdown = dict(ray_config) or (parallel and {}), False
    if isinstance(parallel, dict):
        import ray
        ray_shutdown = not ray.is_initialized()
        ray_shutdown and ray.init(**parallel)
    from dione.cron import run_step
    import time
    try:
        while True:
            time.sleep(1)
            run_step(parallel)
    except (KeyboardInterrupt, SystemExit):
        pass

    if ray_shutdown:
        import ray
        ray.is_initialized() and ray.shutdown()


if __name__ == '__main__':
    cli()
