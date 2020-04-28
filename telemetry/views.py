from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Device, StatData
import json
import pandas as pd
import numpy as np
from django.conf import settings
import datetime
from main.views import send_to_user
from os import listdir
from os.path import isfile, join


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


def update_db(request):
    """
    This function will update current db
    with devices and data
    :param request: only POST is allowed, should contain header 'reload'
    :return: 200 if OK else METHOD_NOT_ALLOWED
    """
    if request.method == 'POST':
        body = request.body
        request_data = json.loads(body)

        if 'reload' not in request_data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})
        path = settings.BASE_DIR + settings.STATIC_ROOT + "/datafiles/"
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            if file[-3:] == 'dat':
                load_data(file)
        return HttpResponse(200)
    else:
        return JsonResponse(status=405, data={"message": "METHOD_NOT_ALLOWED"})


def main_telemetry_page(request):
    """
    Main telemetry page, contains links to other params
    :param request: Request
    :return: simple html render page
    """
    return render(request, 'telemetry/home.html', {'user': request.user})


def data_all(request):
    """
    This function will display all telemetry from devices.

    :param request: GET or POST, when becomes GET uses default parameters:
                    displays all data for each device
    headers: 'start_date': start date in format "year-month-day"
             'end_date': start date in format "year-month-day"
             'params' : array with displaying parameters: ['temp', 'vibration', 'power', 'load', 'time']
    :return: JSON with devices and telemetry
    """
    devices = Device.objects.all()
    all_data = []
    for device in devices:
        if request.method == 'POST':
            body = request.body
            request_data = json.loads(body)
            display_params = request_data['params']

            if 'start_date' not in request_data or 'end_date' not in request_data:
                data = StatData.objects.filter(device=device)
            else:
                data = StatData.objects.filter(date__range=[request_data['start_date'],
                                                            request_data['end_date']])
        else:
            display_params = ['temp', 'vibration', 'power', 'load', 'time']
            data = StatData.objects.filter(device=device)
        params = []
        for obj in data:
            z = {'date': str(obj.date).split(sep='+')[0]}
            if 'temp' in display_params:
                z['temp'] = obj.temp
            if 'vibration' in display_params:
                z['vibration'] = obj.vibration
            if 'power' in display_params:
                z['power'] = obj.power
            if 'load' in display_params:
                z['load'] = obj.load
            if 'time' in display_params:
                z['time'] = obj.time
            params.append(z)
        all_data.append({'device': device.idDevice,
                         'data': params})
    return render(request, 'telemetry/all.html', {'stats': json.dumps(all_data)})


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
    if not all_data:
        send_to_user('TELEMETRY', 'Все системы в норме', request.user)
    else:
        send_to_user('TELEMETRY', 'Обнаружены критические повреждения', request.user)
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
    if not all_data:
        send_to_user('TELEMETRY', 'Все системы в норме', request.user)
    else:
        send_to_user('TELEMETRY', 'Проверьте параметры устройств: некоторые приближаются к критическим',
                     request.user)
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
