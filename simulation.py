#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from road import Road
from plot import plot_data
from config import read_params, read_bottlenecks
from argparse import ArgumentParser
from os import mkdir
from shutil import copyfile
from datetime import datetime

parser = ArgumentParser(description='Simulate the density evolution of a road') 
parser.add_argument('-f','--filename',
                    help='Filename of the output')
parser.add_argument('-p','--params',
                    help='csv file with model parameters')
parser.add_argument('-b','--bottlenecks',
                    help='csv file with bottlenecks parameters')
args = parser.parse_args()

#reading model parameters from configuration file
params = read_params(args.params)

#building the road
road = Road(**params)
road.make_cells()

#reading bottleneks
bns = read_bottlenecks(road, args.bottlenecks)

#simulation with the chosen bottlenecks
road.simulation(bns)


#saving output
if args.filename:
    name = args.filename
else:
    date = datetime.now().strftime("%d-%b-%Y_%H:%M:%S")
    name = 'density_plot_'+date

#directory with output and configuration
directory_name ='output/'+name
mkdir(directory_name)

plot_data(road, directory_name+'/plot.png')

copyfile(args.params, directory_name+'/configuration.csv')
copyfile(args.bottlenecks, directory_name+'/bottlenecks.csv')
