import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import layouts & callbacks
from pages.home import home_layout
from pages.input_array import input_array_layout, register_callbacks
from pages.simulation import simulation_layout

# Initialize the Dash app with Bootstrap
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True
)

# Create the Flask server for deployment
server = app.server

# Define app layout with navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='container')  # Central container for page content
])

# Callback to handle routing between pages
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ['/', '/home']:
        return home_layout
    elif pathname == '/input-array':
        return input_array_layout
    elif pathname == '/simulation':
        return simulation_layout
    else:
        return html.Div(
            [
                html.H3("404 - Page Not Found", className="text-center mt-5"),
                html.A("Go Back to Home", href="/home", className="btn btn-primary d-block mx-auto mt-3")
            ],
            className="text-center"
        )

# Register input array callbacks
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)