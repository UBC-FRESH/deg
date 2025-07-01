# import modules
import os
from os import listdir
from os.path import isfile, join
import sys

########################################################################################################
gep_dev = True
if gep_dev:
    ws3_path = '../lib/ws3'
    try:
        _path = os.path.abspath(os.path.join(os.path.dirname(__file__), ws3_path))
    except:
        _path = os.path.abspath(os.path.join(os.path.dirname('__file__'), ws3_path))
    if not _path in os.sys.path:
        os.sys.path.insert(0, _path)
import ws3
from ws3.forest import ForestModel, Action
from ws3.spatial import ForestRaster
from ws3.common import clean_vector_data, reproject_vector_data, rasterize_stands, hash_dt, warp_raster
########################################################################################################

import numpy as np
import pandas as pd
from pandas import DataFrame as DF
import geopandas as gpd
import matplotlib.pyplot as plt
import gurobipy as grb
import rasterio
import rasterio.plot
import seaborn as sns
from functools import partial
import fiona
import folium
import pathlib
try:
   import cPickle as pickle
except:
   import pickle
import copy
from pathlib import Path
import rasterio
import shutil

from deg import *

# configure paths and global variables
deg_mode = 'rhrs' # 'classic'
sda_mode = 'randblk' # 'randpxl'
obj_mode = 'max_hvol' # 'max_harea'
horizon = 6
period_length = 10
max_age = 100
dat_path = '../dat'
basenames = read_basenames(dat_path+'/basenames.txt')
yld_path = '%s/yld.csv' % dat_path
tolerance = 10.
clean_inv = False
rasterize_inv = False
gdb_path = lambda bn: '%s/gdb/%s.gdb' % (dat_path, bn)
shp_path = lambda bn: '%s/shp/%s.shp' % (dat_path, bn)
tif_path = lambda bn: '%s/tif/%s.tif' % (dat_path, bn)
shp_name = 'stands'
age_col = 'age'
theme_cols = ['theme0', 'theme1', 'theme2', 'theme3']
compress = 'lzw'
dtype = rasterio.uint8
base_year = 2015
prop_names = [u'THLB', u'AU', u'LdSpp', u'Age2015', u'Shape_Area']
prop_types = [(u'theme0', 'str:10'),
              (u'theme1', 'str:1'),
              (u'theme2', 'str:5'), 
              (u'theme3', 'str:50'), 
              (u'age', 'int:5'), 
              (u'area', 'float:10.1')]
tvy_name = 'totvol'
snk_epsg = 3005 # ESPG:3005 corresponds to NAD83/BC Albers
sns.set_style('dark')
hdt_path = '%s/hdt' % dat_path
coast_bn = ['tsa01', 'tsa02', 'tsa03'] # FIX ME: totally bogus (check GIS data for real coast TSA codes) 
_p_slashburn = read_pslashburn('%s/p_slashburn.csv' % dat_path)
p_slashburn = lambda bn: _p_slashburn[bn]
# oe = operability expression
# ogi = old growth index
oe_harvest = '_age >= 4 and ogi <= 0.99' if scenario_name == 'rogh' else '_age >= 4 and _age <= 99'
action_params = {'harvest':
                    {'oe':oe_harvest,
                     'mask':('?', '1', '?', '?'),
                     'is_harvest':True,
                     'targetage':0},
                 #'harvest_ct30':
                 #   {'oe':oe_harvest,
                 #    'mask':('?', '1', '?', '?'),
                 #    'is_harvest':True,
                 #    'targetage':0},
                 'fire':
                    {'oe':'_age >= 4 and _age <= 99',
                     'mask':('?', '?', '?', '?'),
                     'is_harvest':False,
                     'targetage':0}}
util = 0.90 if scenario_name == 'more' else 0.85

proc_mode = 'seq_tsa'
deg_mode = 'rhrs' #'classic'
obj_mode = 'min_harea'
run_sda = 1 # set to True for production runs
twopass_cacut_factor = 1.35
fm_horizon = horizon