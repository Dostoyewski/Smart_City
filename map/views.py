from djeym.models import Placemark, Map, CategoryPlacemark, MarkerIcon, IconCollection, CategoryPolyline, Polyline, CategoryPolygon, Polygon, HeatPoint
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import pandas as pd
import numpy as np
from django.conf import settings
import datetime
from os import listdir
from os.path import isfile, join
import requests




# Create your views here.
def CreateLineCategory(name,map_num):
    main_map = Map.objects.get(pk = map_num)
    category_main = CategoryPlacemark.objects.create(
            ymap=main_map,
            title=name + '(На утверждение)')
    category_line = CategoryPolyline.objects.create(
            ymap=main_map,
            title=name)
    return(category_main)
    
def CreateAreaCategory(name,map_num):
    main_map = Map.objects.get(pk = map_num)
    category_main = CategoryPlacemark.objects.create(
            ymap=main_map,
            title=name + '(На утверждение)')
    category_area = CategoryPolygon.objects.create(
            ymap=main_map,
            title=name)
    return(category_main)

def CreateLine (map_num, name_category, name, filename, about):
    main_map = Map.objects.get(pk = map_num)
    category = CreateLineCategory(name_category, map_num)
    coordinates = load_data(filename)
    polyline = Polyline.objects.create(
            ymap=main_map,
            category=category,
            header=name,
            body=about,
            coordinates=coordinates)


def CreateArea (map_num, name_category, name, coordinates, filename, about):
    main_map = Map.objects.get(pk = map_num)
    category = CreateAreaCategory(name_category, map_num)
    coordinates = load_data(filename)
    polygon = Polygon.objects.create(
            ymap=main_map,
            category=category,
            header=name,
            body=about,
            coordinates=coordinates)
        
def load_data(filename):
    """
    This function will load all data to django db
    :param filename:
    :return: True, if OK, else False
    """
    df = pd.read_table(settings.BASE_DIR + settings.STATIC_ROOT + "/datafiles/people/" + filename, sep=',',
                        usecols=['Latitude','Longitude','Elevation'])
    Latitude = df['Latitude']
    Longitude = df['Longitude']
    coordinates = '['
    for i in range(len(Latitude)):
        coordinates+= '['+ str(Latitude[i]) + ',' + str(Longitude[i]) + ']' + ','
    coordinates = coordinates[0:-1]
    coordinates += ']'
    return(coordinates)

def getcoord(obj):
    map_request = "https://geocode-maps.yandex.ru/1.x/?apikey=fafde453-2c72-4d6e-b318-fda89f6c09ef&geocode=" + obj + '&format=json'
    response = requests.get(map_request)
    data = requests.get(map_request).json()
    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
    return(pos) 


def CreateHeat(filename, map_num):
    df = pd.read_excel(settings.BASE_DIR + settings.STATIC_ROOT + "/datafiles/" + filename)
    objects, col = df['Объект'], df['Количество']
    main_map = Map.objects.get(pk = map_num)
    for i in range(len(objects)):
        if (col[i] > 400):
            loc = getcoord(objects[i])
            coord = '['+str(loc[1]) + ',' + str(loc[0]) + ']'
            heat_point = HeatPoint.objects.create(ymap=main_map, weight = col[i], coordinates = coord )
