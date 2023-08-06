#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2021-2022 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import io
import os
import collections
import os.path as osp

name = 'dione'
mydir = osp.dirname(__file__)


# Version-trick to have version-info in a single place,
# taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-
# version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version(what='__version__'):
    fglobals = {}
    with io.open(osp.join(mydir, name, '_version.py'), encoding='UTF-8') as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals[what]


# noinspection PyPackageRequirements
def get_long_description(cleanup=False):
    from sphinx.application import Sphinx
    from sphinx.util.osutil import abspath
    import tempfile
    import shutil
    from doc.conf import extensions
    from sphinxcontrib.writers.rst import RstTranslator
    from sphinx.ext.graphviz import text_visit_graphviz
    RstTranslator.visit_dsp = text_visit_graphviz
    outdir = tempfile.mkdtemp(prefix='setup-', dir='.')
    exclude_patterns = os.listdir(mydir or '.')
    exclude_patterns.remove('pypi.rst')

    # noinspection PyTypeChecker
    app = Sphinx(
        abspath(mydir), osp.join(mydir, 'doc/'), outdir, outdir + '/.doctree',
        'rst', status=None, warning=None, confoverrides={
            'exclude_patterns': exclude_patterns,
            'master_doc': 'pypi',
            'dispatchers_out_dir': abspath(outdir + '/_dispatchers'),
            'extensions': extensions + ['sphinxcontrib.restbuilder']
        }
    )

    app.build(filenames=[osp.join(app.srcdir, 'pypi.rst')])

    with open(outdir + '/pypi.rst') as file:
        res = file.read()

    if cleanup:
        shutil.rmtree(outdir)
    return res


proj_ver = read_project_version()
url = 'https://github.com/JRCSTU/%s' % name
download_url = '%s/tarball/v%s' % (url, proj_ver)
project_urls = collections.OrderedDict((
    ('Documentation', read_project_version('__documentation__')),
    ('Issue tracker', '%s/issues' % url),
))
if __name__ == '__main__':
    import functools
    from setuptools import setup, find_packages

    long_description = ''
    if os.environ.get('ENABLE_SETUP_LONG_DESCRIPTION') == 'TRUE':
        try:
            long_description = get_long_description()
            print('LONG DESCRIPTION ENABLED!')
        except Exception as ex:
            print('LONG DESCRIPTION ERROR:\n %r', ex)

    extras = {
        'cli': ['click', 'click-log'],
        'plot': [
            'flask', 'regex', 'graphviz', 'requests', 'Pygments', 'jinja2',
            'docutils'
        ],
        'gui': [
            'dash', 'dash-bootstrap-components', 'plotly'
        ],
        'parallel': ['ray[default]']
    }
    extras['gui'] += extras['plot']
    # noinspection PyTypeChecker
    extras['all'] = sorted(functools.reduce(set.union, extras.values(), set()))
    extras['dev'] = extras['all'] + [
        'wheel', 'sphinx', 'gitchangelog', 'mako', 'sphinx_rtd_theme', 'ddt',
        'sphinxcontrib-restbuilder', 'nose', 'coveralls', 'sphinx-click',
        'pyinstaller'
    ]

    setup(
        name=name,
        version=proj_ver,
        packages=find_packages(exclude=[
            'tests', 'tests.*', 'doc', 'doc.*', 'requirements', 'compose',
            'data', 'docker'
        ]),
        url=url,
        project_urls=project_urls,
        download_url=download_url,
        license='EUPL 1.1+',
        author='Vincenzo Arcidiacono',
        author_email='vinci1it2000@gmail.com',
        description='DIONE tool.',
        long_description=long_description,
        keywords=[
            "python", "utility", "library", "fleet", "fuel", "scientific",
            "engineering", "forecast"
        ],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: CPython",
            "Development Status :: 5 - Production/Stable",
            'Natural Language :: English',
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: European Union Public Licence 1.1 "
            "(EUPL 1.1)",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
        ],
        install_requires=[
            'numpy<=1.19.3',
            'pandas',
            'lmfit',
            'scipy',
            'schedula>=1.2.4',
            'xlref',
            'openpyxl',
            'pymoo>=0.5.0',
            'tqdm',
            'pyarrow'
        ],
        entry_points={
            'console_scripts': [
                '%(p)s = %(p)s.cli:cli' % {'p': name},
            ],
        },
        package_data={
            name: [
                'demos/*.xlsx',
                'templates/*.xlsx',
                'assets/*',
                'cron/*.ini'
            ]
        },
        extras_require=extras,
        tests_require=['nose>=1.0', 'ddt', 'dill', 'matplotlib'],
        test_suite='nose.collector',
    )
