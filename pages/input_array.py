import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Updated Input Array Page Layout (Full Width Fix)
input_array_layout = html.Div(
    children=[
        # Header Section
        dbc.Row(
            dbc.Col(
                html.H1("Input Array for Sorting", className="text-center my-4"), 
                width=12
            ),
            className="w-100 m-0 p-0"  # Ensuring full width
        ),
        
        # Input Form for the number of elements
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.H3("Number of Elements (5 to 15)", className="text-center mb-4"),
                        dcc.Input(
                            id='num-elements-input',
                            type='number',
                            min=5,
                            max=15,
                            placeholder='No. of Array Elements',
                            className='mb-3',
                            style={'width': '100%', 'textAlign': 'center', 'fontWeight': '600'}
                        ),
                        dbc.Button(
                            "Generate Array Inputs",
                            id='generate-array-button',
                            color="primary",
                            className="btn-block mb-3",
                            n_clicks=0
                        )
                    ],
                    className="text-center"
                ),
                width=12
            ),
            className="w-100 m-0 p-0"  # Full width fix
        ),
        
        # Dynamic Array Input Boxes
        dbc.Row(
            dbc.Col(
                html.Div(id='array-input-container', className="input-array-box-container"),
                width=12
            ),
            className="w-100 m-0 p-0"
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
                            disabled=True
                        )
                    ],
                    className="text-center"
                ),
                width=12
            ),
            className="w-100 m-0 p-0"
        ),
        
        # Back Button
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        dbc.Button(
                            "Back",
                            href="/",
                            color="secondary",
                            className="btn-block mt-3"
                        )
                    ],
                    className="text-center"
                ),
                width=12
            ),
            className="w-100 m-0 p-0"
        ),
        
        # Footer or Information Section
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Enter the array elements and click 'Submit' to visualize the sorting algorithm.", 
                               className="text-center mt-4")
                    ]
                ),
                width=12
            ),
            className="w-100 m-0 p-0"
        ),

        # Store component to hold the array data
        dcc.Store(id='array-data-store')
    ],
    className="p-0 m-0 w-100"  # Ensuring full width
)

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
        prevent_initial_call=True
    )
    def enforce_two_digit_and_autofocus(values):
        if not values:
            raise PreventUpdate  # Avoid unnecessary updates

        updated_values = list(values)  # Copy of values to modify
        n_submit_list = [None] * len(values)  # Initialize n_submit list

        for i, val in enumerate(values):
            if val is not None and (val < 10 or val > 99):
                updated_values[i] = None  # Reset invalid input
            elif val is not None and 10 <= val <= 99 and i < len(values) - 1:
                n_submit_list[i + 1] = 1  # Auto-focus on the next box

        return updated_values, n_submit_list  # ✅ Ensure correct return values

    # Callback to store array data and redirect to the sorting page
    @app.callback(
    Output('array-data-store', 'data', allow_duplicate=True),  # Allow duplicate output
    Output('url', 'pathname'),
    Input('submit-button', 'n_clicks'),
    State({'type': 'array-input', 'index': ALL}, 'value'),
    State('num-elements-input', 'value'),
    State('url', 'search'),
    prevent_initial_call=True
)
    def store_array_data_and_redirect(n_clicks, array_values,num_elements,search):
        if not array_values or any(val is None for val in array_values):
            raise dash.exceptions.PreventUpdate


        # Store the array data in the dcc.Store component
        array_data = {
            'num_elements': num_elements,
            'array_values': array_values
        }

        # Extract Sorting Method from URL
        query_params = dict(param.split('=') for param in search.lstrip('?').split('&') if '=' in param)
        method = query_params.get("method", "")

        if method:
            return array_data, f"/sorting?num={num_elements}&method={method}"  # Redirect with sorting method
        else:
            return array_data, "/sorting"  # Redirect without sorting method