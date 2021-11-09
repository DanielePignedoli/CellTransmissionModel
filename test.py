#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hypothesis import given, settings
from hypothesis import strategies as st
import config
from road import Road, Cell
import numpy as np
import pandas as pd
from math import isnan


def test_config():
    """
    Test the configuration file reading.
    """
    params = config.read_params('configuration.csv')
    for key in params.keys():
        assert bool(key) == True
        
@given(st.floats(1),st.floats(1), st.floats(1),st.floats(0.01))
@settings(max_examples=1)
def test_config_botlenecks(L,pmax,V,T):
    """
    Test bottlenecks configuration file reading.
    """
    road = Road(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
    road.make_cells()
    
    bns = config.read_bottlenecks(road, 'bottlenecks.csv')
    assert type(bns) == pd.DataFrame
    assert bns.isna().any().any() == False

@given(st.floats(1),st.floats(1), st.floats(1),st.floats(0.01))
@settings(max_examples=1)
def test_initialisation(L,pmax,V,T):
    """
    Test Road class varables after initialization.
    """
    
    road = Road(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
    road.make_cells()
    
    #test if all the input variables are well initializated
    assert road.mean_time_gap == T 
    assert road.density_max == pmax
    assert road.free_v == V
    assert road.mean_time_gap == T
    
    
    #test for the computed variables
    assert road.cell_length < road.road_length 
    assert road.cong_v < 0
    assert road.p_c < road.density_max 

    
    
@given(st.floats(1),st.floats(1), st.floats(1), st.floats(0.01), st.integers(1))
@settings(max_examples=1)
def test_simulation(L,pmax,V,T,it):
    """
    Test variables after several steps of simulation.
    
    Test methods needed for an actual simulation.
    """
    road = Road(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
    road.make_cells()
    
    for i in range(it):
        road.update_density()
    
    for c in road.cell[1:-1]:
        assert c.density <= road.density_max
        assert c.density >= 0
        assert c.flow <= road.max_flow
        
@given(st.floats(1),st.floats(1), st.floats(1), st.floats(0.01), st.integers(1))
@settings(max_examples=1)
def test_output(L,pmax,V,T,it):
    """
    Test output data.
    """
    road = Road(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
    road.make_cells()
    
    road.data.append([c.density for c in road.cell[1:-1]])
    for i in range(it):
        road.update_density()
    road.data.append([c.density for c in road.cell[1:-1]])

    output = np.array(road.data)
    
    assert not np.isnan(output).all()
    assert (output <= road.density_max).all()
    

@given(st.floats(1),st.floats(0), st.floats(0), st.floats(0))
@settings(max_examples=2)
def test_cell_updates(p,S,D,C):     
    """
    Test Cella class methhods.
    """
    road = Road(road_length = 3.0,density_max = 120.0,free_v = 50.0,mean_time_gap = 0.06,source=0.8)
    cell = Cell(road)
    
    cell.density = p
    cell.capacity = C
    cell.supply = S
    cell.demand = C
    
    cell.flow_equilibrium()
    assert isnan(cell.flow) == False 
    
    cell.update_capacity()
    cell.update_demand()
    cell.update_supply()
    assert isnan(cell.capacity) == False
    assert isnan(cell.demand) == False
    assert isnan(cell.supply) == False    
    
    
    