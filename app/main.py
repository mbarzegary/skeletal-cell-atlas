from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app, settings, server
from app.apps import atlas, upload
from healthcheck import HealthCheck

health = HealthCheck()
server.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())

app.title = "Skeletal Cell Atlas"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return atlas.layout
    elif pathname == '/upload':
        return upload.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True, port=settings.get('SERVER_PORT'))
