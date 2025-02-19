from dash import html, dcc
import dash_bootstrap_components as dbc

insertion_sort_layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Insertion Sort Visualization", className="text-center my-5"), width=12)),
    
    dbc.Row(dbc.Col(html.Div(id='insertion-sort-container', className='sorting-container'), width=12)),
    
    dbc.Row(dbc.Col(
        html.Div([
            dbc.Button("Start", id="start-insertion", color="primary", className="m-2"),
            dbc.Button("Stop", id="stop-insertion", color="danger", className="m-2"),
            dbc.Button("Restart", id="restart-insertion", color="warning", className="m-2"),
            dbc.Button("Back", href="/input-array", color="secondary", className="m-2")
        ], className="text-center"), width=12
    ))
])