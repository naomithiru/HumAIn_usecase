import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('results.csv')

fig1 = px.bar(df, x="year", y = "ai_entity", color="year", barmode="group")

fig2 = px.bar(df, x = "ai_entity", y="year", color="status", barmode="group")


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='AI Trends'),

        html.Div(children='''
            AI Trends Over The Years.
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig1
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        #html.H1(children='Hello Dash'),

        html.Div(children='''
            Comparison Pre and Post Covid.
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)



