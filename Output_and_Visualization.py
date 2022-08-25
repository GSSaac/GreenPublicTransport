#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:27:58 2022

@author: giu

"""


import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

path_FPAI = '../GreenerCities_fruitPunchAI/code'

with open('../GreenerCities_fruitPunchAI/code/bdd100k labels/labels/det_20/det_val.json', 'r') as f:
  data = json.load(f)

path_info = '../GreenerCities_fruitPunchAI/code/bdd100k info/info/100k/val'
# Output: {'name': 'Bob', 'languages': ['English', 'French']}
#print(data)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

from os import listdir
import os
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'
list_infofiles = [i for i in listdir(path_info) if '.json' in i]

n_images = len(data)
label_list = list()
for n in np.arange(n_images):
    image_name = data[n]['name']
    timestamp = data[n]['timestamp'] 
    weather = data[n]['attributes']['weather']
    scene = data[n]['attributes']['scene']
    timeofday = data[n]['attributes']['timeofday']
    
    
    n_objects = len(data[n]['labels'])
    n_cars = 0
    n_busses = 0
    n_trucks = 0
    n_peds = 0
    
    #categs = np.unique([data[n]['labels'][j]['category'] for j in np.arange(n_objects)])
    for j in np.arange(n_objects):
        if data[n]['labels'][j]['category']=='car':
            n_cars = n_cars+1
    
        elif data[n]['labels'][j]['category']=='bus':
            n_busses = n_busses +1
            
        elif data[n]['labels'][j]['category']=='truck':
            n_trucks = n_trucks +1
            
        elif data[n]['labels'][j]['category']=='pedestrian':
            n_peds = n_peds +1
        
            
    label_list.append([image_name,weather,scene,timeofday,
                       timestamp,n_cars,n_busses,n_trucks,n_peds])
    #print(n_cars,n_busses)
label_list = pd.DataFrame(label_list)
label_list.columns = ['image_name','weather','scene',
                      'timeofday','timestamp',
                      'n_cars','n_busses','n_trucks','n_peds']



count_objs = pd.DataFrame([])
objs = ['n_cars','n_busses','n_trucks','n_peds']
for o in objs:
    count_o = label_list[o].value_counts().reset_index(name = 'N of N')
    count_o.columns=['N','N of N']
    count_o['type'] = o
    count_objs = pd.concat([count_objs,count_o],axis = 0)
    
#%matplotlib inline
sns.barplot(data = count_objs, x = 'N',y = 'N of N', hue = 'type')


lat_list = list()
lon_list = list()
movie_name = list()
s_date = list()
e_date = list()
f_date = list()
#country = list()
#state = list()
#city = list()
for i in np.arange(label_list.shape[0]):
    image_name = label_list['image_name'].iloc[i].split('.')[0]
    with open(os.path.join(path_info,image_name+'.json'), 'r') as f:
        info_data = json.load(f)
    movie_name.append(info_data['filename'])
    print(image_name)
  
  # find data at 10nth second
    start_date = datetime.datetime.fromtimestamp(info_data['startTime']/1e3)
    end_date = datetime.datetime.fromtimestamp(info_data['endTime']/1e3)
    
    start_date_plus10 = start_date+datetime.timedelta(seconds=10)
    start_date_plus10 = start_date_plus10.strftime('%Y-%m-%d %H:%M:%S')
    
    s_date.append(start_date.strftime('%Y-%m-%d %H:%M:%S'))
    e_date.append(end_date.strftime('%Y-%m-%d %H:%M:%S'))
    f_date.append(start_date_plus10)
    
    time_stamp_list = [datetime.datetime.fromtimestamp(info_data['locations'][j]['timestamp']/ 1e3).strftime('%Y-%m-%d %H:%M:%S') for j in np.arange(len(info_data['locations'])-1)]
    try: 
        find_index = time_stamp_list.index(start_date_plus10)
        #if len(find_index)>0:
        lat = info_data['locations'][find_index]['latitude']
        lon = info_data['locations'][find_index]['longitude']
        lon_list.append(lon)
        lat_list.append(lat)
#        location = geolocator.reverse(str(lat)+","+str(lon))
#        country.append(location[0].split(',')[-1])
#        state.append(location[0].split(',')[-3])
#        city.append(location[0].split(',')[-4])
    except:
#    else:
        
        print('not found')
        
        lon_list.append(np.nan)
        lat_list.append(np.nan)
#        country.append(None)
#        state.append(None)
#        city.append(None)
            

label_list['video_name'] = movie_name 
label_list['longitude'] = lon_list
label_list['latitude'] = lat_list
label_list['bin_busses'] = 0
label_list['bin_busses'].loc[label_list['n_busses']>0] = 1
label_list['start_date'] = pd.to_datetime(s_date)
label_list['end_date'] = pd.to_datetime(e_date)
label_list['frame_date'] = pd.to_datetime(f_date)
#label_list['country'] = country
#label_list['state'] = state
#label_list['city'] = city

lat = label_list['latitude'].loc[~label_list['latitude'].isna()]
lon = label_list['longitude'].loc[~label_list['latitude'].isna()]

country = list()
state = list()
city = list()
for i in np.arange(len(lat)):
    print(i)
    location = geolocator.reverse(str(lat.iloc[i])+","+str(lon.iloc[i]))
    country.append(location[0].split(',')[-1])
    state.append(location[0].split(',')[-3])
    city.append(location[0].split(',')[-4])
    
    
label_list['country'] = ''
label_list['state'] = ''
label_list['city'] = ''
label_list['country'].loc[~label_list['latitude'].isna()] = country
label_list['state'].loc[~label_list['latitude'].isna()] = state
label_list['city'].loc[~label_list['latitude'].isna()] = city

label_list.to_csv(os.path.join(path_FPAI,'IdealAlgoOutput_fromlabeled_val.csv'))
########
# load saved table
label_list=pd.read_csv(os.path.join(path_FPAI,'IdealAlgoOutput_fromlabeled_val.csv'))
########

fig = px.scatter_mapbox(label_list.loc[label_list['city']==' City of New York',:], 
                     lat='latitude',lon='longitude', 
                     hover_name="n_busses",
                     size ="n_busses",
                     color="n_busses",#"city",
                     hover_data= {
                        "start_date": False,
                        "end_date": False,
                        "bin_busses": False,
                        "frame_date": False,
                        "weather": True,
                        "scene": True,
                        "longitude": False,
                        "latitude": False,
                        "timeofday": True,
                        "n_busses": True,
                        "n_cars": True},
                    #animation_frame="frame_date", animation_group="n_busses",
                    #color_continuous_scale=px.colors.cyclical.IceFire, 
                    size_max=15,
                    color_discrete_sequence=["black","yellow","red", "orange","green", 
                                                "blue", "goldenrod", "magenta"], 
                        zoom=8, height=1000,width=1000)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":100,"t":10,"l":100,"b":100}, 
                  legend=dict(orientation="h"))
fig.update_traces(marker_coloraxis=None)
#fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.show()

import plotly.figure_factory as ff

tmp = label_list.loc[label_list['city']==' City of New York',:]
tmp.sort_values(['frame_date'], inplace = True)
tmp['date'] = pd.to_datetime(tmp['frame_date']).dt.date.astype(str)
tmp['hour'] = pd.to_datetime(tmp['frame_date']).dt.hour
tmp = tmp.iloc[0:5000,:]



#px.set_mapbox_access_token(open(os.path.join(path_FPAI,".mapbox_token")).read())
api_token = 'pk.eyJ1IjoiZ2l1c2NoaSIsImEiOiJja29iZHJ1cHAxZGR1Mm9tcTMwMno2Mm9uIn0.XFFL7SFpHHP3ZqYUq_XeiA'
fig = ff.create_hexbin_mapbox(
    data_frame=tmp, lat=tmp['latitude'], lon=tmp['longitude'],
    nx_hexagon=30, opacity=0.8, labels={"color": "Summed n_busses"},
    color="n_busses", agg_func=np.sum, color_continuous_scale="Magma",
    mapbox_style="open-street-map",show_original_data=True, 
    original_data_marker=dict(opacity=0.2, size=5, color="red"), 
    zoom=10,
)
fig.update_layout( mapbox_accesstoken=api_token, mapbox_style = 'streets')#"basic")
fig.show()

fig = ff.create_hexbin_mapbox(
    data_frame=tmp, lat=tmp['latitude'], lon=tmp['longitude'], 
    nx_hexagon=30, 
    animation_frame="timeofday",#"date", 
    #color_continuous_scale="sunset",#color_continuous_scale="Cividis", 
    color_continuous_scale="Magma",
    color="n_cars", 
    agg_func=np.sum,#agg_func=np.sum, 
    labels={"color": "Total Cars", "frame": "Date"},
    opacity=0.8, min_count=1,#mapbox_style="open-street-map",
    zoom=10,
    show_original_data=True, 
    original_data_marker=dict(opacity=0.2, size=5, color="red")
)
fig.update_layout( mapbox_accesstoken=api_token, mapbox_style = 'streets')#"basic")

fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
fig.layout.sliders[0].pad.t=20
fig.layout.updatemenus[0].pad.t=40
fig.show()  

# https://plotly.com/python/hexbin-mapbox/

#https://stackoverflow.com/questions/67056641/how-to-generate-2d-gaussian-kernel-using-2d-convolution-in-python
