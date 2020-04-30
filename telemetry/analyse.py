import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor


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


def load_file(filename='February.dat'):
    df = pd.read_table("C:/Users/Федор/Documents/GIT/Smart_City/static/datafiles/" + filename, sep='\t',
                       usecols=['Machine ID', 'Date',
                                'Temperature', 'Vibration',
                                'Power', 'System load',
                                'Work time'])
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


if __name__ == "__main__":
    data = load_file()
    fig, ax = plt.subplots()
    ax.plot(data[3]['time'], data[3]['temp'])
    ax.set(xlabel='x', ylabel='y',
           title='Ships plot')
    ax.grid()
    clf = MLPRegressor(alpha=0.001, hidden_layer_sizes=(10,), max_iter=50000,
                       activation='logistic', verbose='True', learning_rate='adaptive')
    n = len(data[3]['time'])
    X = np.reshape(data[3]['time'], [n, 1])
    Y = np.reshape(data[3]['temp'], [n, ])
    a = clf.fit(X, Y)
    x_ = np.linspace(data[3]['time'][0], data[3]['time'][1], 500)
    pred_x = np.reshape(x_, [500, 1])  # [160, ] -> [160, 1]
    pred_y = clf.predict(pred_x)  # predict network output given x_
    plt.plot(pred_x, pred_y, '-')
    plt.show()

