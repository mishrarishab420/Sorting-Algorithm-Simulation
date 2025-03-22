import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import random

# Quick Sort Algorithm with Step-by-Step Animation
def quick_sort_steps(arr):
    steps = []

    def quick_sort_helper(arr, low, high):
        if low < high:
            # Partition the array and get the pivot index
            pivot_idx = partition(arr, low, high, steps)
            # Recursively sort the subarrays
            quick_sort_helper(arr, low, pivot_idx - 1)
            quick_sort_helper(arr, pivot_idx + 1, high)

    def partition(arr, low, high, steps):
        pivot = arr[high]  # Choose the last element as the pivot
        steps.append(('pivot', high))  # Highlight the pivot
        i = low - 1  # Index of the smaller element

        for j in range(low, high):
            steps.append(('compare', j, high))  # Compare with pivot
            if arr[j] < pivot:
                i += 1
                if i != j:
                    steps.append(('swap', i, j))  # Swap elements
                    arr[i], arr[j] = arr[j], arr[i]
        if i + 1 != high:
            steps.append(('swap', i + 1, high))  # Swap pivot into place
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(('settle', i + 1))  # Pivot is now in its correct position
        return i + 1

    quick_sort_helper(arr, 0, len(arr) - 1)
    return steps

# Layout for the Quick Sort Page
def quick_sort_layout():
    return html.Div(
        children=[
            # Header Section
            dbc.Row(
                dbc.Col(
                    html.H1("Quick Sort Visualization", className="text-center my-4"),
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
                                id="quick-sort-start-button",
                                color="primary",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Restart Sorting",
                                id="quick-sort-restart-button",
                                color="warning",
                                className="btn-block mb-3",
                                n_clicks=0
                            ),
                            dbc.Button(
                                "Back",
                                id="quick-sort-back-button",
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
                    html.Div(id="quick-sort-array-container", style={"display": "flex", "justifyContent": "center", "alignItems": "flex-end", "height": "300px"}),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),

            # Step Explanation
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="quick-sort-step-explanation",
                        className="text-center mt-3 p-3",
                        style={
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
                    ),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),

            # Interval for Animation (slowed down to 1500ms)
            dcc.Interval(id="quick-sort-interval", interval=1500, n_intervals=0, disabled=True),

            # Store component to hold the array data
            dcc.Store(id="array-data-store")
        ],
        className="p-0 m-0 w-100"
    )

# Callbacks for Quick Sort
def register_quick_sort_callbacks(app):
    @app.callback(
        [Output("quick-sort-array-container", "children", allow_duplicate=True),
         Output("quick-sort-interval", "disabled", allow_duplicate=True),
         Output("array-data-store", "data", allow_duplicate=True),
         Output("quick-sort-step-explanation", "children", allow_duplicate=True),
         Output("quick-sort-step-explanation", "style", allow_duplicate=True)],
        [Input("quick-sort-interval", "n_intervals"),
         Input("quick-sort-start-button", "n_clicks"),
         Input("quick-sort-restart-button", "n_clicks"),
         Input("quick-sort-back-button", "n_clicks")],
        [State("quick-sort-array-container", "children"),
         State("quick-sort-interval", "disabled"),
         State("array-data-store", "data")],
        prevent_initial_call=True
    )
    def update_quick_sort_array(n_intervals, start_clicks, restart_clicks, back_clicks, current_children, interval_disabled, array_data):
        ctx = dash.callback_context

        # Initialize array data if None
        if array_data is None:
            array_data = {
                "array_values": [random.randint(1, 100) for _ in range(10)],
                "steps": [],
                "current_step": 0
            }

        arr = array_data["array_values"]
        steps = array_data.get("steps", [])
        current_step = array_data.get("current_step", 0)

        # Identify which button was clicked
        button_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

        # Handle button clicks
        if button_id == "quick-sort-start-button" and start_clicks > 0:
            steps = quick_sort_steps(arr.copy())
            array_data["steps"] = steps
            array_data["current_step"] = 0
            interval_disabled = False
        elif button_id == "quick-sort-restart-button" and restart_clicks > 0:
            array_data = {
                "array_values": [random.randint(1, 100) for _ in range(10)],
                "steps": [],
                "current_step": 0
            }
            steps = quick_sort_steps(array_data["array_values"].copy())
            array_data["steps"] = steps
            interval_disabled = False
        elif button_id == "quick-sort-back-button" and back_clicks > 0:
            return [], True, array_data, "", {"fontSize": "20px", "opacity": 0}

        # Step through sorting animation
        step_explanation = "Click Start Button for sorting visualization"
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
                    step = steps[current_step]
                    action = step[0]

                    if action == 'pivot':
                        step_explanation = f"Selected pivot: {arr[step[1]]}"
                    elif action == 'compare':
                        step_explanation = f"Comparing {arr[step[1]]} with pivot {arr[step[2]]}"
                    elif action == 'swap':
                        arr[step[1]], arr[step[2]] = arr[step[2]], arr[step[1]]
                        step_explanation = f"Swapping {arr[step[1]]} and {arr[step[2]]}"
                    elif action == 'settle':
                        step_explanation = f"Pivot {arr[step[1]]} is now in its correct position."

                    array_data["current_step"] += 1
                else:
                    interval_disabled = True
                    step_explanation = "Sorting completed!"
                    explanation_style["opacity"] = 1

        # Create boxes for the array elements
        boxes = []
        for idx, value in enumerate(arr):
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
                if current_step < len(steps):
                    step = steps[current_step]
                    if step[0] == 'pivot' and idx == step[1]:
                        box_style["backgroundColor"] = "yellow"
                    elif step[0] == 'compare' and (idx == step[1] or idx == step[2]):
                        box_style["backgroundColor"] = "orange"
                    elif step[0] == 'swap' and (idx == step[1] or idx == step[2]):
                        box_style["backgroundColor"] = "red"
                        box_style["transform"] = "translateY(-80px)"
                    elif step[0] == 'settle' and idx == step[1]:
                        box_style["backgroundColor"] = "lightgreen"

            boxes.append(html.Div(str(value), style=box_style))

        return boxes, interval_disabled, array_data, step_explanation, explanation_style