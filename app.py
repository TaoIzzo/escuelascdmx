# import dash
#
# app = dash.Dash(__name__, suppress_callback_exceptions=True)
# server = app.server
import dash

app = dash.Dash(__name__,
                title="IEBS PROYECTO")
app.title="IEBS PROYECTO"
server = app.server
