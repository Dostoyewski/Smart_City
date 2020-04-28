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


@csrf_exempt
def load_data(request):
    try:
        """body = request.body
        data = json.loads(body)

        if 'status' not in data or 'filename' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        filename = data['filename']"""
        filename = "February.dat"
        df = pd.read_table(settings.BASE_DIR + settings.STATIC_ROOT + "/datafiles/" + filename, sep='\t',
                           usecols=['Machine ID', 'Date',
                                    'Temperature', 'Vibration',
                                    'Power', 'System load',
                                    'Work time'])
        df.apply(lambda x: x.replace(',', '.'))
        print(df)
        idd = df['Machine ID'].unique()
        idd = [i for i in idd if i != '#']
        print(idd)
        for mech in idd:
            device, created = Device.objects.get_or_create(idDevice=int(mech))
            ind = np.where(df['Machine ID'].values == mech)
            print(type(ind[0][0]))
            for index in ind[0]:
                data = df['Date'][index].split(sep=' ')
                time = data[1].split(sep=':')
                data = data[0].split(sep='.')
                data = [int(i) for i in data]
                time = [int(i) for i in time]
                date = datetime.datetime(data[2], data[1], data[0], time[0], time[1], time[2])
                stat, created = StatData.objects.get_or_create(device_id=device.pk, device__idDevice=int(mech), date=date)
                print('ok')
                print(created)
                print(float(df['Temperature'][index].replace(',', '.')))
                stat.temp = float(df['Temperature'][index].replace(',', '.'))
                stat.vibration = float(df['Vibration'][index].replace(',', '.'))
                stat.power = float(df['Power'][index].replace(',', '.'))
                stat.load = float(df['System load'][index].replace(',', '.'))
                stat.time = int(df['Work time'][index])
                stat.save()

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})