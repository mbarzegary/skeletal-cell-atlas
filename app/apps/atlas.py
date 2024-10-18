from app import app, server, settings
from flask import send_from_directory

# upgraded to dash v2.0
import dash
from dash import dcc
from dash import html
# import dash_daq as daq
# import loompy

import base64
import plotly.express as px
import pandas as pd
import numpy as np
import os
import time
import scanpy as sc

data_path = os.path.abspath(settings.get('DATA_PATH'))
data_file_name = "Atlas_v3_5.h5ad"
h5_file = os.path.join(data_path, data_file_name)
df = pd.read_csv(os.path.join(data_path, 'data.csv'))
df.insert(0, 'Gene', 0)
df_genes = pd.read_csv(os.path.join(data_path, 'genes.csv'))
df_filtered = []

available_techs = df['tech'].unique()
available_tissues = df['tissue'].unique()
available_devtps = df['devtp'].unique()
available_studies = df['study'].unique()
available_types = df['identity'].unique()

app_title = "Skeletal Cell Atlas"
header_bg_color = "#506784"
header_font_color = "#F3F6FA"

option_block = [
        html.H3('Filters'),

        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Cell type'),
            dcc.Dropdown(
                id='type-column',
                options=[{'label': i, 'value': i} for i in available_types],
                value=[],
                multi=True
            )
        ]),

        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Technology'),
            dcc.Dropdown(
                id='tech-column',
                options=[{'label': i, 'value': i} for i in available_techs],
                value=[],
                multi=True
            )
        ]),

        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Tissue'),
            dcc.Dropdown(
                id='tissue-column',
                options=[{'label': i, 'value': i} for i in available_tissues],
                value=[],
                multi=True
            )
        ]),

        # html.Div(className='app-controls-block', children=[
        #     html.Div(className='app-controls-name', children='Origin'),
        #     dcc.Dropdown(
        #         id='origin-column',
        #         options=[{'label': i, 'value': i} for i in available_origins],
        #         value='Limb bud',
        #         multi=True
        #     )
        # ]),

        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Developmental time point'),
            dcc.Dropdown(
                id='devtp-column',
                options=[{'label': i, 'value': i} for i in available_devtps],
                value=[],
                multi=True
            )
        ]),

        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Study'),
            dcc.Dropdown(
                id='study-column',
                options=[{'label': i, 'value': i} for i in available_studies],
                value=[],
                multi=True
                )
        ]),

        html.Hr(),

        html.H3('Gene Expressions'),
        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Gene of interest'),
            dcc.Dropdown(
                id='gene-expr',
                options=[{'label': i, 'value': i} for i in df_genes['genes'].unique()]
            )
        ]),

        html.Hr(),

        html.H3('Visualization'),
        # html.Div(className='app-controls-block', children=[
        #     html.Div(className='app-controls-name', children='View'),
        #     daq.ToggleSwitch(
        #         id='view-switch',
        #         color=header_bg_color,
        #         label=['2D', '3D'],
        #         size=35,
        #         labelPosition='bottom',
        #         value=False
        #     )
        # ]),
        html.Div(className='app-controls-block', children=[
            html.Div(className='app-controls-name', children='Cell size'),
            dcc.Slider(
                id='cell-size-input',
                value=2,
                min=1,
                max=7,
                step=1
            )
        ]),

        html.Hr(),
        html.H3('Download Data'),
        html.Div(className='app-controls-block', children=[
            html.Div(
                [
                    html.Button("Download filtered gene expression", id="btn_gene", className="control-download"),
                    dcc.Download(id="download-gene"),
                    html.Button("Download filtered records as CSV", id="btn_csv", className="control-download"),
                    dcc.Download(id="download-dataframe-csv"),
                    # html.A(html.Button('Download database as Loom file', className='control-download'),
                    #     href='/downloadloom', target="_blank"),
                    html.A(html.Button('Download database as H5 file', className='control-download'),
                        href='https://kuleuven-my.sharepoint.com/personal/liesbeth_ory_kuleuven_be/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fliesbeth%5Fory%5Fkuleuven%5Fbe%2FDocuments%2FAtlas%5Fv3%5F5%2Eh5ad&parent=%2Fpersonal%2Fliesbeth%5Fory%5Fkuleuven%5Fbe%2FDocuments&ga=1&LOF=1', target="_blank"),
                ]
            )
        ])
    ]

page_layout = html.Div(id='main-body', className='app-body', children=[
        # dcc.Loading(className='data-loading', fullscreen=True,
        #     children=[html.Div(id='main-container')]),
        html.Div(className='data-loading', children=
        dcc.Loading(type="dot", children=[
            html.Div(children=[dcc.Graph(id='main-fig')]),
            html.Div(id='number-output', style={"text-align": "center"})
            ])),
        html.Div(className='control-tabs', children=[
            dcc.Tabs(id='explorer-control-tabs', value='what-is', children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children='What is Skeletal Cell Atlas?'),
                        html.P('The Skeletal Cell Atlas is an initiative to integrate publicly available single-cell RNA-seq datasets from skeletal and limb developmental studies. The atlas is an interactive web-based resource to facilitate accessibility of genomics data. Users can interactively identify cell types expressing genes of interest or discover transcriptomic subpopulations within a cell type.'),
                        html.P('In the "Options" tab, you can filter the atlas based on the available metadata or plot your gene of interest.'),
                        html.P('Interested in contributing to the atlas?'),
						html.A("Contact us!", href='mailto:liesbet.geris@kuleuven.be', target="_blank")
                    ])
                ),
                dcc.Tab(
                    label='Options',
                    value='view',
                    children=html.Div(className='control-tab', children=[
                        html.Div(
                            id='feature-view-options',
                            children = option_block
                        )
                    ])
                )
            ])
        ])
    ])



layout = html.Div(
        id='main_page',
        children=[
            # dcc.Location(id='url', refresh=False),
            html.Div(
                id='app-page-header',
                children=[
                    html.A(
                        id='logo', children=[
                            html.Img(
                                src='data:image/jpg;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            'app/assets/logo.jpg', 'rb'
                                        ).read()
                                    ).decode()
                                )
                            )],
                        href="#"
                    ),
                    html.H2(
                        app_title
                    )
                ],
                style={
                    'background': header_bg_color,
                    'color': header_font_color,
                }
            ),
            html.Div(
                id='app-page-content',
                children=page_layout
            )
        ],
    )

def read_genes(selected_gene):
    if os.path.isfile(h5_file):
        adata = sc.read_h5ad(h5_file)
        return adata[:, selected_gene].X.toarray()
    else:
        return None

@app.callback(
    [dash.dependencies.Output('main-fig', 'figure'),
     dash.dependencies.Output("number-output", "children")],
    [dash.dependencies.Input('type-column', 'value'),
     dash.dependencies.Input('tech-column', 'value'),
     dash.dependencies.Input('tissue-column', 'value'),
     dash.dependencies.Input('devtp-column', 'value'),
     dash.dependencies.Input('study-column', 'value'),
     dash.dependencies.Input('gene-expr', 'value'),
    #  dash.dependencies.Input('view-switch', 'value'),
     dash.dependencies.Input('cell-size-input', 'value')])
def update_graph(selected_type, selected_tech, selected_tissue,
                 selected_devtp, selected_study,
                #  selected_gene, is_3d, cell_size):
                 selected_gene, cell_size):

    if type(selected_type) == str:
        selected_type = [selected_type]
    if type(selected_tech) == str:
        selected_tech = [selected_tech]
    if type(selected_tissue) == str:
        selected_tissue = [selected_tissue]
    if type(selected_devtp) == str:
        selected_devtp = [selected_devtp]
    if type(selected_study) == str:
        selected_study = [selected_study]

    color_scale = px.colors.sequential.Viridis

    color_ind = "identity"
    if selected_gene != None:
        color_ind = "Gene"
        df["Gene"] = read_genes(selected_gene)
        color_scale = ["lightgrey", "blue"]
        # color_scale = ["lightgrey", "blue", "red"]

    global df_filtered
    df_filtered = df[(df.tech.notnull() if selected_tech == [] else df.tech.isin(selected_tech))
                     & (df.identity.notnull() if selected_type == [] else df.identity.isin(selected_type))
                     & (df.tissue.notnull() if selected_tissue == [] else df.tissue.isin(selected_tissue))
                     & (df.devtp.notnull() if selected_devtp == [] else df.devtp.isin(selected_devtp))
		             & (df.study.notnull() if selected_study == [] else df.study.isin(selected_study))
                    ]
    if len(df_filtered.index) == 0:
        return px.scatter(), "No record to plot"

    fig = px.scatter(df_filtered, x="x", y="y", color=color_ind,
                         color_continuous_scale=color_scale,
                         hover_name="identity", hover_data=["tech", "tissue", "devtp", "study"])

    fig.update_traces(marker=dict(size=cell_size))
    fig.update_layout(legend=dict(itemsizing='constant',font=dict(size=18)))
    fig.update_xaxes(title="UMAP 1")
    fig.update_yaxes(title="UMAP 2")

    return fig, f"Number of records: {len(df_filtered.index)}"

@app.callback(
    dash.dependencies.Output("download-dataframe-csv", "data"),
    dash.dependencies.Input("btn_csv", "n_clicks"),
    prevent_initial_call=True)
def download_csv(n_clicks):
    return dcc.send_data_frame(df_filtered.to_csv, "data.csv")

@app.callback(
    dash.dependencies.Output("download-gene", "data"),
    dash.dependencies.Input("btn_gene", "n_clicks"),
    prevent_initial_call=True)
def download_gene(n_clicks):
    df_gene = df_filtered.filter(items=['Gene'])
    return dcc.send_data_frame(df_gene.to_csv, "gene.csv")

@server.route("/downloadloom")
def download_loom_file():
    return send_from_directory(data_path, data_file_name, as_attachment=True)
