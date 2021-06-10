#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from road import MakeRoad

#reading model parameters from configuration file
config = pd.read_csv('config.csv', sep = '=', names = ['variable', 'value'])
config = config.dropna()
params_dict = {}
for var,value in config.values:
    params_dict[var] = value

#building the road
road = MakeRoad(**params_dict)
