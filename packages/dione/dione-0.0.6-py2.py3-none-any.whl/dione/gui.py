# -*- coding: utf-8 -*-
#
# Copyright 2021-2022 European Commission (JRC)
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
r"""
Defines the GUI.
"""
import io
import os
import dash
import json
import base64
import logging
import datetime
import tempfile
import traceback
import schedula as sh
import os.path as osp
from dash import dcc, html
from flask import send_file, request
import dash_bootstrap_components as dbc
from schedula.utils.drw import Site, basic_app
from dash.dependencies import Input, Output, State
from ._version import __version__, __title__, __documentation__
from .graph import __graphs__

log = logging.getLogger(__name__)
VERBOSE = os.environ.get('DIONE_VERBOSE', 'false').lower() == 'true'
server = basic_app(tempfile.mkdtemp())
ODIR = os.environ.get('DIONE_OUTPUTS', '')
if ODIR:
    @server.route('/outputs/<path:path>')
    def send_outputs(path):
        return send_file(
            open(osp.join(ODIR, path), 'rb'), as_attachment=True,
            attachment_filename=osp.basename(path)
        )

app = dash.Dash(
    assets_folder=osp.abspath(osp.join(osp.dirname(__file__), 'assets')),
    title=__title__, server=server
)

tabs = dbc.Tabs([
    dbc.Tab(dcc.Loading(html.Div(
        [dcc.Graph(id=k)], id='%s-container' % k
    )), **v) for k, v in __graphs__.items()
])
navbar = dbc.Navbar([
    dbc.NavbarBrand(__title__, className="ml-2 mr-1"),
    html.Sub(__version__, className="navbar-brand", style={
        "font-size": "small", "padding-bottom": 0
    }),
    dbc.Nav([
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem([
                    html.A(
                        "Template", href="templates/input_template.xlsx",
                        className='dropdown-item', id='template-link'
                    ),
                    dbc.Tooltip(
                        "Download the Input Template File",
                        target="template-link"
                    )
                ]),
                dbc.DropdownMenuItem([
                    html.A(
                        "Demo", href="demos",
                        className='dropdown-item',
                        id='demos-link'
                    ),
                    dbc.Tooltip("Download Demo Files", target="demos-link")
                ])
            ],
            nav=True,
            in_navbar=True,
            label="Downloads"),
        dbc.NavItem(dbc.NavLink("Documentation", href=__documentation__))
    ], className='navbar-nav')
], color='dark', light=False, dark=True)
style_base = {
    'width': '100%',
    'marginTop': '.2rem',
    'textAlign': 'center'
}
style_upload = sh.combine_dicts(style_base, {
    'borderWidth': '1px',
    'marginTop': '1rem',
    'borderStyle': 'dashed',
    'height': '60px',
    'lineHeight': '60px',
    'borderRadius': '5px',
    'cursor': 'pointer'
})
run_button = dbc.Button(
    ['Run Simulation'], id='run-button', color='primary', style=style_base
)
graph_button = dbc.Button(
    ['Render Graphs'], id='graph-button', color='primary',
    style=style_base if __graphs__ else {'display': 'none'}
)


def _json_default(o):
    if hasattr(o, 'to_plotly_json'):
        return o.to_plotly_json()
    return o


input_upload = dcc.Upload(
    id='upload-input-file',
    children=[
        html.Div(
            'Upload Input Files',
            id='upload-input-file-text'
        ),
        dbc.Tooltip(
            "Drag and Drop or Select Input Files",
            target="upload-input-file-text"
        )
    ],
    style=style_upload,
    multiple=True
)

app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([input_upload], id='upload-input-file-container'),
            dbc.Col([html.H3('OR', style=style_base)], md=1),
            dbc.Col(dcc.Loading([dcc.Upload(
                id='upload-output-file',
                children=[
                    html.Div(
                        'Upload Output File', id='upload-output-file-text'
                    ),
                    dbc.Tooltip(
                        "Drag and Drop or Select Output File",
                        target="upload-output-file-text"
                    )
                ],
                style=style_upload,
                multiple=False
            )], id='running'))
        ], align='center'),
        dbc.Row([
            dbc.Col([html.Div([dbc.ListGroup([dbc.ListGroupItem([dbc.Button(
                ["Show Input Files"], id='show-input-button',
                color='secondary', size="sm", style=style_base
            )], style={"padding": 0, "border-style": "hidden"})]), dbc.Collapse(
                id='input-file-list-collapse', children=dbc.ListGroup(
                    id='input-file-group'
                )
            )], id='input-file-list', hidden=True)], style=style_base),
            dbc.Col(md=1),
            dbc.Col([
                html.Div(dbc.ListGroup(
                    id='output-file-group'
                ), id='output-file-list', hidden=True),
                dbc.Tooltip(
                    "Click to download the Output File",
                    target="output-file-list"
                )
            ], style=style_base)
        ], align='center'),
        dbc.Row([
            dbc.Col(html.Div(
                [run_button], id='run-button-container', hidden=True
            )),
            dbc.Col(md=1),
            dbc.Col(html.Div(
                [graph_button], id='graph-button-container', hidden=True
            )),
        ], align='center'),
        html.Div(
            [tabs], id='graph-container', hidden=True,
            style=sh.combine_dicts(style_base, {'marginTop': '1rem'})
        ),
        html.Div(id='input-files', hidden=True),
        html.Div(id='run-error', hidden=True),
        html.Div(id='render-error', hidden=True),
        html.Button(['clean inputs'], id='clean-inputs', hidden=True),
        html.Button(['clean outputs'], id='clean-output', hidden=True),
        html.Button(['clean graphs'], id='clean-graphs', hidden=True),
        dbc.Toast(
            id="error-toast",
            header="Ops...",
            is_open=False,
            dismissable=True,
            icon="danger",
            style={
                "position": "fixed", "top": 66, "right": 10,
                "max-width": "none", "white-space": "pre-wrap",
                "overflow-y": "auto", "max-height": "calc(100vh - 66px - 9px)"
            }
        )
    ], fluid=True)
])


# noinspection PyUnusedLocal
@app.server.route("/demos")
@app.server.route("/templates/<path:path>")
def download(path=None):
    """Files download callback."""
    path = osp.join(osp.dirname(__file__), request.path[1:])
    if osp.isdir(path):
        import glob
        import zipfile
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as z:
            for f_name in glob.glob(osp.join(path, '**/*'), recursive=True):
                z.write(f_name, arcname=osp.relpath(f_name, osp.basename(path)))
        data.seek(0)
        return send_file(
            data, as_attachment=True,
            attachment_filename='%s.zip' % osp.basename(path)
        )
    return send_file(path, as_attachment=True)


app.clientside_callback(
    """
    function(n_clicks, contents, filenames, children) {
        let clear = (n_clicks || 0) > (window.clear_inputs_n || 0),
            hidden = !!clear || !(contents && contents.length), i;
        window.clear_inputs_n = n_clicks || 0;
        children = clear ? [] : (children || []);
        if (!hidden) {
            window.input_counter = window.input_counter || 0
            for (i = 0; i < contents.length; i++) { 
                let key = window.input_counter;
                window.input_counter++;
                children.push({
                    type: "ListGroupItem",
                    namespace: "dash_bootstrap_components",
                    props: {
                        style: {
                            "paddingTop": ".1rem", 
                            "paddingBottom": ".1rem"
                        }, 
                        id: "input-group-" + key, 
                        children: [
                            {
                                type: "A", 
                                namespace: "dash_html_components",
                                props: { 
                                    id: "input-" + key,
                                    children: [filenames[i]], 
                                    href: contents[i],  
                                    download: filenames[i],
                                    style: {float: "left"}
                                }
                            }, {
                                type: "Tooltip", 
                                namespace: "dash_bootstrap_components", 
                                props: {
                                    children: [
                                        "Click to download the Input File"
                                    ], 
                                    target: "input-" + key
                                }
                            }, {
                                type: "Button", 
                                namespace: "dash_html_components", 
                                props: {
                                    children:["remove"],
                                    className: "btn btn-danger btn-sm",
                                    style: {float: "right"},
                                    onClick: (function(id) {
                                        if (!window.running) {
                                            document.getElementById(id).remove()
                                            document.getElementById('clean-output').click()
                                            document.getElementById('clean-graphs').click()
                                        }
                                    }).bind(null, "input-group-" + key)
                                }
                            }
                        ]
                    }
                })
            }
        }
        if (!clear){
            document.getElementById('clean-output').click()
            document.getElementById('clean-graphs').click()
        }
        return [children, hidden, hidden, [%s]];
    }
    """ % json.dumps(
        input_upload, default=_json_default, separators=(',', ':')
    ),
    Output('input-file-group', 'children'),
    Output('input-file-list', 'hidden'),
    Output('run-button-container', 'hidden'),
    Output('upload-input-file-container', 'children'),
    Input('clean-inputs', 'n_clicks'),
    Input('upload-input-file', 'contents'),
    State('upload-input-file', 'filename'),
    State('input-file-group', 'children')
)
app.clientside_callback(
    """
    function(click, is_open) {
        if (!click)
            is_open = true
        return [!is_open, is_open ? "Show Input Files" : "Hide Input Files"];
    }
    """,
    Output('input-file-list-collapse', 'is_open'),
    Output('show-input-button', 'children'),
    Input('show-input-button', 'n_clicks'),
    State('input-file-list-collapse', 'is_open')
)
app.clientside_callback(
    """
    function(click, group) {
        window.running = true;
        let files = [];
        for (i = 0; i < (group || []).length; i++){
            if (!group[i].props.n_clicks) {
                files.push(group[i].props.children[0].props.download)
                files.push(group[i].props.children[0].props.href)
            }
        }
        return [!!click, [{
            type: "Spinner", 
            namespace: "dash_bootstrap_components", 
            props: {size: "sm"}
        }, " Running..."], files]
    }
    """,
    Output('run-button', 'disabled'),
    Output('run-button', 'children'),
    Output('input-files', 'children'),
    Input('run-button', 'n_clicks'),
    State('input-file-group', 'children')
)


@app.callback(
    Output('upload-output-file', 'contents'),
    Output('upload-output-file', 'filename'),
    Output('run-button-container', 'children'),
    Output('run-error', 'children'),
    Input('run-button', 'disabled'),
    Input('input-files', 'children')
)
def execute(running, input_files):
    """Execute callback."""
    output_file, output_fpath, error = None, None, None
    if running:
        # noinspection PyBroadException
        try:
            from . import dsp
            it = iter(input_files)
            input_files = {
                k: io.BytesIO(base64.b64decode(v.split(',')[1]))
                for k, v in zip(it, it)
            }
            input_fpaths, input_files = zip(*input_files.items())
            outputs = ['output_file', 'output_fpath']
            output_fpath = datetime.datetime.today().strftime(
                '%Y%m%d_%H%M%S-output.xlsx'
            )
            inputs = {
                'input_files': input_files, 'input_fpaths': input_fpaths,
                'output_fpath': osp.join(ODIR, output_fpath)
            }
            inputs = sh.combine_dicts(inputs, getattr(app, 'inputs', {}))
            output_file, _ = sh.selector(outputs, dsp(
                inputs, outputs=outputs + (['written'] if ODIR else []),
                verbose=VERBOSE
            ), output_type='list')

            if ODIR:
                output_file = 'outputs/%s' % output_fpath
            else:
                output_file.seek(0)
                output_file = (
                    'data:application/vnd.openxmlformats-officedocument'
                    '.spreadsheetml.sheet;base64,{}'
                ).format(base64.b64encode(output_file.read()).decode())
        except Exception:
            error = traceback.format_exc()
            log.warning(error)
    return output_file, output_fpath, run_button, error


app.clientside_callback(
    """
    function(n_clicks, contents, filename) {
        let clear = (n_clicks || 0) > (window.clear_output_n || 0);
        window.clear_output_n = n_clicks || 0;
        let hidden = clear || !(contents && contents.length);
        if (!clear) {
            if (!window.running)
                document.getElementById('clean-inputs').click()
            document.getElementById('clean-graphs').click()
        }
        window.running = false
        return [clear ? [] : {
            type: "ListGroupItem",
            namespace: "dash_bootstrap_components",
            props: {
                children: [{
                    type: "A", 
                    namespace: "dash_html_components",
                    props: { 
                        id: "output-link",
                        children: [filename], 
                        href: contents,  
                        download: filename
                    }
                }],
                style: {"padding": 0}
            }
        }, hidden, hidden];
    }
    """,
    Output('output-file-group', 'children'),
    Output('output-file-list', 'hidden'),
    Output('graph-button-container', 'hidden'),
    Input('clean-output', 'n_clicks'),
    Input('upload-output-file', 'contents'),
    State('upload-output-file', 'filename')
)
app.clientside_callback(
    """
    function(click) {
        return [!!click, [{
            type: "Spinner", 
            namespace: "dash_bootstrap_components", 
            props: {size: "sm"}
        }, " Rendering..."]]
    }
    """,
    Output('graph-button', 'disabled'),
    Output('graph-button', 'children'),
    Input('graph-button', 'n_clicks')
)
app.clientside_callback(
    """
    function(n_clicks, disabled, error) {
        let clear = (n_clicks || 0) > (window.clear_graphs_n || 0);
        window.clear_graphs_n = n_clicks || 0;
        if (clear)
            return true
        return !!(error || (disabled === true))
    }
    """,
    Output('graph-container', 'hidden'),
    Input('clean-graphs', 'n_clicks'),
    Input('graph-button', 'disabled'),
    Input('render-error', 'children'),

)
app.clientside_callback(
    """
    function(run_error, render_error) {
        let error = run_error || render_error;
        return [error, !!error]
    }
    """,
    Output('error-toast', 'children'),
    Output('error-toast', 'is_open'),
    Input('run-error', 'children'),
    Input('render-error', 'children')
)


@app.callback(
    Output('render-error', "children"),
    Output('graph-button-container', 'children'),
    *(Output('%s-container' % k, "children") for k in __graphs__),
    Input('graph-button', 'disabled'),
    State('upload-output-file', 'contents'),
    State('upload-output-file', 'filename')
)
def render(rendering, contents, filename):
    """Render graphs callback."""
    error = None
    if rendering and contents is not None:
        # noinspection PyBroadException
        try:
            from . import dsp
            if ODIR and not ';base64,' in contents:
                inputs = {'input_fpaths': (osp.join(ODIR, filename),)}
            else:
                content_type, content_string = contents.split(';base64,')
                decoded = base64.b64decode(content_string)
                output_file = io.BytesIO(decoded)
                inputs = {
                    'input_fpaths': (filename,),
                    'input_files': (output_file,)
                }
            inputs = sh.combine_dicts(inputs, getattr(app, 'inputs', {}))
            sol = dsp(
                inputs, outputs=['graphs'], verbose=VERBOSE
            ).get('graphs', {})
            graphs = [
                dcc.Graph(id=k, figure=sol[k]) if k in sol else None
                for k in __graphs__
            ]
        except Exception:
            error = traceback.format_exc()
            log.warning(error)
            graphs = [None] * len(__graphs__)
    else:
        graphs = [dcc.Graph(id=k) for k in __graphs__]

    return [error, graph_button] + graphs


class GUI(Site):
    def __init__(self, sitemap=None, *args, inputs=None, **kwargs):
        super(GUI, self).__init__(sitemap, *args, **kwargs)
        self.inputs = inputs or {}

    def app(self):
        app.inputs = self.inputs
        return app.server


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
