import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt
import requests
import time as tm

url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/3'
data = requests.get(url).json()
data = data['trace']['sensors']
dict_ = {}
for rec in data:
    sen = str(rec['id'])
    lst = [rec['value']]
    value = lst
    dict_[sen] = value
df = pd.DataFrame.from_dict(dict_, orient='columns')
df['timestamp']=dt.datetime.now()

def animate():
    x_values = dframe['timestamp']
    y_values1 = dframe['1']
    y_values2 = dframe['2']
    plt.cla()
    plt.plot( x_values, y_values1)
    plt.plot( x_values, y_values2)
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Sensors')
    plt.tight_layout()
    

def read_API(df):
    url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/2'
    data = requests.get(url).json()
    data = data['trace']['sensors']
    dict_ = {}
    for rec in data:
        sen = str(rec['id'])
        lst = [rec['value']]
        value = lst
        dict_[sen] = value
    df1 = pd.DataFrame.from_dict(dict_, orient='columns')
    df1['timestamp']=dt.datetime.now()
    if len(df) > 50:
        df.drop(df.index[0])
    result = pd.concat([df, df1])
    return result

plt.ion()
fig, ax = plt.subplots()

while True:
    df = read_API(df)
    dframe = df.copy()
    dframe['timestamp'] = pd.to_datetime(dframe['timestamp']) + pd.DateOffset(hours=2)
    dframe = dframe.set_index('timestamp')
    end = dframe.index.max()
    start= end - dt.timedelta(seconds=5)
    dframe = dframe.loc[start:end]
    dframe = dframe.reset_index()
    #plt.scatter(dframe['timestamp'], dframe['1'])
    #plt.show()
    #plt.pause(0.1)
    #ax.clear()
    #dframe.plot(kind='line', x='timestamp', y='1', ax=ax)
    #dframe.plot(kind='line', x='timestamp', y='2', ax=ax)
    #dframe.plot(kind='line', x='timestamp', y='3', ax=ax)
    #plt.show()
    #plt.pause(0.5)
    ani = FuncAnimation(plt.gcf(), animate())
    plt.tight_layout()
    plt.show()

