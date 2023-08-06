import dash
from dash import html, dcc, MATCH
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from MS_visualizer_lite.components.components import create_slider, \
    create_button, \
    create_dropdown, \
    create_plot, \
    create_radio_box, \
    create_min_max_input, \
    create_min_max_input_with_step, \
    create_checkbox, \
    create_headline_button, \
    create_searchable_dropdown

from examples.get_data import get_opentims_data, memoized_get_bounds, get_bounds
from MS_visualizer_lite.server import app
from MS_visualizer_lite.controller.func import get_data_path_options
from MS_visualizer_lite.assets.plotly_colors import css_colors

import plotly.express as px
import pathlib

# CONFIG
RT_START = 1200
RT_STOP = 1500
FRAME_START = 10
FRAME_STOP = 50
MZ_MIN = 550
MZ_MAX = 551
TOF_MIN = 196000
TOF_MAX = 200000
TRANSFORMED_MZ_MIN = 100
TRANSFORMED_MZ_MAX = 200
SCAN_MIN = 1
SCAN_MAX = 450
INV_ION_M_MIN = 0.6
INV_ION_M_MAX = 1.5
MIN_INTENSITY = 10

DEFAULT_PATH = "data/data.d"
BASE_PATH = "data/"

# DEFAULT_PATH = "/data/rawdata/gutamine/G2112/G211202_004_Slot1-1_1_3342.d"
# BASE_PATH = "/data/rawdata/gutamine/"


# Layout
visualizer = html.Div([

    # store if the graph shows the raw or clustered data
    dcc.Store(id="last_button_id"),

    html.Div(id="test", children=None),

    dcc.Download(id="json_download"),

    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([  # headline - H3 replaced with button to collapse row
                    # html.H3("Data:"),
                    create_headline_button({"type": "collapse_section_button", "index": 0}, "Data △")
                ], width=3, className="d-grid gap-2"),
                dbc.Col([  # settings column
                    dbc.Collapse([
                        dbc.Row([
                            html.Div(id="refresh_id"),
                            create_searchable_dropdown("data_path_id", "Path", get_data_path_options(BASE_PATH),
                                                       DEFAULT_PATH),
                            # create_searchable_dropdown("settings_options", "Saved Settings:", get_options()),
                            # create_checkbox("parameters_only", "",
                            #                 [{"label": "load only algorithm parameter", "value": True}], [True]),
                        ]),
                        html.Br(),
                        # create_button("load_settings", "Load from DB"),
                        html.Br(),
                        # create_textfield_input("json_settings", "Copy Json:", "Copy Json content here"),
                        # html.Br(),
                        # create_button("load_json_settings", "Load from Json"),
                        # html.Br(),
                    ], id={"type": "collapse_section_id", "index": 0}, is_open=True)
                ]),
            ]),
        ], className="input_group"),
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col([
                    # html.H3("Axes:"),  # headline
                    create_headline_button({"type": "collapse_section_button", "index": 1}, "Axes △")
                ], width=3, className="d-grid gap-2"),
                dbc.Col([  # settings column
                    dbc.Collapse([
                        html.Label("Select Axes for filtering:"),
                        html.Br(),
                        html.Br(),
                        create_radio_box("x_axis", "X Axis:",
                                         [{"label": "mz", "value": "mz"}, {"label": "tof", "value": "tof"},
                                          {"label": "transformed_mz", "value": "transformed_mz"}], "mz"),
                        create_radio_box("y_axis", "Y Axis:", [{"label": "retention_time", "value": "retention_time"},
                                                               {"label": "frame", "value": "frame"}], "retention_time"),
                        create_radio_box("z_axis", "Z Axis:",
                                         [{"label": "inv_ion_mobility", "value": "inv_ion_mobility"},
                                          {"label": "scan", "value": "scan"}], "scan"),
                        html.Br(),
                        html.Label("Select Axes shown in the graph:"),
                        html.Br(),
                        html.Br(),
                        create_radio_box("x_axis_graph", "X Axis:",
                                         [{"label": "mz", "value": "mz"}, {"label": "tof", "value": "tof"},
                                          {"label": "transformed_mz", "value": "transformed_mz"}], "mz"),
                        create_radio_box("y_axis_graph", "Y Axis:",
                                         [{"label": "retention_time", "value": "retention_time"},
                                          {"label": "frame", "value": "frame"}], "retention_time"),
                        create_radio_box("z_axis_graph", "Z Axis:",
                                         [{"label": "inv_ion_mobility", "value": "inv_ion_mobility"},
                                          {"label": "scan", "value": "scan"}], "scan"),
                        html.Br(),
                        # TODO implement resolution with transformed_mz
                        # create_slider("resolution", "resolution:", min_=5000, max_=150000, step=1000,
                        #               default_value=DEFAULT_RESOLUTION),
                    ], id={"type": "collapse_section_id", "index": 1}, is_open=True)
                ]),
            ]),
        ], className="input_group"),
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col([
                    # html.H3("MS-1 filter:"),  # headline
                    create_headline_button({"type": "collapse_section_button", "index": 2}, "MS-1 filter △")
                ], width=3, className="d-grid gap-2"),
                dbc.Col([  # settings column
                    dbc.Collapse([
                        dcc.Store(id="min_max_values_x", storage_type='session'),
                        dcc.Store(id="min_max_values_y", storage_type='session'),
                        dcc.Store(id="min_max_values_z", storage_type='session'),
                        html.Div(id="x_axis_value"),
                        html.Div(id="y_axis_value"),
                        html.Div(id="z_axis_value"),
                        html.Br(),
                        create_slider("min_intensity", "min intensity:", default_value=MIN_INTENSITY, min_=0, max_=500),
                        create_checkbox("multiply_charged_only", "", [{"label": "multiply charged only", "value": True}], []),
                    ], id={"type": "collapse_section_id", "index": 2}, is_open=True)
                ]),
            ]),
        ], className="input_group"),
        html.Br(),

        html.Div([
            dbc.Row([
                dbc.Col([
                    # html.H3("MS-1 Points:"),  # headline
                    create_headline_button({"type": "collapse_section_button", "index": 3}, "MS-1 Points △")
                ], width=3, className="d-grid gap-2"),
                dbc.Col([  # settings column
                    dbc.Collapse([
                        dbc.Row([
                            dbc.Col(
                                create_slider("opacity", "opacity:", min_=0.1, max_=1, step=0.1, default_value=0.5), ),
                            dbc.Col(create_slider("point_size", "point size:", min_=0.1, max_=5, step=0.1,
                                                  default_value=2.5), ),
                        ]),
                        dbc.Row([
                            dbc.Col(create_dropdown("color_scale", "color scale:",
                                                    [{"label": i, "value": i} for i in
                                                     sorted(px.colors.named_colorscales())],
                                                    value="inferno")),
                            dbc.Col(create_dropdown("paper_bgcolor", "Graph background color:",
                                                    [{"label": i, "value": i} for i in css_colors],
                                                    value="lightsteelblue")),
                        ]),
                        html.Br(),
                        create_button("plot-raw-data-button", "Plot Raw Data", disabled=True),
                    ], id={"type": "collapse_section_id", "index": 3}, is_open=True)
                ]),
            ]),
        ], className="input_group"),
        html.Br(),


    ], className="group input"),

    html.Div([
        html.Div([  # output div - will show the graph
            html.Div(id="graph_output"),
        ], className="graph"),
        html.Br(),
        html.Div([  # output div - will show the graph
            html.Div(id="table_output"),
        ], className="table"),
    ], className="group output")

], className="page_group")


# Callbacks

@app.callback(
    Output({"type": "collapse_section_id", "index": MATCH}, "is_open"),
    Output({"type": "collapse_section_button", "index": MATCH}, "children"),
    Input({"type": "collapse_section_button", "index": MATCH}, "n_clicks"),
    State({"type": "collapse_section_id", "index": MATCH}, "is_open"),
    State({"type": "collapse_section_button", "index": MATCH}, "children"),
)
def toggle_collapse(n_clicks, is_open, button_text):
    if n_clicks != 0:
        if "△" in button_text:
            button_text = button_text.replace("△", "▽")
        elif "▽" in button_text:
            button_text = button_text.replace("▽", "△")
        else:
            pass
        return not is_open, button_text
    return is_open, button_text


@app.callback(
    Output("data_path_id", "options"),
    Input("data_path_id", "value"),
)
def reload_options(selected_data):
    return get_data_path_options(BASE_PATH)


# x axis selection
@app.callback(
    Output("x_axis_value", "children"),
    Output("x_axis", "value"),
    Output("min_max_values_x", "data"),
    Input("x_axis", "value"),
    State("data_path_id", "value"),
    State("min_max_values_x", "data"),
)
def update(value, data_path, min_max):
    ctx = dash.callback_context

    button_id = ctx.triggered[0]["prop_id"].split('.')[0]

    if min_max is not None:
        MIN = min_max["min"]
        MAX = min_max["max"]


    if data_path is None:
        data_path = DEFAULT_PATH

    data = memoized_get_bounds(data_path)

    if value == "mz":
        if button_id != "load_settings":
            MIN = MZ_MIN
            MAX = MZ_MAX
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("x_start", "x_stop", "number", "m/z:", min_=data["mz"][0], max_=data["mz"][1],
                                 default_value=[MIN, MAX]),
        ]), value, min_max
    elif value == "tof":
        if button_id != "load_settings":
            MIN = TOF_MIN
            MAX = TOF_MAX
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("x_start", "x_stop", "number", "tof:", min_=data["tof"][0], max_=data["tof"][1],
                                 default_value=[MIN, MAX]),
        ]), value, min_max
    else:
        if button_id != "load_settings":
            MIN = TRANSFORMED_MZ_MIN
            MAX = TRANSFORMED_MZ_MAX
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("x_start", "x_stop", "number", "transformed mz:",
                                 default_value=[MIN, MAX]),
        ]), value, min_max


# y axis selection
@app.callback(
    Output("y_axis_value", "children"),
    Output("y_axis", "value"),
    Output("min_max_values_y", "data"),
    Input("y_axis", "value"),
    State("data_path_id", "value"),
    State("min_max_values_y", "data"),
)
def update(value, data_path, min_max):
    ctx = dash.callback_context

    button_id = ctx.triggered[0]["prop_id"].split('.')[0]

    if min_max is not None:
        MIN = min_max["min"]
        MAX = min_max["max"]

    if data_path is None:
        data_path = DEFAULT_PATH

    data = memoized_get_bounds(data_path)

    if value == "retention_time":
        if button_id != "load_settings":
            MIN = round(RT_START / 60, 3)
            MAX = round(RT_STOP / 60, 3)
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("y_start", "y_stop", "number", "Rt:", min_=round(data["retention_time"][0] / 60, 4),
                                 max_=round(data["retention_time"][1] / 60, 4),
                                 default_value=[MIN, MAX]),
        ]), value, min_max
    else:
        if button_id != "load_settings":
            MIN = FRAME_START
            MAX = FRAME_STOP
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("y_start", "y_stop", "number", "Frame:", min_=data["frame"][0],
                                 max_=data["frame"][1],
                                 default_value=[MIN, MAX]),
        ]), value, min_max


# z axis selection
@app.callback(
    Output("z_axis_value", "children"),
    Output("z_axis", "value"),
    Output("min_max_values_z", "data"),
    Output("plot-raw-data-button", "disabled"),
    Input("z_axis", "value"),
    State("data_path_id", "value"),
    State("min_max_values_z", "data"),
)
def update(value, data_path, min_max):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split('.')[0]

    if min_max is not None:
        MIN = min_max["min"]
        MAX = min_max["max"]

    if data_path is None:
        data_path = DEFAULT_PATH

    data = get_bounds(data_path)

    if value == "scan":
        if button_id != "load_settings":
            MIN = SCAN_MIN
            MAX = SCAN_MAX
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input("z_start", "z_stop", "number", "Scan:", min_=data["scan"][0],
                                 max_=data["scan"][1],
                                 default_value=[MIN, MAX]),
        ]), value, min_max, False
    else:
        if button_id != "load_settings":
            MIN = INV_ION_M_MIN
            MAX = INV_ION_M_MAX
            min_max = {"min": MIN, "max": MAX}
        return html.Div([
            create_min_max_input_with_step("z_start", "z_stop", "number", "inv ion mobility:",
                                           min_=data["inv_ion_mobility"][0],
                                           max_=data["inv_ion_mobility"][1],
                                           default_value=[MIN, MAX],
                                           step=0.1)
        ]), value, min_max, False


# button callback
@app.callback(
    Output("graph_output", "children"),
    Output("last_button_id", "data"),
    Output("table_output", "children"),

    Input("plot-raw-data-button", "n_clicks"),

    Input("opacity", "value"),
    Input("point_size", "value"),
    Input("color_scale", "value"),
    Input("paper_bgcolor", "value"),

    Input("x_axis_graph", "value"),
    Input("y_axis_graph", "value"),
    Input("z_axis_graph", "value"),

    State("multiply_charged_only", "value"),

    State("x_axis", "value"),
    State("y_axis", "value"),
    State("z_axis", "value"),

    State("data_path_id", "value"),
    State("x_start", "value"),
    State("x_stop", "value"),
    State("y_start", "value"),
    State("y_stop", "value"),
    State("z_start", "value"),
    State("z_stop", "value"),
    State("min_intensity", "value"),

    State("last_button_id", "data"),

    prevent_initial_call=True
)
# @cache.memoize(timeout=Timeout)
def graph_callback(raw_data_button, opacity, point_size, color_scale, paper_bgcolor,
                   x_axis_graph, y_axis_graph, z_axis_graph, multiply_charged_only,
                   x_axis, y_axis, z_axis, data_path, x_start, x_stop, y_start, y_stop, z_start, z_stop, min_intensity,
                   last_button_id):
    # check which callback triggered
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split('.')[0]
        if button_id == "plot-raw-data-button" or button_id == "plot_clustered_data":
            last_button_id = button_id

        data_path = pathlib.Path(data_path)

        # check if all start stop values are set correctly
        if x_start is None or x_stop is None or y_start is None or y_stop is None or z_start is None or z_stop is None:
            return "Not all values are set", last_button_id, ""
        if x_start >= x_stop or y_start >= y_stop or z_start >= z_stop:
            return "Supplied minimal value was greater or equal to the maximal value", last_button_id, ""

        if y_axis == "retention_time":
            # convert min to sec
            y_start = y_start * 60
            y_stop = y_stop * 60

        extents = {
            x_axis: (x_start, x_stop),
            y_axis: (y_start, y_stop),
            z_axis: (z_start, z_stop)
        }

        if multiply_charged_only:
            df = get_opentims_data(
                data_path=data_path,
                min_intensity=min_intensity,
                constraint="inv_ion_mobility <= 0.4467452 + 0.00101627*mz and inv_ion_mobility <= 0.5301116 + 0.000849*mz",
                **extents
            )
        else:
            df = get_opentims_data(
                data_path=data_path,
                min_intensity=min_intensity,
                **extents
            )


        if y_axis == "retention_time":
            # convert sec to min
            df["retention_time"] = df["retention_time"].map(lambda retention_time: retention_time / 60)

    if button_id == "plot-raw-data-button" or last_button_id == "plot-raw-data-button":

        if df.empty:
            return "No Data for selected Settings", last_button_id, ""
        else:

            return create_plot('data_plot', df, x_axis_graph, y_axis_graph, z_axis_graph, opacity, point_size,
                               color_scale,
                               paper_bgcolor), last_button_id, ""


    return "", last_button_id, ""
