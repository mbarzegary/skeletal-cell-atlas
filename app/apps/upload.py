import base64
import os
from urllib.parse import quote as urlquote

from app import app, server, settings
from flask import send_from_directory

import dash
import dash_uploader as du
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

UPLOAD_DIRECTORY = os.path.abspath(settings.get('DATA_PATH'))
du.configure_upload(app, UPLOAD_DIRECTORY, use_upload_id=False)
PASSWORD = settings.get('UPLOAD_PASSWORD')

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


layout = html.Div(
    [
        html.H1("File Browser"),
        html.H2("Login"),
        dcc.Input(placeholder='password', id='password', type='password'),
        html.Button('Login', id='submit'),
        html.H2("Upload"),
        du.Upload(id='dash-uploader',max_file_size=21000),
        html.H2("File List"),
        html.Ul(id="file-list"),
    ]
)

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("dash-uploader", "isCompleted"),
     Input("submit", "n_clicks")],
    [State("dash-uploader", "fileNames"),
     State("password", "value")],
)
def update_output(upload_done, n_clicks, file_names, password):
    """Save uploaded files and regenerate the file list."""

    if (password != PASSWORD):
        if (upload_done): # remove uploaded files
            for filename in file_names:
                os.remove(UPLOAD_DIRECTORY + filename)
        return [html.Div("Not logged in!")]

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
