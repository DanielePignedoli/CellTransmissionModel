#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hypothesis import given, settings
from hypothesis import strategies as st
from road import MakeRoad

@given(st.floats(min_value = 1),st.floats(min_value= 1), st.floats(min_value=1),
                 st.floats(min_value=0.01))
@settings(max_examples=1)
def test_configuration(L,pmax,V,T):
    road =  MakeRoad(L,pmax,V,T,source=0.8)
    road.make_cells()
    assert type(road) == MakeRoad
    assert type(road.n_cells) == int
    assert road.cong_v < 0
    assert road.p_c < road.density_max 
    
    
@given(st.floats(min_value = 1),st.floats(min_value= 1), st.floats(min_value=1),
                 st.floats(min_value=0.01))
@settings(max_examples=1)
def test_simulation(L,pmax,V,T):
    road =  MakeRoad(L,pmax,V,T,source=0.8)
    road.make_cells()
    road.update_density()
    
    for c in road.cell[1:-1]:
        assert c.density <= road.density_max
        assert c.density >= 0
        assert c.flow <= road.max_flow
        

        
