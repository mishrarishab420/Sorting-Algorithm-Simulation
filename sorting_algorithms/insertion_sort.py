# insertion_sort.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np

# Insertion Sort Algorithm with Step-by-Step Animation
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Step 1: Highlight comparison (both elements move up)
        yield arr.copy(), j, i, "move_up", f"Compare {arr[j]} and {key}"

        while j >= 0 and key < arr[j]:
            # Step 2: Pause in the up position while comparing
            yield arr.copy(), j, j + 1, "compare", f"Comparing {arr[j]} and {key}"
            
            # Step 3: If the key is smaller, swap positions horizontally
            yield arr.copy(), j, j + 1, "swap_horizontal", f"Swapping {arr[j]} and {key}"
            
            # Step 4: Shift elements right
            arr[j + 1] = arr[j]
            yield arr.copy(), j, j + 1, "shift", f"Shifting {arr[j]} to the right"
            j -= 1

        # Step 5: Place the key at its correct position
        arr[j + 1] = key
        yield arr.copy(), j + 1, i, "place", f"Placing {key} in its correct position"

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
                className="w-100 m-0 p-0"
            ),
            
            # Buttons for Start, Restart, and Back
            dbc.Row(
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Button(
                                "Start Sorting",
                                id="insertion-start-button",
                                color="primary",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Restart Sorting",
                                id="insertion-restart-button",
                                color="warning",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Back",
                                id="insertion-back-button",
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
                    html.Div(id="insertion-array-container", style={"display": "flex", "justifyContent": "center", "alignItems": "flex-end", "height": "300px"}),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),
            
            # Step Explanation
            dbc.Row(
                dbc.Col(
                    html.Div(id="insertion-step-explanation", 
                             className="text-center mt-3", 
                             style={
                                "fontSize": "24px",
                                "fontWeight": "bold",
                                "transition": "opacity 0.5s ease-in-out",
                                "backgroundColor": "#f8f9fa",  # Light background color
                                "border": "2px solid #dee2e6",  # Border
                                "borderRadius": "10px",  # Rounded corners
                                "maxWidth": "80%",  # Limit width
                                "margin": "0 auto",  # Center horizontally
                                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Add shadow
                                "color": "#343a40"  # Dark text color
                             }
                        ),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),
            
            # Interval for Animation (slowed down to 1500ms)
            dcc.Interval(id="insertion-interval", interval=1500, n_intervals=0, disabled=True),
            
            # Store component to hold the array data
            dcc.Store(id="array-data-store")  
        ],
        className="p-0 m-0 w-100"
    )

# Callbacks for Insertion Sort
def register_insertion_callbacks(app):
    @app.callback(
        [Output("insertion-array-container", "children"),
         Output("insertion-interval", "disabled"),
         Output("array-data-store", "data"),
         Output("insertion-step-explanation", "children"),
         Output("insertion-step-explanation", "style")],
        [Input("insertion-interval", "n_intervals"),
         Input("insertion-start-button", "n_clicks"),
         Input("insertion-restart-button", "n_clicks"),
         Input("insertion-back-button", "n_clicks")],
        [State("insertion-array-container", "children"),
         State("insertion-interval", "disabled"),
         State("array-data-store", "data")],
        prevent_initial_call=False
    )
    def update_insertion_array(n_intervals, start_clicks, restart_clicks, back_clicks, current_children, interval_disabled, array_data):
        ctx = dash.callback_context

        # Debugging: Print triggered inputs
        print(f"Triggered: {ctx.triggered}")

        # Initialize array data if None
        if array_data is None:
            array_data = {
                "array_values": np.random.randint(1, 100, 10).tolist(),
                "steps": [],
                "current_step": 0,
                "box_ids": list(range(10))  # Initialize box_ids
            }
            print("Initialized array_data")

        arr = array_data["array_values"]
        steps = array_data.get("steps", [])
        current_step = array_data.get("current_step", 0)
        box_ids = array_data.get("box_ids", list(range(len(arr))))

        # Identify which button was clicked
        button_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        print(f"Button clicked: {button_id}")

        # Handle button clicks
        if button_id == "insertion-start-button" and start_clicks > 0:
            steps = list(insertion_sort(arr.copy()))  # Convert generator to list
            array_data["steps"] = steps
            array_data["current_step"] = 0
            interval_disabled = False
            print("Started sorting")
        elif button_id == "insertion-restart-button" and restart_clicks > 0:
            array_data = {
                "array_values": np.random.randint(1, 100, 10).tolist(),
                "steps": [],
                "current_step": 0,
                "box_ids": list(range(10))  # Reset box_ids
            }
            steps = list(insertion_sort(array_data["array_values"].copy()))  # Convert generator to list
            array_data["steps"] = steps
            interval_disabled = False
            print("Restarted sorting")
        elif button_id == "insertion-back-button" and back_clicks > 0:
            print("Back button clicked")
            return [], True, array_data, "Click Start Button for sorting visualization", {"fontSize": "20px", "opacity": 1}

        # Step through sorting animation
        step_explanation = "Click Start Button for sorting visualization"  # ✅ Default explanation
        explanation_style = {
            "fontSize": "24px",
            "fontWeight": "bold",
            "transition": "opacity 0.5s ease-in-out",
            "backgroundColor": "#f8f9fa",  # Light background color
            "border": "2px solid #dee2e6",  # Border
            "borderRadius": "10px",  # Rounded corners
            "maxWidth": "80%",  # Limit width
            "margin": "0 auto",  # Center horizontally
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Shadow
            "color": "#343a40"  # Dark text color
        }

        if start_clicks and start_clicks > 0:
            if not interval_disabled and steps:
                if current_step < len(steps):
                    sorted_arr, move_index, current_index, action, explanation = steps[current_step]

                    step_explanation = explanation  # ✅ Set explanation dynamically
                    array_data["current_step"] += 1  # Move to next step
                    print(f"Step: {explanation}")
                    print(f"box_ids: {box_ids}")

                    # ✅ Correct Swap Handling: Only Update box_ids
                    if action == "swap_horizontal":
                        box_ids[move_index], box_ids[current_index] = box_ids[current_index], box_ids[move_index]
                        array_data["box_ids"] = box_ids  # Update tracking of positions
                    
                else:
                    interval_disabled = True
                    step_explanation = "Sorting completed!"  # ✅ Final message
                    explanation_style["opacity"] = 1
                    print("Sorting completed")

        # Create boxes for the array elements
        boxes = []
        for idx, box_id in enumerate(box_ids):  
            value = array_data["array_values"][box_id]  # ✅ Correct way to get values
            box_style = {
                "width": "100px",
                "height": "100px",
                "border": "3px solid #000",
                "borderRadius": "50%",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "fontSize": "20px",
                "margin": "10px",
                "transition": "transform 1s ease-in-out",
            }

            # Apply animations based on sorting step
            if not interval_disabled and steps:
                if idx == current_index or idx == move_index:
                    if action == "move_up":
                        box_style["transform"] = "translateY(-80px)"
                        box_style["backgroundColor"] = "yellow"
                    elif action == "compare":
                        box_style["transform"] = "translateY(-80px)"
                        box_style["backgroundColor"] = "orange"
                    elif action == "swap_horizontal":
                        if idx == move_index:
                            box_style["transform"] = "translateX(-80px) translateY(-80px)"
                        elif idx == current_index:
                            box_style["transform"] = "translateX(80px) translateY(-80px)"
                        box_style["backgroundColor"] = "red"
                    elif action == "shift":
                        box_style["transform"] = "translateY(-80px)"
                        box_style["backgroundColor"] = "lightblue"
                    elif action == "place":
                        box_style["transform"] = "translateY(0px)"
                        box_style["backgroundColor"] = "lightgreen"

            boxes.append(html.Div(str(value), style=box_style))

        return boxes, interval_disabled, array_data, step_explanation, explanation_style