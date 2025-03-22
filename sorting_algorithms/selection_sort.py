import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Selection Sort Algorithm with Step-by-Step Animation
def selection_sort_steps(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps.append(('compare', i, j, min_idx))  # Step 1: Compare elements
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            steps.append(('swap', i, min_idx))  # Step 2: Swap elements
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(('settle', i))  # Step 3: Mark element as settled
    return steps

# Layout for the Selection Sort Page
def selection_sort_layout():
    return html.Div(
        children=[
            # Header Section
            dbc.Row(
                dbc.Col(
                    html.H1("Selection Sort Visualization", className="text-center my-4"),
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
                    html.Div(id="array-container", style={"display": "flex", "justifyContent": "center", "alignItems": "flex-end", "height": "300px"}),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),

            # Step Explanation
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="step-explanation",
                        className="text-center mt-3 p-3",
                        style={
                            "fontSize": "24px",
                            "fontWeight": "bold",
                            "transition": "opacity 0.5s ease-in-out",
                            "backgroundColor": "#f8f9fa",  # Light background color
                            "border": "2px solid #dee2e6",  # Border
                            "borderRadius": "10px",  # Rounded corners
                            "maxWidth": "80%",  # Limit width
                            "margin": "0 auto"  # Center horizontally
                        }
                    ),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),

            # Current Smallest Element
            dbc.Row(
                dbc.Col(
                    html.Div(id="current-smallest", className="text-center mt-3", style={"fontSize": "18px", "color": "blue"}),
                    width=12
                ),
                className="w-100 m-0 p-0"
            ),

            # Interval for Animation (slowed down to 1500ms)
            dcc.Interval(id="interval", interval=1500, n_intervals=0, disabled=True),

            # Store component to hold the array data
            dcc.Store(id="array-data-store")
        ],
        className="p-0 m-0 w-100"  # Ensuring full width
    )

# Callbacks for Selection Sort
def register_selection_sort_callbacks(app):
    # Global variables
    global sorting_steps, global_array, original_array
    sorting_steps = []
    global_array = []
    original_array = []

    @app.callback(
        [Output("array-container", "children", allow_duplicate=True),
         Output("interval", "disabled", allow_duplicate=True),
         Output("array-data-store", "data", allow_duplicate=True),
         Output("step-explanation", "children", allow_duplicate=True),
         Output("current-smallest", "children", allow_duplicate=True)],
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
        global sorting_steps, global_array, original_array

        # Debugging
        print(f"Button ID: {ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None}")
        print(f"Array Data: {array_data}")
        print(f"Interval Disabled: {interval_disabled}")

        # Initialize or reset the array data
        if array_data is None:
            array_data = {"array_values": []}
            global_array = []
            sorting_steps = []
        else:
            global_array = array_data["array_values"].copy()

        # Identify which button was clicked
        if not ctx.triggered:
            button_id = None
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle button clicks
        if button_id == "start-button" and start_clicks > 0:
            sorting_steps = selection_sort_steps(global_array.copy())
            interval_disabled = False
        elif button_id == "restart-button" and restart_clicks > 0:
            global_array = array_data["array_values"].copy()
            sorting_steps = selection_sort_steps(global_array.copy())
            interval_disabled = False
        elif button_id == "back-button" and back_clicks > 0:
            return [], True, array_data, "", ""

        # Step through sorting animation
        step_explanation = ""
        smallest_text = ""
        compare_idx = None
        swap_idx = None
        is_swap = False
        settled = None
        min_idx = None

        if not interval_disabled and sorting_steps:
            if n_intervals < len(sorting_steps):
                step = sorting_steps[n_intervals]
                if step[0] == 'compare':
                    step_explanation = f"Comparing {global_array[step[1]]} and {global_array[step[2]]}. Current smallest: {global_array[step[3]]}"
                    compare_idx = step[1]
                    swap_idx = step[2]
                    min_idx = step[3]
                elif step[0] == 'swap':
                    global_array[step[1]], global_array[step[2]] = global_array[step[2]], global_array[step[1]]
                    step_explanation = f"Swapping {global_array[step[2]]} and {global_array[step[1]]}"
                    compare_idx = step[1]
                    swap_idx = step[2]
                    is_swap = True
                elif step[0] == 'settle':
                    step_explanation = f"{global_array[step[1]]} is now in its correct position."
                    settled = step[1]
            else:
                interval_disabled = True
                step_explanation = "Sorting completed!"

        # Create boxes for the array elements
        boxes = create_array_boxes(global_array, compare_idx, swap_idx, is_swap, settled, min_idx)

        # Update the array data store
        array_data["array_values"] = global_array

        return boxes, interval_disabled, array_data, step_explanation, smallest_text

    # Function to create array boxes with optional highlighting
    def create_array_boxes(arr, compare_idx=None, swap_idx=None, is_swap=False, settled=None, min_idx=None):
        boxes = []
        for i, value in enumerate(arr):
            style = {
                "width": "100px",
                "height": "100px",
                "border": "3px solid #000",
                "borderRadius": "50%",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "fontSize": "20px",
                "margin": "10px",
                "transition": "transform 0.5s, background-color 0.5s"
            }
            if compare_idx is not None and (i == compare_idx or i == swap_idx):
                style["backgroundColor"] = "#ffcccb"  # Light red for comparison
            if is_swap and (i == compare_idx or i == swap_idx):
                style["backgroundColor"] = "red"  # Red for swapping
                style["transform"] = "translateY(20px)"
            if settled is not None and i <= settled:
                style["backgroundColor"] = "#90EE90"  # Light green for settled
            if min_idx is not None and i == min_idx:
                style["backgroundColor"] = "#add8e6"  # Light blue for the smallest found so far
            boxes.append(html.Div(str(value), style=style))
        return boxes