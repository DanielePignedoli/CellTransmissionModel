#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def read_params(file = 'config.csv'):
    #reading model parameters from configuration file
    config = pd.read_csv('config.csv', sep = '=', header=2)
    config = config.dropna()
    
    params_dict = {}
    for var,value in config.values:
        params_dict[var] = value
    
    return params_dict

def read_bottlenecks(road, file = 'bottlenecks.csv'):
    #reading bottleneks, and converting units in model indexes
    bns = pd.read_csv('bottlenecks.csv', sep=',', header = 1)
    bns['start_index']= bns['start'].apply(lambda x : round(x/road.cell_length))
    bns['end_index']= bns['end'].apply(lambda x : round(x/road.cell_length))
    bns['ti_index']= bns['time_i'].apply(lambda t : round(t/road.dt/60))
    bns['tf_index']= bns['time_f'].apply(lambda t : round(t/road.dt/60))
    return bns