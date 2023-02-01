import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Load the data from the excel file
file_path = 'path/to/excel/file.xlsx'
data = pd.read_excel(file_path)

# Check for missing data and fill with mean value
data.fillna(data.mean(), inplace=True)

# Create a Dash app
app = dash.Dash(__name__)

# Add a bar chart to the dashboard
bar_chart = px.bar(data, x=data.columns, y=data.mean(), color=data.columns)
bar_chart.update_layout(title='Bar Chart', xaxis_title='Features', yaxis_title='Mean Value')

# Add a pie chart to the dashboard
pie_chart = px.pie(data, values=data.sum(), names=data.columns)
pie_chart.update_layout(title='Pie Chart')

# Add a histogram to the dashboard
hist_chart = px.histogram(data, nbins=10)
hist_chart.update_layout(title='Histogram')

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Interactive Dashboard'),
    html.Div([
        dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': col, 'value': col} for col in data.columns],
            value=data.columns[0],
            multi=False
        ),
        html.Div([
            dcc.Graph(id='bar-chart', figure=bar_chart),
            dcc.Graph(id='pie-chart', figure=pie_chart),
            dcc.Graph(id='hist-chart', figure=hist_chart)
        ])
    ])
])

#interactive filtering
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')]
)
def update_bar_chart(feature):
    bar_chart = px.bar(data, x=feature, y=data[feature].mean(), color=feature)
    bar_chart.update_layout(title='Bar Chart', xaxis_title=feature, yaxis_title='Mean Value')
    return bar_chart

@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')]
)
def update_pie_chart(feature):
    pie_chart = px.pie(data, values=data[feature].sum(), names=feature)
    pie_chart.update_layout(title='Pie Chart')
    return pie_chart

@app.callback(
    dash.dependencies.Output('hist-chart','figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')]
)
def update_hist_chart(feature):
    hist_chart = px.histogram(data, nbins=10, x=feature)
    hist_chart.update_layout(title='Histogram', xaxis_title=feature, yaxis_title='Count')
    return hist_chart

if name == 'main':
    app.run_server(debug=True)
