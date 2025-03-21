import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Initialize the Dash app for this page
home_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Home page layout
home_layout = html.Div(
    children=[
        # Header Section
        dbc.Row(
            dbc.Col(
                html.H1("Sorting Algorithm Simulation", className="text-center my-5 fade-in"),
                width={"size": 8, "offset": 2}
            )
        ),
        
        # Algorithm Selection Buttons
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.H3("Select a Sorting Algorithm", className="text-center mb-4 fade-in"),
                        html.Div(
                            className="button-grid",
                            children=[
                                dbc.Button("Quick Sort", color="primary", className="btn-block fade-in", href="/input-array?method=quick-sort"),
                                dbc.Button("Selection Sort", color="success", className="btn-block fade-in", href="/input-array?method=selection-sort"),
                                dbc.Button("Insertion Sort", color="warning", className="btn-block fade-in", href="/input-array?method=insertion-sort")
                            ]
                        )
                    ],
                    className="container-glass text-center p-4"
                ),
                width={"size": 8, "offset": 2}
            )
        ),
        
        # Footer or Information Section (Optional)
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Select the sorting algorithm to visualize and learn how it works!", className="text-center mt-4 fade-in")
                    ]
                ),
                width={"size": 8, "offset": 2}
            )
        )
    ],
    className="p-4"
)

# Set the layout of the app
home_app.layout = home_layout

# If this is the only page being rendered, this line is typically used to run the page independently
if __name__ == "__main__":
    home_app.run_server(debug=True)