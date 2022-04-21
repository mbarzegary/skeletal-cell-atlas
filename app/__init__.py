import dash
from app.settings import settings


app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
