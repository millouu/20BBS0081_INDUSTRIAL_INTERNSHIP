from datetime import datetime
import math
import pandas as pd
from dash import dcc, dash
from dash import html, callback_context
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# READ DATASET
df = pd.read_csv("plugin_dataset_filtered.csv")
external_stylesheets = [
    'https://drive.google.com/uc?export=view&id=1p8h1PdSIW4kNCfycW_0QpjsipBbbik3I',
    dbc.themes.BOOTSTRAP
]

fig2 = go.Figure(data=[go.Pie()])
fig2.update_layout(
    showlegend=False,
    annotations=[
        dict(text='Uh-Oh, nothing to show!', font_size=30, showarrow=False,
             font=dict(color='#9DA0A8', family='Urbanist'))],
    title='Data Availability Pie',
    title_font=dict(size=22, color='#9DA0A8', family='Urbanist')
)

fig = px.treemap()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# DEFINE APP LAYOUT
app.layout = html.Div(
    style={
        'font-family': 'Urbanist',
        'margin': '0px',
        'padding': '0px'
    },

    children=[
        html.Div(
            children=[
                html.Div(
                    [
                        html.Div(
                            children=[
                                html.H2(["Dashboard"],
                                        style={
                                            "font-family": "Urbanist",
                                            "margin-right": "10px",
                                            "margin-bottom": "0px"
                                        }),
                                html.Div(
                                    children=[],
                                    style={
                                        'height': '35px',
                                        'border-left': '3px solid #131313',
                                        "margin-right": "10px"
                                    }
                                ),
                                html.H5(["Production Data Availability"],
                                        style={
                                            # "width":"200px",
                                            "font-family": "Bebas Neue",
                                            "font-size": "2rem",
                                            'text-align': 'left',
                                            "margin-bottom": "0px"
                                        })
                            ],
                            style={
                                'display': 'flex',
                                'align-items': "center"
                            }
                        ),

                        html.Div(
                            [
                                dbc.Button('Download Your Dataset',
                                           id='download-dataset-button',
                                           n_clicks=0,
                                           className="me-1",
                                           outline='false',
                                           style={
                                               'background-color': '#131313',
                                               'color': 'white',
                                               'border-radius': '3px',
                                               'font-size': '1.1rem',
                                               'padding': '8px 30px'
                                           }
                                           ),
                                dbc.Popover(
                                    [
                                        dbc.PopoverBody(
                                            [
                                                html.H6("Select Threshold"),
                                                html.P("This will be used to compute availability"),
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id='save-dataset-threshold-dropdown',
                                                            options=[
                                                                {'label': 'Years', 'value': 'years'},
                                                                {'label': 'Months', 'value': 'months'},
                                                                {'label': 'Days', 'value': 'days'},
                                                                {'label': 'Hours', 'value': 'hours'},
                                                                {'label': 'Minutes', 'value': 'minutes'},
                                                                {'label': 'Seconds', 'value': 'seconds'}
                                                            ],
                                                            value='years',
                                                            placeholder="Select Unit",
                                                            style={
                                                                'margin-right': '10px',
                                                                'width': '100px'
                                                            },
                                                            clearable=False
                                                        ),
                                                        dbc.Input(id="save-dataset-threshold-value",
                                                                  placeholder="Enter Value",
                                                                  type="number", value=1, min=1, step=1)
                                                    ],
                                                    style={
                                                        'display': 'flex'
                                                    }
                                                ),
                                                html.Br(),
                                                html.H6("Enter File Name"),
                                                dbc.Input(id="save-dataset-filename-input", placeholder="",
                                                          type="text"),

                                                html.P("The file will not download unless you enter a file name."),
                                                html.Br(),
                                                html.H6("Choose File Format"),
                                                dcc.Dropdown(
                                                    id='save-dataset-format-dropdown',
                                                    options=[
                                                        {'label': 'CSV', 'value': 'csv'},
                                                        {'label': 'JSON', 'value': 'json'}
                                                    ],
                                                    value='csv',
                                                    placeholder='Select an option',
                                                    clearable=False
                                                ),
                                                html.Br(),
                                                dbc.Button('Save File',
                                                           id='save-dataset-button',
                                                           n_clicks=0,
                                                           className="me-1",
                                                           outline='false',
                                                           style={
                                                               'background-color': '#131313',
                                                               'color': 'white',
                                                               'padding': '10px 30px',
                                                               'border-radius': '3px',
                                                               'font-size': '1rem',
                                                               'text-align': 'center',
                                                               'width': '100%'
                                                           }
                                                           ),

                                            ],

                                        ),
                                    ],
                                    id='dropdown-popover',
                                    is_open=False,
                                    target='download-dataset-button',
                                    placement='bottom',
                                    trigger='hover',
                                    style={
                                        'max-width': '400px'
                                    }

                                )
                            ],

                        ),
                        dcc.Download(id='download-dataset')
                    ],

                    style={
                        # 'padding': '2rem',
                        'color': '#131313',
                        'margin': '30px 50px 60px 50px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    }

                ),

                html.Div(
                    [
                        # DIV FOR ENTITY DROPDOWN LIST
                        html.Div(
                            [
                                html.Div(
                                    [html.Label(
                                        children=[
                                            html.H5(
                                                children='Select Property:',
                                                style={
                                                    'margin-bottom': '10px',
                                                    'margin-top': '0px'
                                                }
                                            )
                                        ]
                                    ),
                                        dcc.Dropdown(
                                            id='property-dropdown',
                                            options=[{'label': i, 'value': i} for i in
                                                     sorted(df["Property"].unique())],
                                            value=[]
                                            # multi=True
                                        )],
                                    style={
                                        'width': '30%'
                                    }
                                ),
                                html.Div(
                                    children=[
                                        html.Label(
                                            children=[
                                                html.H5(
                                                    children='Select Entities:',
                                                    style={
                                                        'margin-bottom': '10px',
                                                        'margin-top': '0px'
                                                    }
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id='entities-dropdown',
                                                    style={
                                                        'width': '95%'
                                                    },
                                                    options=[{'label': i, 'value': i} for i in
                                                             sorted(df["Entity Name"].unique())],
                                                    value=[],
                                                    multi=True
                                                ),

                                                html.Div(
                                                    id='btn-container',
                                                    children=[
                                                        dbc.Button(
                                                            ["Select All"],
                                                            id="select-all-button",
                                                            className="me-2",
                                                            disabled=True,
                                                            n_clicks=0,
                                                            style={
                                                                'background-color': '#131313',
                                                                'color': 'white',
                                                                'padding': '10px 30px',
                                                                'border-radius': '3px',
                                                                'font-size': '1rem',
                                                                'text-align': 'center',
                                                                'width': '100%',
                                                                'border': 'none'
                                                            }
                                                        )
                                                    ],
                                                    style={
                                                        'width': '30%'
                                                    }
                                                )
                                            ],
                                            style={
                                                'display': 'flex'
                                            }
                                        )
                                    ],
                                    style={
                                        'width': '30%'
                                    }
                                ),
                                html.Div(
                                    children=[
                                        html.Label(
                                            children=[
                                                html.H5(
                                                    children='Select Threshold:',
                                                    style={
                                                        'margin-bottom': '10px',
                                                        'margin-top': '0px'
                                                    }
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id='threshold-dropdown',
                                                    options=[
                                                        {'label': 'Years', 'value': 'years'},
                                                        {'label': 'Months', 'value': 'months'},
                                                        {'label': 'Days', 'value': 'days'},
                                                        {'label': 'Hours', 'value': 'hours'},
                                                        {'label': 'Minutes', 'value': 'minutes'},
                                                        {'label': 'Seconds', 'value': 'seconds'}
                                                    ],
                                                    value='years',
                                                    placeholder="Select Unit",
                                                    style={
                                                        'margin-right': '10px',
                                                        'width': '150px'
                                                    },
                                                    clearable=False
                                                ),
                                                dbc.Input(id="threshold-value", placeholder="Enter Value",
                                                          type="number", value=1, min=1, step=1)
                                            ],
                                            style={
                                                'display': 'flex',
                                            }
                                        )
                                    ],
                                    style={
                                        'width': '30%'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                # 'width':'100%',
                                'justify-content': 'space-between'
                            }

                        ),

                        html.Br(),
                        html.Br(),
                        html.Div(
                            style={
                                'display': 'flex',
                                'justify-content': 'space-between'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'flex-direction': 'column',
                                        'width': '950px'
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.H3("PROPERTY:",
                                                        style={"margin-bottom": "0px", "margin-right": "20px"}),
                                                html.H3([],
                                                        id="selected-property-heading",
                                                        style={
                                                            "margin-bottom": "0px",
                                                            "font-weight": "bold"
                                                        })
                                            ],
                                            style={
                                                'display': 'flex',
                                                'border': '1px solid #C3C3C3',
                                                'border-radius': '2px',
                                                'padding': '20px',
                                                "align-items": "baseline",
                                                'margin-bottom': '20px'
                                            }
                                        ),
                                        html.Div(
                                            id="datatable-div-container",
                                            children=[
                                                # DIV FOR CONTAINING DATA TABLE
                                                html.Div(
                                                    id='datatable-div',
                                                    children=[
                                                        html.Div(
                                                            [
                                                                html.P(
                                                                    "Select some entities from the list to view the datatable")
                                                            ],
                                                            style={
                                                                'position': 'absolute',
                                                                'top': '50%',
                                                                'left': '50%',
                                                                'transform': ' translate(-50%,-50%)',
                                                                'color': '#9DA0A8',
                                                                'font-size': '1.8rem',
                                                                'text-align': 'center'
                                                            }
                                                        ),
                                                        dash_table.DataTable(id="datatable")
                                                    ]
                                                )
                                            ],
                                            style={
                                                'position': 'relative',
                                                'border': '1px solid #C3C3C3',
                                                'border-radius': '2px',
                                                'height': '355px'
                                            }
                                        )
                                    ]
                                ),
                                html.Br(),

                                # DIV FOR CONTAINING PIE CHART
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="pie-chart",
                                            figure=fig2
                                        )
                                    ],
                                    style={
                                        'border': '1px solid #C3C3C3',
                                        'border-radius': '2px',
                                        'width': '403px'
                                    }
                                )
                            ]
                        ), html.Br(), html.Br(), html.Br(),
                        html.Div(
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'flex-direction': 'column',
                                        'justify-content': 'space-between'
                                    },
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    style={
                                                        'display': 'flex',
                                                        'justify-content': 'space-between',
                                                        # 'margin': '0px 30px 0px 30px'
                                                    },
                                                    children=[
                                                        html.Div(
                                                            [
                                                                html.H3(
                                                                    "Data Availability Treemap"
                                                                ),
                                                                html.P(
                                                                    [
                                                                        "This treemap shows the availability of different properties of an entity based on a common threshold.",
                                                                        html.Br(),
                                                                        "The size of the sectors is based on the number of properties associated with an entity.",
                                                                        html.Br()
                                                                    ],
                                                                    style={
                                                                        'font-size': '18px'
                                                                    }),
                                                            ],
                                                            style={
                                                                'width': '50%'
                                                            }
                                                        ),
                                                        html.Div(
                                                            style={
                                                                'display': 'flex',
                                                                'flex-direction': 'column',
                                                                'border': '1px solid #C3C3C3',
                                                                'border-radius': '2px',
                                                                'padding': '10px 10px',
                                                                'width': '403px'
                                                            },
                                                            children=[
                                                                html.H4("How is the Availability Score calculated?",
                                                                        style={
                                                                            'font-size': '21px'
                                                                        }),
                                                                html.Div(
                                                                    [
                                                                        html.Div("Availability Score= ",
                                                                                 style={
                                                                                     'margin-right': '10px'
                                                                                 }),
                                                                        html.Div(
                                                                            [
                                                                                html.Div("No. Of Available Properties",
                                                                                         style={
                                                                                             'margin-bottom': '1px'
                                                                                         }),
                                                                                html.Hr(
                                                                                    style={
                                                                                        'display': 'block',
                                                                                        'height': '1px',
                                                                                        'border': '0',
                                                                                        'border-top': '2px solid #000000',
                                                                                        'margin': '0 0 0 0',
                                                                                        'padding': '0'
                                                                                    }
                                                                                ),
                                                                                html.Div("Total No. Of Properties")
                                                                            ],
                                                                            style={
                                                                                'display': 'flex',
                                                                                'flex-direction': 'column',
                                                                                'text-align': 'center'
                                                                            }
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        'display': 'flex',
                                                                        'margin': '0 auto',
                                                                        'font-size': '17px'
                                                                    }
                                                                ),
                                                                html.H6(
                                                                    [
                                                                        html.Em(
                                                                            "The value of the score lies between 0 and 1 (inclusive)")
                                                                    ],
                                                                    style={
                                                                        'margin': '20px auto 0 auto',
                                                                        'color': '#787777'
                                                                    })
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ],
                                            style={
                                                # 'width':'20%'
                                            }
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H6(
                                                    children='Select Threshold:',
                                                    style={
                                                        'margin-bottom': '10px',
                                                        'margin-top': '0px',
                                                        'padding': '0px 30px 0px 30px'
                                                    }
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='threshold2-dropdown',
                                                            options=[
                                                                {'label': 'Years', 'value': 'years'},
                                                                {'label': 'Months', 'value': 'months'},
                                                                {'label': 'Days', 'value': 'days'},
                                                                {'label': 'Hours', 'value': 'hours'},
                                                                {'label': 'Minutes', 'value': 'minutes'},
                                                                {'label': 'Seconds', 'value': 'seconds'}
                                                            ],
                                                            value='years',
                                                            placeholder="Select Unit",
                                                            style={
                                                                'margin-right': '10px',
                                                                'width': '150px'
                                                            },
                                                            clearable=False
                                                        ),
                                                        dbc.Input(id="threshold2-value", placeholder="Enter Value",
                                                                  type="number", value=1, min=1, step=1)
                                                    ],
                                                    style={
                                                        'display': 'flex',
                                                        'padding': '0px 30px 0px 30px',
                                                        'margin-bottom': '5px'
                                                    }
                                                ),
                                                dcc.Graph(
                                                    id="treemap-graph",
                                                    figure=fig,
                                                    style={
                                                        'z-index': '-1'
                                                    }
                                                ),
                                                html.Span(
                                                    [
                                                        html.P("💡", style={'margin-right': '5px'}),
                                                        html.Em([
                                                            "Hover over the sectors to view details about the entity."],
                                                            style={
                                                                'font-size': '18px'
                                                            })
                                                    ],
                                                    style={
                                                        'display': 'flex',
                                                        'padding': '0px 30px 0px 30px',
                                                        'margin-top': '-10px',
                                                        'position': 'absolute',
                                                        'z-index': '100'
                                                    }
                                                )
                                            ],
                                            style={

                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    style={
                        'margin': '70px 50px 50px 50px'
                    }

                )
            ]
        )
    ]
)


@app.callback(
    [Output("selected-property-heading", "children"),
     Input("property-dropdown", "value")]
)
def update_selected_property_div(selected_prop):
    return [selected_prop]


# FOR UPDATING THE DATATABLE WITH THE VALUES FROM THE DROPDOWN
@app.callback(
    [Output(component_id='datatable-div', component_property='children'),
     Output(component_id='datatable-div-container', component_property='style'), Output("pie-chart", "figure")],
    [Input(component_id='property-dropdown', component_property='value'),
     Input(component_id='entities-dropdown', component_property='value'),
     Input('threshold-value', 'value'),
     Input('threshold-dropdown', 'value')]
)
def update_datatable(property_val, entity_vals, threshold_val, threshold_unit):
    emptyfig = go.Figure(data=[go.Pie()])
    emptyfig.update_layout(
        showlegend=False,
        annotations=[
            dict(text='Uh-Oh, nothing to show!', font_size=30, showarrow=False,
                 font=dict(color='#9DA0A8', family='Urbanist'))],
        title='Data Availability Pie',
        title_font=dict(size=22, color='#9DA0A8', family='Urbanist')
    )
    if not property_val:
        return (
            [html.Div(
                [
                    html.P("Please select a property to  view the datatable")
                ],
                style={
                    'position': 'absolute',
                    'top': '50%',
                    'left': '50%',
                    'transform': ' translate(-50%,-50%)',
                    'color': '#9DA0A8',
                    'font-size': '1.8rem',
                    'text-align': 'center'
                }
            ), {'position': 'relative',
                'border': '1px solid #C3C3C3',
                'border-radius': '2px',
                'height': '355px'}, emptyfig]
        )
    elif not entity_vals:
        return (
            [html.Div(
                [
                    html.P("Please select some entities to  view the datatable")
                ],
                style={
                    'position': 'absolute',
                    'top': '50%',
                    'left': '50%',
                    'transform': ' translate(-50%,-50%)',
                    'color': '#9DA0A8',
                    'font-size': '1.8rem',
                    'text-align': 'center'
                }
            )], {'position': 'relative',
                 'border': '1px solid #C3C3C3',
                 'border-radius': '2px',
                 'height': '355px'}, emptyfig
        )


    else:
        if property_val and entity_vals and threshold_val and threshold_unit:
            temp_df = df[df["Property"].astype(str) == str(property_val)]

            filtered_df = temp_df[temp_df.loc[:, ('Entity Name')].isin(entity_vals)]
            # df2 = filtered_df.loc[:, ('Property')]
            df1 = filtered_df.loc[:, ('Entity Name')]
            tsdf = filtered_df.loc[:, ('Timestamp')]
            valuedf = filtered_df.loc[:, ('Value')]
            df3 = pd.concat([df1, tsdf, valuedf], axis=1)
            df3.columns = ['entity_name', 'timestamp', 'value']
            df3['available'] = False

            for ind in df3.index:
                curr = datetime.now()

                if threshold_unit == 'years':
                    if math.ceil((curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                           '%Y-%m-%dT%H:%M:%S.%fZ')).days / 365) > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'


                elif threshold_unit == 'months':
                    if math.ceil((curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                           '%Y-%m-%dT%H:%M:%S.%fZ')).days / 30) > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'


                elif threshold_unit == 'days':
                    if (curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                 '%Y-%m-%dT%H:%M:%S.%fZ')).days > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'


                elif threshold_unit == 'hours':
                    if math.ceil((curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                           '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() / 3600) > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'

                elif threshold_unit == 'minutes':
                    if math.ceil((curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                           '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() / 60) > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'

                elif threshold_unit == 'seconds':
                    if (curr - datetime.strptime(df3.loc[ind, 'timestamp'],
                                                 '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() > threshold_val:
                        df3.loc[ind, 'available'] = '🔴'
                    else:
                        df3.loc[ind, 'available'] = '🟢'

            df3 = df3.sort_values('entity_name')

            pie_dict = {'Available': 0, 'Not Available': 0}
            status_counts = df3['available'].value_counts().to_dict()
            if '🔴' in status_counts:
                pie_dict['Not Available'] = status_counts['🔴']
            if '🟢' in status_counts:
                pie_dict['Available'] = status_counts['🟢']

            pie_colors = ['rgb(192, 219, 183)', 'rgb(242, 100, 92)']
            piefig = go.Figure(data=[go.Pie(
                go.Pie(labels=list(pie_dict.keys()), values=list(pie_dict.values()))
            )])
            piefig.update_traces(
                hoverinfo='none',
                marker=dict(colors=pie_colors)
            )
            piefig.update_layout(
                title='Data Availability Pie',
                title_font=dict(size=22, family='Urbanist'),
                legend=dict(font=dict(family='Urbanist', size=16))
            )
            piefig.update_layout(legend_itemclick=False, legend_orientation='h', legend_xref='paper', legend_x=0.0001)

            return ([dash_table.DataTable(
                id='datatable',
                columns=[{'name': 'Entity Name', 'id': 'entity_name'},
                         {'name': 'Last Available Timestamp', 'id': 'timestamp'},
                         {'name': 'Last Available Value', 'id': 'value'},
                         {'name': 'Availability Status', 'id': 'available'}],
                data=df3.to_dict('records'),

                style_data_conditional=[
                    {
                        'if': {'column_id': 'available'},
                        'text-align': 'center',
                    }
                ],
                style_cell=
                {
                    'textAlign': 'left',
                    'padding': '10px',
                    'font-family': 'Urbanist',
                    'font-size': '1.2rem',
                    'width': '10%'
                },
                style_header=
                {
                    'fontWeight': 'bold',
                    'text-align': 'center',
                    'fontSize': '1.2rem',
                    'background-color': '#131313',
                    'color': 'white'
                },
                style_table=
                {
                    'maxHeight': '600px',
                    'overflowY': 'auto',
                    'width': '950px',
                    'maxWidth': '950px'
                },
                fixed_rows={'headers': True},
                style_data=
                {
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                tooltip_header={
                    "available": '💡 Tooltip: Click on the arrow toggle on the left to sort the table and see all 🔴 rows or 🟢 rows.'
                },
                css=[{
                    'selector': '.dash-table-tooltip',
                    'rule': 'background-color: white; '
                            'font-family: Urbanist; '
                            'color: black; '
                            'padding:1rem; '
                            'border:0px;'
                            'border-radius:5px;'
                            'box-shadow: 2px 2px 10px #9DA0A8;'

                }],
                tooltip_delay=0,
                tooltip_duration=None,
                sort_action="native"
            )], {'position': 'relative',
                 'border': '1px solid #C3C3C3',
                 'border-radius': '2px',
                 'height': 'fit-content'}, piefig)
        else:
            return (
                [html.Div(
                    [
                        html.P("Make sure you have selected a threshold")
                    ],
                    style={
                        'position': 'absolute',
                        'top': '50%',
                        'left': '50%',
                        'transform': ' translate(-50%,-50%)',
                        'color': '#9DA0A8',
                        'font-size': '1.8rem',
                        'text-align': 'center'
                    }
                )], {'position': 'relative',
                     'border': '1px solid #C3C3C3',
                     'border-radius': '2px',
                     'height': '355px'}, emptyfig
            )


@app.callback(
    Output('entities-dropdown', 'options'),
    Input('property-dropdown', 'value'))
def set_cities_options(selected_property):
    temp_df = df[df["Property"].astype(str) == str(selected_property)]
    return [{'label': i, 'value': i} for i in temp_df["Entity Name"]]


# FOR IMPLEMENTING SELECT ALL USING A BUTTON
@app.callback(
    Output("btn-container", "children"),
    [Input("property-dropdown", "value")]
)
def helper(props):
    if not props:
        return (
            dbc.Button(
                ["Select All"],
                id="select-all-button",
                className="me-2",
                n_clicks=0,
                disabled=True,
                style={
                    'background-color': '#131313',
                    'color': 'white',
                    'border-radius': '3px',
                    'font-size': '1rem',
                    'text-align': 'center',
                    'width': '100%',
                    'border': 'none'

                }
            )
        )
    else:
        return (
            dbc.Button(
                ["Select All"],
                id="select-all-button",
                className="me-2",
                n_clicks=0,
                disabled=False,
                style={
                    'background-color': '#131313',
                    'color': 'white',
                    'border-radius': '3px',
                    'font-size': '1rem',
                    'text-align': 'center',
                    'width': '100%',
                    'border': 'none'
                }
            )
        )


@app.callback(
    Output('select-all-button', 'n_clicks'),
    Input('property-dropdown', 'value')
)
def upon_click(prop):
    if not prop:
        return None


@app.callback(
    Output("entities-dropdown", "value"),
    [Input("select-all-button", "n_clicks")],
    [State("entities-dropdown", "options")])
def update_dropdown(n_clicks, options):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate()
    else:
        trigged_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigged_id == 'select-all-button':
            if n_clicks == 0:  ## Do not update in the beginning
                raise PreventUpdate()

            else:  ## Select all options on odd clicks
                return [i['value'] for i in options]
        else:
            raise PreventUpdate()


# FOR THE TREEMAP
@app.callback(
    Output('treemap-graph', 'figure'),
    Input('threshold2-value', 'value'),
    Input('threshold2-dropdown', 'value')
)
def func(t_val, t_unit):
    emptyfig = px.treemap()
    emptyfig.add_annotation(
        x=0.5,
        y=0.5,
        text='Make sure the threshold field has a value greater than 0',
        showarrow=False,
        font=dict(size=30, family="Urbanist", color='#9DA0A8')
    )
    emptyfig.update_layout(
        title={
            'text': 'Empty Treemap',
            'font': {
                'family': 'Urbanist',
                'size': 24,
                'color': '#9DA0A8'
            }
        }
    )

    if not t_val:
        return emptyfig

    else:
        data = df['Entity Name'].value_counts().reset_index()
        data.columns = ['entity_name', 'count_props']
        data_list = []
        data["avail_count"] = 0

        for ind in data.index:
            timee = df[df["Entity Name"] == data.loc[ind, "entity_name"]]["Timestamp"].tolist()
            propp = df[df["Entity Name"] == data.loc[ind, "entity_name"]]["Property"].tolist()
            current = datetime.now()
            countavprops = 0
            avprop_names = []
            navprop_names = []

            for i in range(len(timee)):
                delta = current - datetime.strptime(timee[i], '%Y-%m-%dT%H:%M:%S.%fZ')
                if t_unit == 'years':
                    if math.ceil(delta.days / 365) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])
                elif t_unit == 'months':
                    if math.ceil(delta.days / 30) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])
                elif t_unit == 'days':
                    if math.ceil(delta.days) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])
                elif t_unit == 'hours':
                    if math.ceil(delta.total_seconds() / 3600) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])
                elif t_unit == 'minutes':
                    if math.ceil(delta.total_seconds() / 60) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])
                elif t_unit == 'seconds':
                    if math.ceil(delta.total_seconds()) <= t_val:
                        countavprops += 1
                        avprop_names.append(propp[i])
                    else:
                        navprop_names.append(propp[i])

            data_list.append([data.loc[ind, "entity_name"], data.loc[ind, "count_props"], countavprops,
                              (countavprops / data.loc[ind, "count_props"]), avprop_names, navprop_names, ""])

        data = pd.DataFrame(data_list,
                            columns=["entity_name", "count_all_props", "count_av_props", "avail_perc", "name_av_props",
                                     "name_nav_props", "parents"])

        fig = px.treemap(data, names='entity_name', values='count_all_props', parents='parents',
                         color='avail_perc',
                         range_color=[0, 1],
                         color_continuous_scale=["#CC3048", "#EB8595", "#FAFAFA", "#496397", "#2B3467"],
                         custom_data=data[["avail_perc", "name_av_props", "name_nav_props"]])
        fig.update_layout(margin=dict(t=25, l=25, r=25, b=25))
        fig.update_layout(font_family="Urbanist", font_size=16)
        fig.update_traces(marker=dict(cornerradius=2))
        fig.update_coloraxes(colorbar_orientation="h", colorbar_thickness=20, colorbar_title_text="AVAILABILITY SCORE",
                             colorbar_title_side="top")
        fig.data[0].hovertemplate = (
                '<b>ENTITY NAME: </b>%{label}'
                '<br>' +
                '<br>' +
                '<b>AVAILABILITY SCORE: %{customdata[0]:.2f}</b>' +
                '<br>' +
                '<br>' +
                '<b>AVAILABLE PROPERTIES</b> <br>%{customdata[1]}' +
                '<br>' +
                '<br>' +
                '<b>UNAVAILABLE PROPERTIES</b> <br><i>%{customdata[2]} </i>' +
                '<br>'
        )

        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Urbanist"
            )
        )
        return fig


# FOR DOWNLOADING THE DATASET BUTTON
@app.callback(
    Output('download-dataset', 'data'),
    Output('save-dataset-button', 'n_clicks'),
    [Input('save-dataset-button', 'n_clicks'),
     Input('save-dataset-threshold-dropdown', 'value'),
     Input('save-dataset-threshold-value', 'value')],
    [State('save-dataset-filename-input', 'value'),
     State('save-dataset-format-dropdown', 'value')]
)
def save_file(n_clicks, threshold_unit, threshold_val, filename, file_format):
    if n_clicks > 0 and filename and file_format and threshold_val:
        dataframe = df
        dataframe["Threshold"] = str(threshold_val) + " " + threshold_unit

        dataframe['Available'] = False
        # setting availability based on time el
        for ind in dataframe.index:
            curr = datetime.now()

            if threshold_unit == 'years':
                if math.ceil((curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')).days / 365) > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True


            elif threshold_unit == 'months':
                if math.ceil((curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')).days / 30) > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True


            elif threshold_unit == 'days':
                if (curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                             '%Y-%m-%dT%H:%M:%S.%fZ')).days > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True


            elif threshold_unit == 'hours':
                if math.ceil((curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() / 3600) > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True


            elif threshold_unit == 'minutes':
                if math.ceil((curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                                       '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() / 60) > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True


            elif threshold_unit == 'seconds':
                if (curr - datetime.strptime(dataframe.loc[ind, 'Timestamp'],
                                             '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds() > threshold_val:
                    dataframe.loc[ind, 'Available'] = False
                else:
                    dataframe.loc[ind, 'Available'] = True

        if file_format == 'csv':
            return [dcc.send_data_frame(dataframe.to_csv, f'{filename}.csv', index=False), 0]
        elif file_format == 'json':
            return [dcc.send_data_frame(dataframe.to_json, f'{filename}.json', orient='records'), 0]

    else:
        raise PreventUpdate()


if __name__ == '__main__':
    app.run_server(debug=True)
