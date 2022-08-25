#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 18:51:11 2022

@author: giu

"""

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
fps = 30
image_timing_sec = 10

frame = fps*image_timing_sec

########
# load saved table
label_list=pd.read_csv(os.path.join(path_FPAI,'IdealAlgoOutput_fromlabeled_val.csv'))

video_1 = 'cabc30fc-e7726578'
video_2 = 'cabc30fc-eb673c5a'

m1v1_out = pd.read_csv(os.path.join(path_FPAI,video_1+'_yolov5_output.csv'))
m2v1_out = pd.read_csv(os.path.join(path_FPAI,video_1+'_yolov7_output.csv'))

m1v2_out = pd.read_csv(os.path.join(path_FPAI,video_2+'_yolov5_output.csv'))
m2v2_out = pd.read_csv(os.path.join(path_FPAI,video_2+'_yolov7_output.csv'))


list_videos = label_list['video_name'].tolist()



models_output = pd.concat([m1v1_out.iloc[frame,:][['n_cars', 'n_busses', 'n_trucks', 'n_peds']],
        m2v1_out.iloc[frame,:][['n_cars', 'n_busses', 'n_trucks', 'n_peds']],


m1v2_out.iloc[frame,:][['n_cars', 'n_busses', 'n_trucks', 'n_peds']],
m2v2_out.iloc[frame,:][['n_cars', 'n_busses', 'n_trucks', 'n_peds']]], axis = 1)
models_output.columns = ['m1_v1','m2_v1','m1_v2','m1_v']