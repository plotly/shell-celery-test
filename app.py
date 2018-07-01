import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import pytz
import datetime as dt
import pickle
from utils import StaticUrlPath
import config
from auth import auth

# server side data pulling mock-up
def get_new_data():
    print('pull new data')
    data = np.random.normal(size=1)
    with open('temp.pickle', 'wb') as f:
        pickle.dump(data[0], f, protocol=pickle.HIGHEST_PROTOCOL)
        print('dump new value')
        f.close()

def get_new_data_every(period=5):
    print('start loop on server side')
    """Update the data every 'period' seconds"""
    while True:
        get_new_data()
        print("pulling is in sleep")
        time.sleep(period)


app = dash.Dash(__name__, static_folder='static')
auth(app)
server = app.server

get_new_data()

app.layout = html.Div([
    html.Link(href='/static/stylesheet.css', rel='stylesheet'),

    html.Div(id='live-update-text'),
    # Update internal for live updating of page
    dcc.Interval(
        id='live-update',
        interval=4 * 1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('live-update-text', 'children'),
              [Input('live-update', 'n_intervals')])
def update_figs(n):
    print('start updating text display')
    if os.path.isfile('temp.pickle'):
        with open('temp.pickle', 'rb') as f:
            b = pickle.load(f)
            print('read new value')
            f.close()
    else:
        b = 0.0
    style = {'padding': '5px', 'fontSize': '30px'}
    return [html.Span('The latest updated data: {0:.2f}'.format(b), style=style)]

# define multi-processes
def start_multi():
    executor = ProcessPoolExecutor(max_workers=1)
    executor.submit(get_new_data_every)

if __name__ == '__main__':
    start_multi()
    app.run_server(processes=1)
