from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import Device, StatData
from django.http import JsonResponse
import json
import pandas as pd
import numpy as np
from django.conf import settings
import datetime
from main.views import send_to_user


@csrf_exempt
def load_data(filename):
    """
    This function will load all data to django db
    :param filename:
    :return: True, if OK, else False
    """
    try:
        df = pd.read_table(settings.BASE_DIR + settings.STATIC_ROOT + "/datafiles/" + filename, sep='\t',
                           usecols=['Machine ID', 'Date',
                                    'Temperature', 'Vibration',
                                    'Power', 'System load',
                                    'Work time'])
        df.apply(lambda x: x.replace(',', '.'))
        idd = df['Machine ID'].unique()
        idd = [i for i in idd if i != '#']
        for mech in idd:
            device, created = Device.objects.get_or_create(idDevice=int(mech))
            ind = np.where(df['Machine ID'].values == mech)
            for index in ind[0]:
                data = df['Date'][index].split(sep=' ')
                time = data[1].split(sep=':')
                data = data[0].split(sep='.')
                data = [int(i) for i in data]
                time = [int(i) for i in time]
                date = datetime.datetime(data[2], data[1], data[0], time[0], time[1], time[2])
                stat, created = StatData.objects.get_or_create(device_id=device.pk, device__idDevice=int(mech),
                                                               date=date)
                stat.temp = float(df['Temperature'][index].replace(',', '.'))
                stat.vibration = float(df['Vibration'][index].replace(',', '.'))
                stat.power = float(df['Power'][index].replace(',', '.'))
                stat.load = float(df['System load'][index].replace(',', '.'))
                stat.time = int(df['Work time'][index])
                stat.save()
        return True
    except TypeError:
        return False


def main_telemetry_page(request):
    """
    Main telemetry page, contains links to other params
    :param request: Request
    :return: simple html render page
    """
    return render(request, 'telemetry/home.html', {'user': request.user})


def data_all(request):
    """
    This function will display all telemetry from devices
    :param request:
    :return: JSON with devices and telemetry
    """
    devices = Device.objects.all()
    all_data = []
    for device in devices:
        data = StatData.objects.filter(device=device)
        params = []
        for obj in data:
            z = {'date': str(obj.date).split(sep='+')[0],
                 'temp': obj.temp,
                 'vibration': obj.vibration,
                 'power': obj.power,
                 'load': obj.load,
                 'time': obj.time
                 }
            params.append(z)
        all_data.append({'device': device.idDevice,
                         'data': params})
    send_to_user('TELEMETRY', 'New data loaded to DB', request.user)
    return render(request, 'telemetry/all.html', {'stats': all_data})


def data_critical(request):
    """
    This function will display critical errors in telemetry
    :param request: Request
    :return: JSON with attention devices
    """
    devices = Device.objects.all()
    all_data = []
    for device in devices:
        data = StatData.objects.filter(device=device)
        params = []
        for obj in data:
            if not check_parameters('critical', obj)['status']:
                z = {'date': str(obj.date).split(sep='+')[0],
                     'temp': obj.temp,
                     'vibration': obj.vibration,
                     'power': obj.power,
                     'load': obj.load,
                     'time': obj.time
                     }
                params.append(z)
        if not params:
            all_data.append({'device': device.idDevice,
                             'data': params})
    send_to_user('TELEMETRY', 'New data loaded to DB', request.user)
    return render(request, 'telemetry/critical.html', {'stats': all_data})


def data_attention(request):
    """
    This function will display attention telemetry
    :param request: Request
    :return: JSON with attention devices
    """
    devices = Device.objects.all()
    all_data = []
    for device in devices:
        data = StatData.objects.filter(device=device)
        params = []
        for obj in data:
            if not check_parameters('danger', obj)['status']:
                z = {'date': str(obj.date).split(sep='+')[0],
                     'temp': obj.temp,
                     'vibration': obj.vibration,
                     'power': obj.power,
                     'load': obj.load,
                     'time': obj.time
                     }
                params.append(z)
        if not params:
            all_data.append({'device': device.idDevice,
                             'data': params})
    send_to_user('TELEMETRY', 'New data loaded to DB', request.user)
    return render(request, 'telemetry/danger.html', {'stats': all_data})


def check_parameters(flag, data):
    """
    This function returns all error with classification
    :param flag: 'danger' or 'critical'
    :param data: data measures from devices
    :return: JSON with errors and descriptions
    """
    device = data.device
    errors = []
    status = True
    if flag == 'danger':
        # Loading danger params
        if data.temp > device.danger_temp:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'temp'})
        if data.power > device.danger_pow:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'pow'})
        if data.vibration > device.danger_vibr:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'vibr'})
        if data.time > device.danger_time:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'time'})
        if data.load > device.danger_load:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'load'})
    elif flag == 'critical':
        # Loading critical params
        if data.temp > device.critical_temp:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'temp'})
        if data.power > device.critical_pow:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'pow'})
        if data.vibration > device.critical_vibr:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'vibr'})
        if data.time > device.critical_time:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'time'})
        if data.load > device.critical_load:
            status = False
            errors.append({'status': flag,
                           'isOK': False,
                           'message': 'load'})
    return {'status': status, 'errors': errors}
