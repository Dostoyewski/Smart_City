import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr


def get_datetime(data):
    data = data.split(sep=' ')
    time = data[1].split(sep=':')
    data = data[0].split(sep='.')
    data = [int(i) for i in data]
    time = [int(i) for i in time]
    try:
        date = datetime.datetime(data[2], data[1], data[0], time[0], time[1], time[2])
    except IndexError:
        date = datetime.datetime(data[2], data[1], data[0], time[0], time[1], 0)
    return date


def load_file(filenames=['February.dat']):
    df = []
    for filename in filenames:
        df.append(pd.read_table("C:/Users/Федор/Documents/GIT/Smart_City/static/datafiles/" + filename, sep='\t',
                                usecols=['Machine ID', 'Date',
                                         'Temperature', 'Vibration',
                                         'Power', 'System load',
                                         'Work time']))
    df = pd.concat(df).drop_duplicates().reset_index(drop=True)
    df = df.applymap(lambda x: x.replace(',', '.'))
    idd = df['Machine ID'].unique()
    idd = [i for i in idd if i != '#']
    print(idd)
    data = []
    first_time = get_datetime(df['Date'][1])
    print(first_time)
    for mech in idd:
        index = np.where(df['Machine ID'].values == mech)
        time = []
        vibration = []
        power = []
        temp = []
        load = []
        for ind in index[0]:
            date = get_datetime(df['Date'][ind])
            time.append((date - first_time).total_seconds())
            vibration.append(float(df['Vibration'][ind]))
            temp.append(float(df['Temperature'][ind]))
            power.append(float(df['Power'][ind]))
            load.append(float(df['System load'][ind]))
        data.append({"device": mech,
                     "time": time,
                     "vibration": vibration,
                     "power": power,
                     "temp": temp,
                     "load": load})
    return data


def get_fit(data, n, param):
    X = data[n]['time']
    Y = data[n][param]
    nmax = 50
    for i in range(nmax):
        p = np.poly1d(np.polyfit(X, Y, deg=i))
        x_t = np.linspace(np.min(X), np.max(X), len(X))
        if pearsonr(p(x_t), Y)[0] > 0.8:
            return p, pearsonr(p(x_t), Y)[0]
    return p, pearsonr(p(x_t), Y)[0]


if __name__ == "__main__":
    data = load_file(['February.dat', 'March.dat'])
    fig, ax = plt.subplots()
    # ax.plot(data[3]['time'], data[3]['temp'])
    ax.set(xlabel='x', ylabel='y',
           title='Ships plot')
    ax.grid()
    n = 1
    params = ['vibration', 'load', 'temp']

    for n in range(12):
        print('========', n, '=========')
        for param in params:
            p, corr = get_fit(data, n, param)
            print(param)
            print(corr)
            print('deg:', len(p.coef))
            print('***************')
    X = data[n]['time']
    Y = data[n][param]
    x_t = np.linspace(np.min(X), np.max(X), 232)

    plt.plot(x_t, p(x_t), '-')
    plt.plot(X, Y)
    plt.show()
