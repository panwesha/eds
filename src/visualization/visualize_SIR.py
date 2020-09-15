import pandas as pd
import numpy as np

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.graph_objects as go

import os
print(os.getcwd())
fitted_final_data_dash_df = pd.read_csv('/Users/anweshapanda/ads_covid-19/data/processed/sir/fitted_SIR_data.csv',sep=';')
yd = fitted_final_data_dash_df.copy()
# Initial reading of required data
#df_input_large=pd.read_csv('../ads_covid-19/data/processed/COVID_final_set.csv',sep=';')
fitted_final_data_dash_df = pd.read_csv('/Users/anweshapanda/ads_covid-19/data/processed/SIR/fitted_SIR_data.csv',sep=';')
optimized_dash_df = pd.read_csv('/Users/anweshapanda/ads_covid-19/data/processed/SIR/optimized_SIR_data.csv',sep=';')
ydata_dash_df = pd.read_csv('/Users/anweshapanda/ads_covid-19/data/processed/SIR/ydata_SIR_data.csv',sep=';')



fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data
    Goal of the project is to learn data science by applying a cross industry standard process,
    it covers the full walkthrough of: automated data gathering, data transformations,
    filtering and machine learning to approximating the doubling time, and
    (static) deployment of responsive dashboard.
    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),

    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in fitted_final_data_dash_df],
        value=['US', 'Germany','Italy'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select SIR Model and/or fitted SIR Model
        '''),

    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'SIR curve and fitted SIR curve ', 'value': 'SIR_value'},

    ],
    value='SIR_value',
    multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope')
])


@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(full_country_list,show_doubling):




    traces = []
    for each in full_country_list:




        traces.append(dict(x=ydata_dash_df.date, #df_plot.date,
                                y=ydata_dash_df[each], #=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=4,
                                name=each

                        )
                )
        traces.append(dict(x=ydata_dash_df.date, #df_plot.date,
                                y=fitted_final_data_dash_df[each], #=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=4,
                                name=each+'_fitted'

                        )
                )


    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis={'type': 'log',
                        'range': '[1.1,5.5]',
                        'title':'Number of people infected'
                        }

        )
    }

if __name__ == '__main__':

    app.run_server(debug=True, host='127.0.0.1', port = 8051, use_reloader=False)
