#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from road import MakeRoad
from plot import plot_data, plot3d
from config import read_params, read_bottlenecks

#reading model parameters from configuration file
params = read_params()

#building the road
road = MakeRoad(**params)
road.make_cells()

#reading bottleneks

bns = read_bottlenecks(road)

road.data.append([c.density for c in road.cell[1:-1]])
for i in range(road.iteration):
    
    #setting to zero bottlenecks strenght
    for c in road.cell:
        c.bn_reduction = 0
    
    #check bottlenecks
    for row in bns.itertuples():
        #check time
        if i in range(row.ti_index, row.tf_index):
            #check space
            for c in road.cell[row.start_index:row.end_index]:
                c.bn_reduction += row.strenght
            
    road.update_density()
    road.data.append([c.density for c in road.cell[1:-1]])
    
plot_data(road)
plot3d(road)
