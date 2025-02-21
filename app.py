import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Import layouts & callbacks
from pages.home import home_layout
from pages.input_array import input_array_layout, register_callbacks as register_input_array_callbacks
from sorting_algorithms.insertion_sort import insertion_sort_layout, register_callbacks as register_insertion_sort_callbacks
from sorting_algorithms.merge_sort import merge_sort_layout#, register_callbacks as register_merge_sort_callbacks
from sorting_algorithms.quick_sort import quick_sort_layout#, register_callbacks as register_quick_sort_callbacks

# Initialize the Dash app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True
)

server = app.server

# Define app layout with navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='stored-method', storage_type='session', data=""),  # Store sorting method
    dcc.Store(id='array-data-store', storage_type='session'),  # Store array data
    html.Div(id='page-content', className='container')  # Central container for page content
])

# Callback to store sorting method before loading page
@app.callback(
    Output('stored-method', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False  # Ensures it runs immediately on page load
)
def store_method(search):
    if search:
        query_params = dict(param.split('=') for param in search.lstrip('?').split('&') if '=' in param)
        method = query_params.get("method", "")
        if method:
            print(f"✅ Storing method: {method}")  # Debugging
            return method  # Store the method
    return dash.no_update  # No unnecessary updates

# Callback to render pages correctly
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('stored-method', 'data')],
    [State('url', 'search')]
)
def display_page(pathname, stored_method, search):
    print(f"Pathname: {pathname}, Search: {search}, Stored Method: {stored_method}")  # Debugging

    if pathname in ['/', '/home']:
        return home_layout  # Home page layout
    elif pathname == '/input-array':
        return input_array_layout  # Input array page layout
    elif pathname.startswith('/sorting'):  
        # Extract method from search query or fallback to stored-method
        query_params = dict(param.split('=') for param in search.lstrip('?').split('&') if '=' in param) if search else {}
        method = query_params.get("method", stored_method)

        print(f"Sorting Method: {method}")  # Debugging print

        # Match Sorting Method to the Correct Layout
        if method == "quick-sort":
            return quick_sort_layout  # Call the function to generate the layout
        elif method == "merge-sort":
            return merge_sort_layout  # Call the function to generate the layout
        elif method == "insertion-sort":
            return insertion_sort_layout()  # Call the function to generate the layout
        else:
            return html.H3("Invalid sorting method", className="text-center mt-5")
    
    return html.H3("404 - Page Not Found", className="text-center mt-5")

# Register callbacks for all pages
register_input_array_callbacks(app)
register_insertion_sort_callbacks(app)
#register_merge_sort_callbacks(app)
#register_quick_sort_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)