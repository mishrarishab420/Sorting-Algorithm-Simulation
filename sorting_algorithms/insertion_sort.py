import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import numpy as np

# Insertion Sort Algorithm with Step-by-Step Animation
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Step 1: Highlight comparison (both elements move up)
        yield arr.copy(), j, i, "move_up"

        while j >= 0 and key < arr[j]:
            # Step 2: Pause in the up position while comparing
            yield arr.copy(), j, j + 1, "compare"
            
            # Step 3: If the key is smaller, swap positions horizontally
            yield arr.copy(), j, j + 1, "swap_horizontal"
            
            # Step 4: Shift elements right
            arr[j + 1] = arr[j]
            yield arr.copy(), j, j + 1, "shift"
            j -= 1

        # Step 5: Place the key at its correct position
        arr[j + 1] = key
        yield arr.copy(), j + 1, i, "place"

# Layout for the Insertion Sort Page
def insertion_sort_layout():
    return html.Div(
        children=[
            # Header Section
            dbc.Row(
                dbc.Col(
                    html.H1("Insertion Sort Visualization", className="text-center my-4"), 
                    width=12
                ),
                className="w-100 m-0 p-0"  # Ensuring full width
            ),
            
            # Buttons for Start, Restart, and Back
            dbc.Row(
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Button(
                                "Start Sorting",
                                id="start-button",
                                color="primary",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Restart Sorting",
                                id="restart-button",
                                color="warning",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Back",
                                id="back-button",
                                href="/",
                                color="secondary",
                                className="btn-block mb-3"
                            ),
                        ],
                        className="text-center"
                    ),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),
            
            # Dynamic Array Display
            dbc.Row(
                dbc.Col(
                    html.Div(id="array-container", className="input-array-box-container"),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),
            
            # Interval for Animation
            dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
            
         dcc.Store(id="array-data-store")  
        ],
        className="p-0 m-0 w-100"  # Ensuring full width
    )

# Callbacks for Insertion Sort
def register_callbacks(app):
    @app.callback(
        [Output("array-container", "children"),
        Output("interval", "disabled"),
        Output("array-data-store", "data", allow_duplicate=True)],  # Allow duplicate output
        [Input("interval", "n_intervals"),
        Input("start-button", "n_clicks"),
        Input("restart-button", "n_clicks"),
        Input("back-button", "n_clicks")],
        [State("array-container", "children"),
        State("interval", "disabled"),
        State("array-data-store", "data")],
        prevent_initial_call=True
    )
    
    def update_array(n_intervals, start_clicks, restart_clicks, back_clicks, current_children, interval_disabled, array_data):
        ctx = dash.callback_context
        global sort_generator

        # Identify which button was clicked
        if not ctx.triggered:
            button_id = None
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Initialize or reset the array data
        if array_data is None:
            array_data = {"array_values": np.random.randint(1, 100, 10).tolist()}

        arr = array_data["array_values"]
        array_boxes = [
        html.Div(str(value), className="array-box") for value in arr
    ]

        # Handle button clicks
        if button_id == "start-button" and start_clicks > 0:
            sort_generator = insertion_sort(arr.copy())
            interval_disabled = False
        elif button_id == "restart-button" and restart_clicks > 0:
            sort_generator = insertion_sort(arr.copy())
            interval_disabled = False
        elif button_id == "back-button" and back_clicks > 0:
            return [], True, array_data  # Reset and go back

        # Step through sorting animation
        if not interval_disabled and sort_generator is not None:
            try:
                sorted_arr, move_index, current_index, action = next(sort_generator)
                array_data["array_values"] = sorted_arr  # Update stored array
            except StopIteration:
                interval_disabled = True

        # Create boxes for the array elements
        boxes = []
        for idx, value in enumerate(arr):
            box_style = {
                "width": "50px",
                "height": "50px",
                "border": "2px solid black",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "margin": "5px",
                "backgroundColor": "skyblue",
                "fontSize": "20px",
                "position": "relative",
                "transition": "transform 1s ease-in-out",
            }

            # Apply animations based on sorting step
            if not interval_disabled and sort_generator is not None:
                if idx == current_index or idx == move_index:
                    if action == "move_up":
                        box_style["transform"] = "translateY(-100px)"
                        box_style["backgroundColor"] = "yellow"
                    elif action == "compare":
                        box_style["transform"] = "translateY(-100px)"
                        box_style["backgroundColor"] = "orange"
                    elif action == "swap_horizontal":
                        if idx == move_index:
                            box_style["transform"] = "translateX(-100px) translateY(-100px)"
                        elif idx == current_index:
                            box_style["transform"] = "translateX(100px) translateY(-100px)"
                        box_style["backgroundColor"] = "red"
                    elif action == "shift":
                        box_style["transform"] = "translateY(-100px)"
                        box_style["backgroundColor"] = "lightblue"
                    elif action == "place":
                        box_style["transform"] = "translateY(0px)"
                        box_style["backgroundColor"] = "lightgreen"

            boxes.append(html.Div(str(value), style=box_style))

        return boxes, interval_disabled, array_data