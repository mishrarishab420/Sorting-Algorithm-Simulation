import dash
from dash import dcc, html, Input, Output, State
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

# Generate random data
def generate_random_array(n):
    return np.random.randint(1, 100, n)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Insertion Sort Visualization", style={"textAlign": "center"}),
    html.Div([
        html.Button("Start Sorting", id="start-button", n_clicks=0),
        html.Button("Restart Sorting", id="restart-button", n_clicks=0),
        html.Button("Generate New Array", id="new-array-button", n_clicks=0),
    ], style={"textAlign": "center", "marginBottom": "20px"}),
    html.Div(id="array-container", style={"display": "flex", "justifyContent": "center", "alignItems": "flex-end", "height": "300px"}),
    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
])

# Global variables
arr = generate_random_array(10)
box_ids = list(range(len(arr)))  # Unique IDs for each box
sort_generator = insertion_sort(arr.copy())

# Callback to update sorting visualization
@app.callback(
    [Output("array-container", "children"),
     Output("interval", "disabled")],
    [Input("interval", "n_intervals"),
     Input("start-button", "n_clicks"),
     Input("restart-button", "n_clicks"),
     Input("new-array-button", "n_clicks")],
    [State("array-container", "children"),
     State("interval", "disabled")]
)
def update_array(n_intervals, start_clicks, restart_clicks, new_array_clicks, current_children, interval_disabled):
    ctx = dash.callback_context
    global arr, box_ids, sort_generator

    # Identify which button was clicked
    if not ctx.triggered:
        button_id = "start-button"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "start-button" and start_clicks > 0:
        sort_generator = insertion_sort(arr.copy())
        interval_disabled = False
    elif button_id == "restart-button" and restart_clicks > 0:
        sort_generator = insertion_sort(arr.copy())
        interval_disabled = False
    elif button_id == "new-array-button" and new_array_clicks > 0:
        arr = generate_random_array(10)
        box_ids = list(range(len(arr)))  # Reset box IDs
        sort_generator = insertion_sort(arr.copy())
        interval_disabled = True

    # Step through sorting animation
    if not interval_disabled:
        try:
            sorted_arr, move_index, current_index, action = next(sort_generator)
        except StopIteration:
            interval_disabled = True

    # Create boxes for the array elements
    boxes = []
    for idx, box_id in enumerate(box_ids):
        value = arr[box_id]
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
        if not interval_disabled:
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

    # Update box positions after swap
    if not interval_disabled and action == "swap_horizontal":
        box_ids[move_index], box_ids[current_index] = box_ids[current_index], box_ids[move_index]

    return boxes, interval_disabled

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
