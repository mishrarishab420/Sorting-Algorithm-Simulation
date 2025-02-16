from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Input Array page layout
input_array_layout = html.Div(
    children=[
        # Header Section
        dbc.Row(
            dbc.Col(
                html.H1("Input Array for Sorting", className="text-center my-5"),
                width=12,
                style={"textAlign": "center"}
            )
        ),
        
        # Input Form for the number of elements
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        # Header
                        html.H3("Number of Elements (5 to 15)", className="text-center mb-4"),
                        
                        # Input Box
                        dcc.Input(
                            id='num-elements-input',
                            type='number',
                            min=5,
                            max=15,
                            placeholder='Enter a number between 5 and 15',
                            className='mb-3',
                            style={'width': '100%', 'textAlign': 'center'}
                        ),
                        
                        # Generate Array Button
                        dbc.Button(
                            "Generate Array Inputs",
                            id='generate-array-button',
                            color="primary",
                            className="btn-block mb-3",
                            n_clicks=0  # Initialize n_clicks to 0
                        )
                    ],
                    className="text-center"
                ),
                width={"size": 6, "offset": 3}
            )
        ),
        
        # Dynamic Array Input Boxes (Initially Empty)
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='array-input-container',
                    className="input-array-box-container"
                ),
                width={"size": 6, "offset": 3}
            )
        ),
        
        # Submit Button
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        dbc.Button(
                            "Submit",
                            id='submit-button',
                            color="success",
                            className="btn-block mt-4",
                            disabled=True,  # Disabled by default
                            href="/simulation"
                        )
                    ],
                    className="text-center"
                ),
                width={"size": 6, "offset": 3}
            )
        ),
        
        # Footer or Information Section (Optional)
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Enter the array elements and click 'Submit' to visualize the sorting algorithm.", className="text-center mt-4")
                    ]
                ),
                width={"size": 6, "offset": 3}
            )
        )
    ]
)

# Callback to generate array input boxes dynamically and enable the submit button
def register_callbacks(app):
    @app.callback(
        Output('array-input-container', 'children'),
        Output('submit-button', 'disabled'),
        Input('generate-array-button', 'n_clicks'),
        State('num-elements-input', 'value'),
        prevent_initial_call=True  # Prevent the callback from firing on page load
    )
    def generate_array_inputs(n_clicks, num_elements):
        # Check if the number of elements is valid
        if not num_elements or num_elements < 5 or num_elements > 15:
            return [], True  # No inputs and disable submit button if the input is invalid
        
        # Generate input boxes based on the entered number
        inputs = []
        for i in range(num_elements):
            inputs.append(
                dcc.Input(
                    id={'type': 'array-input', 'index': i},
                    type='number',
                    placeholder=f'Element {i + 1}',
                    className='mb-3',
                    style={'width': '100%', 'text-align': 'center'},
                    min=10,  # Restrict to two-digit numbers
                    max=99,
                    maxLength=2
                )
            )
        
        return inputs, False  # Return the input boxes and enable submit button

    # Callback to ensure two-digit input and auto-focus to the next input box
    @app.callback(
        Output({'type': 'array-input', 'index': ALL}, 'value'),
        Output({'type': 'array-input', 'index': ALL}, 'n_submit'),
        Input({'type': 'array-input', 'index': ALL}, 'value'),
        State({'type': 'array-input', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def enforce_two_digit_and_autofocus(values, ids):
        # Enforce two-digit number validation
        updated_values = list(values)
        n_submit_list = [None] * len(values)  # Initialize empty submit list

        for i, val in enumerate(values):
            if val is not None and (val < 10 or val > 99):
                updated_values[i] = None  # Reset invalid input
            elif val is not None and 10 <= val <= 99 and i < len(values) - 1:
                n_submit_list[i + 1] = 1  # Auto-submit to move focus to the next box

        return updated_values, n_submit_list