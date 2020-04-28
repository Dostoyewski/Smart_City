from django.db import models
import datetime


class Device(models.Model):
    """
    Device model, contains critical and danger values for each parameter
    """
    idDevice = models.IntegerField(unique=True)
    string = models.CharField(blank=True, max_length=50)
    # Temperature params
    danger_temp = models.FloatField(default=45)
    critical_temp = models.FloatField(default=50)
    # Vibration params
    danger_vibr = models.FloatField(default=0.75)
    critical_vibr = models.FloatField(default=1)
    # Power params
    danger_pow = models.IntegerField(default=0.65)
    critical_pow = models.IntegerField(default=0.7)
    # Load params
    danger_load = models.FloatField(default=80)
    critical_load = models.FloatField(default=95)
    # Working time params
    danger_time = models.IntegerField(default=70000)
    critical_time = models.IntegerField(default=80000)


class StatData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateTimeField(unique=True, default=datetime.datetime(2000, 1, 1, 10, 10, 10))
    temp = models.FloatField(default=30)
    vibration = models.FloatField(default=0)
    power = models.FloatField(default=0)
    load = models.FloatField(default=0)
    time = models.IntegerField(default=0)
