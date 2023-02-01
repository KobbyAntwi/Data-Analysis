import pandas as pd
import plotly.express as px
import io
import dash
import dash_core_components as dcc
import dash_html_components as html

def load_data():
    while True:
        file_path = input("Enter the file path of the excel file: ")
        try:
            data = pd.read_excel(file_path)
            break
        except FileNotFoundError:
            print("File not found, please try again.")
    data = data.astype({'Feature 1': 'float64', 'Feature 2': 'float64', 'Feature 3': 'float64'})
    data = data.dropna()
    return data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Interactive Dashboard'),
    html.Div([
        dcc.Dropdown(
            id='feature-dropdown',
            options=[
                {'label': 'Feature 1', 'value': 'Feature 1'},
                {'label': 'Feature 2', 'value': 'Feature 2'},
                {'label': 'Feature 3', 'value': 'Feature 3'}
            ],
            value='Feature 1'
        )
    ]),
    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='hist-chart')
    ])
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_bar_chart(feature):
    if feature is None:
        return dash.no_update

    bar_chart = px.bar(data, x='Category', y=feature)
    bar_chart.update_layout(title='Bar Chart', xaxis_title='Category', yaxis_title=feature)
    return bar_chart

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_pie_chart(feature):
    if feature is None:
        return dash.no_update

    pie_chart = px.pie(data, values=feature, names='Category')
    pie_chart.update_layout(title='Pie Chart')
    return pie_chart

@app.callback(
    Output('hist-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_hist_chart(feature):
    if feature is None:
        return dash.no_update

    hist_chart = px.histogram(data, nbins=10, x=feature)
    hist_chart.update_layout(title='Histogram', xaxis_title=feature, yaxis_title='Frequency')
    return hist_chart

if __name__ == '__main__':
    app.run_server(debug=True)

