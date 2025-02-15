import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import the layouts for each page
from pages.home import home_layout
from pages.input_array import input_array_layout
from pages.simulation import simulation_layout

# Initialize the main app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create server
server = app.server

# Main app layout with routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='container')  # Added 'container' class for layout styling
])

# Callback for page routing
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/input-array':
        return input_array_layout
    elif pathname == '/simulation':
        return simulation_layout
    else:
        return html.H3('404 Page not found')

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
