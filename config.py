#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def read_params(file = 'configuration.csv'):
    """
    Read model parameters from configuration file.
    
    Read paramaters from a csv file, with '=' as separator, then convert 
    them into dictionary.
    
    Parameters
    ----------
    file : str
        Path of the cofiguration file.
        
    Returns
    -------
    dict
        Dictionary with the assigned parameters.
    """
    
    config = pd.read_csv(file, sep = '=', header=2)
    config = config.dropna()
    
    params_dict = {}
    for var,value in config.values:
        params_dict[var] = value
    
    return params_dict

def read_bottlenecks(road, file = 'bottlenecks.csv'):
    """
    "Read bottleneks cconvert units in model indexes.
    
    Read paramaters from a csv file, converting them into a pandas dataframe with
    a row for each bottleneck.
    
    The position of bottlenecks is then converted into a cell index, and also
    the lifetime is coverted into iteration indexes.
    
    Parameters
    ----------
    road : road.Road
        Road object of the actual simulation.
    file : str
        Path of the cofiguration file.
        
    Returns
    -------
    pandas.DataFrame
        Dataframe with strength, position and lifetime of each bottlenecks.
    """
    bns = pd.read_csv(file, sep=',', header = 1)
    bns['start_index']= bns['start'].apply(lambda x : round(x/road.cell_length))
    bns['end_index']= bns['end'].apply(lambda x : round(x/road.cell_length))
    bns['ti_index']= bns['time_i'].apply(lambda t : round(t/road.dt/60))
    bns['tf_index']= bns['time_f'].apply(lambda t : round(t/road.dt/60))
    return bns
