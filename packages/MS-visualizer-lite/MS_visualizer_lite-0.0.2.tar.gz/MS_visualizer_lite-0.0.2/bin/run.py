# dash things
from dash import dcc, html
from dash.dependencies import Input, Output

# import app
from MS_visualizer_lite.server import app

# import components
from MS_visualizer_lite.components.components import create_navbar

# import other pages
from MS_visualizer_lite.view.home import home
from MS_visualizer_lite.view.visualizer import visualizer


# dictionary to create the page according to the url
href2app = {
    "/": home,
    "/visualizer": visualizer,
}

# create the Layout
app.layout = html.Div(id='master-page')


@app.callback(
    Output('master-page', 'children'),
    Input('master-page', 'children'),
)
def create_page(child):
    content = html.Div(id="page-content")

    current_user = app.settings['user']
    if current_user == "devel":
        return html.Div([dcc.Location(id="url"),
                         create_navbar(),
                         html.Br(),
                         content,
                         dcc.Store(id='data-filter-settings', storage_type="session")])

    else:
        return html.Div()


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page_content(pathname):
    return href2app[pathname]


# start the server
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8040
    )
