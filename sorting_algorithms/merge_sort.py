from dash import html, dcc
import dash_bootstrap_components as dbc

merge_sort_layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Merge Sort Visualization", className="text-center my-5"), width=12)),
    
    dbc.Row(dbc.Col(html.Div(id='merge-sort-container', className='sorting-container'), width=12)),
    
    dbc.Row(dbc.Col(
        html.Div([
            dbc.Button("Start", id="start-merge", color="primary", className="m-2"),
            dbc.Button("Stop", id="stop-merge", color="danger", className="m-2"),
            dbc.Button("Restart", id="restart-merge", color="warning", className="m-2"),
            dbc.Button("Back", href="/input-array", color="secondary", className="m-2")
        ], className="text-center"), width=12
    ))
])