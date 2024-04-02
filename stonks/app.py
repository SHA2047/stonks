import dash
from dash import dcc, html, Input, Output, callback_context
import dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout with multiple pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Data | ', href='/data'),
        dcc.Link('Visuals', href='/visuals'),
    ]),
    html.Div(id='page-content')
])

# Define the layout for the 'Data' page
data_page_layout = html.Div([
    html.H1("Data"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True,
        accept=".csv,.xlsx,.parquet"
    ),
    html.Button('Show Full Data', id='full-data-button', n_clicks=0),
    dash_table.DataTable(id='output-data-upload', page_size=5)
])

# Define the layout for the 'Visuals' page
visuals_page_layout = html.Div([
    html.H1("Visuals")
    # Additional content for the 'Visuals' page can be added here
])

# Callback for page content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/data':
        return data_page_layout
    elif pathname == '/visuals':
        return visuals_page_layout
    else:
        return '404'

# Helper function to parse uploaded data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'parquet' in filename:
            # Assume that the user uploaded a Parquet file
            df = pd.read_parquet(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return df

# Callback for file upload
@app.callback(
    Output('output-data-upload', 'data'),
    Output('output-data-upload', 'columns'),
    [Input('upload-data', 'contents')],
    [Input('full-data-button', 'n_clicks')],
    [dash.dependencies.State('upload-data', 'filename')]
)
def update_output(list_of_contents, n_clicks, list_of_names):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if list_of_contents is not None:
        df = parse_contents(list_of_contents[0], list_of_names[0])
        if button_id == 'full-data-button' and n_clicks > 0:
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
        return df.head().to_dict('records'), [{"name": i, "id": i} for i in df.columns]

    raise PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

