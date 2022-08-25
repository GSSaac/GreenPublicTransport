#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 18:44:26 2022

@author: giu

"""
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

path_FPAI = '/Users/giu/Documents/Business/Challenges/GreenerCities_fruitPunchAI/code'


from os import listdir
import os
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'

########
# load saved table
label_list=pd.read_csv(os.path.join(path_FPAI,'IdealAlgoOutput_fromlabeled_val.csv'))

video_1 = 'cabc30fc-e7726578'
video_2 = 'cabc30fc-eb673c5a'

m1v1_out = video_1+'_yolov5_output.csv'
m2v1_out = video_1+'_yolov7_output.csv'

m1v2_out = video_2+'_yolov5_output.csv'
m2v2_out = video_2+'_yolov7_output.csv'

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
