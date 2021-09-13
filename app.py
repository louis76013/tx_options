# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:37:54 2021

@author: louis76013@gmail.com
"""

#import json
from dash.dependencies import Input, Output
#import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash
#import sys
import pandas as pd
import plotly.graph_objects as go
#import plotly.subplots as ms
import numpy as np
import sys

# ================== read settle to get monthly
from csv import reader
# read csv file as a list of lists
with open('settle_monthly_2019_2020_2021.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    print(type(read_obj))
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    print(list_of_rows)

list_of_SettleDate = [int(s[0].replace("/", "")) for s in list_of_rows]

# ======= dataframe daily
df = pd.read_csv('20xx_fut_tx_near_exp.csv')

# ==== re-order index
conditions = [df['Session'] == 'Post', df['Session'] == 'Regular']
values = [df['Date']+'A', df['Date']+'B']
df['DateSession'] = np.select(conditions, values)
df.sort_values(by=['DateSession'], inplace=True)

# ======== select one month

def select_month(idx):
    month = list_of_SettleDate[idx]
    dfm = df[df['Exp'] == month]
    '''
    figm = go.Figure(data=[go.Candlestick(x=dfm['DateSession'],
                                          open=dfm['Open'],
                                          high=dfm['High'],
                                          low=dfm['Low'],
                                          close=dfm['Close'])],
                     layout={'xaxis': {'rangeslider': {'visible': False}},'margin.t':30})
    return figm
    '''
    fig2.update_traces(x=dfm['DateSession'],y=dfm['Volume'],selector=dict(type="bar"))
    fig2.update_traces(x=dfm['DateSession'],
                      open=dfm['Open'],
                      high=dfm['High'],
                      low=dfm['Low'],
                      close=dfm['Close'],selector=dict(type="candlestick"))
    
    return

# print(df)
# sys.exit()
# ======= exclude empty months

dfp = pd.read_csv('20xx_fut_monthly.csv')
dfp = dfp[dfp['Open']!=0]

#======= add column for x-axis
dfp['Date2'] = ''
# print(dfp)

print(dfp.dtypes)
dfp['Start'] = dfp['Start'].astype(str).str[:8]
dfp['Date2'] = dfp['Start'].astype(str)+'-'+dfp['Exp'].astype(str)
print(dfp)
# sys.exit()

# ========== subplot
from plotly.subplots import make_subplots
fig = make_subplots(specs=[[{"secondary_y": True}]])

# include a go.Bar trace for volumes

fig.add_trace(go.Bar(name='Volume',x=dfp['Date2'], y=dfp['Volume'],marker=dict(color='gray',opacity=0.25)),
               secondary_y=True)

fig.add_trace(go.Candlestick(name='OHLC',x=dfp['Date2'],
                open=dfp['Open'],
                high=dfp['High'],
                low=dfp['Low'],
                close=dfp['Close']))

fig.update_layout(hovermode="x",margin_t=30)
fig.update_layout(xaxis=dict(rangeslider=dict(visible=False)))

dfm = df[df['Exp'] == 20210818]

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Bar(name='Volume',x=dfm['DateSession'], y=dfm['Volume'],marker=dict(color='gray',opacity=0.25)),
               secondary_y=True)

fig2.add_trace(go.Candlestick(name='OHLC',x=dfm['DateSession'],
                open=dfm['Open'],
                high=dfm['High'],
                low=dfm['Low'],
                close=dfm['Close']))
                     
# fig.show()
fig2.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
fig2.update_layout(hovermode="x",margin_t=30)

# ============  multiple graphs
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div(children='''
            TX Options Monthly: by Louis76013@gmail.com
        '''),
        dcc.Graph(
            id='graph1',
            figure=fig
        ),
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
#        html.Div(id='addtexthere', children='''
#            TX Futures Daily: by Louis
#        '''),
        dcc.Graph(
            id='graph2',
            figure=fig2
        ),
    ]),
])

                 
@app.callback(
    Output('graph2', 'figure'),
    Input('graph1', 'clickData'))
def update_month_data(clickData):
    idx = clickData['points'][0]['pointIndex']
    select_month(idx)
    return fig2

'''
@app.callback(
    Output('addtexthere', 'children'),
    Input('graph1', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)
'''

@app.callback(
    Output('graph1', 'figure'),
    Input('graph1', 'clickData'))
def highlight_month(clickData):
    idx = clickData['points'][0]['pointIndex']
    colors=['lightslategray',] *34    
    colors[idx]='darkkhaki'
    fig.update_traces(marker_color=colors,selector=dict(type="bar"))
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
