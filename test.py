#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hypothesis import given, settings
from hypothesis import strategies as st
from road import MakeRoad
import numpy as np

@given(st.floats(1),st.floats(1), st.floats(1),st.floats(0.01))
@settings(max_examples=1)
def test_initialisation(L,pmax,V,T):
    #test variables after initialization
    road = MakeRoad(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
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
    #test for variables after several steps of the simulation
    road = MakeRoad(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
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
    #test if output data are all real values below max density
    road = MakeRoad(road_length = L,density_max = pmax,free_v = V,mean_time_gap = T,source=0.8)
    road.make_cells()
    
    road.data.append([c.density for c in road.cell[1:-1]])
    for i in range(it):
        road.update_density()
    road.data.append([c.density for c in road.cell[1:-1]])

    output = np.array(road.data)
    
    assert not np.isnan(output).all()
    assert (output <= road.density_max).all()
        
