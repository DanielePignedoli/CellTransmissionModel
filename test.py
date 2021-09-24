#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hypothesis import given
from hypothesis import strategies as st
from road import MakeRoad
import config

@given(params = {road_length, density_max, free_v, num_lanes, mean_time_gap, simulation_time, dt, source, sink{})
def test_config_params():
    assert type(MakeRoad(**params)) = MakeRoad
    
    
    
