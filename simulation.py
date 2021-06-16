#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from road import MakeRoad
from plot import plot_data

#reading model parameters from configuration file
config = pd.read_csv('config.csv', sep = '=', names = ['variable', 'value'])
config = config.dropna()

params_dict = {}
for var,value in config.values:
    params_dict[var] = value

#building the road
road = MakeRoad(**params_dict)
road.make_cells()

#reading bottleneks, and conerting units in model indexes
bns = pd.read_csv('bottlenecks.csv', sep=',')
bns['start_index']= bns['start'].apply(lambda x : round(x/road.cell_length))
bns['end_index']= bns['end'].apply(lambda x : round(x/road.cell_length))
bns['ti_index']= bns['time_i'].apply(lambda t : round(t/road.dt/60))
bns['tf_index']= bns['time_f'].apply(lambda t : round(t/road.dt/60))


road.data.append([c.density for c in road.cell])
for i in range(road.iteration):
    
    #check bottlenecks
    for row in bns.itertuples():
        #check time
        if i in range(row.ti_index, row.tf_index):
            #check space
            for c in road.cell[row.start_index:row.end_index]:
                c.bn_reduction = row.strenght
        else:
            for c in road.cell[row.start_index:row.end_index]:
                c.bn_reduction = 0
            
    road.update_density()
    road.data.append([c.density for c in road.cell])
    
plot_data(road, filename = 'prova.png')

