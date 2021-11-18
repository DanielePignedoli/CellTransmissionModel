#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import read_bottlenecks, read_params
from road import Road, Cell
import pandas as pd
import os
import numpy as np
import unittest

class CTM_test(unittest.TestCase):
    
    def setUp(self):
        """
        Compute following code before each test.
        """
        self.road = Road(road_length = 3.0,density_max = 120.0,free_v = 50.0,mean_time_gap =0.6,source=0.8)
        self.road.make_cells()
        self.cell = Cell(self.road)
        
    def test_read_params(self):
        """
        Test if the configuration file reading function.
        
        Test if the returned dictionary is what we expect to be.
        """
        test_dict = {'road_length':3 ,'density_max':120, 'free_v':50,
                       'mean_time_gap':0.6, 'simulation_time':0.2,
                       'source':0.8, 'sink':1}
        params = read_params('configuration.csv')
        
        self.assertDictEqual(params,test_dict)
         
    def test_read_bottlenecks(self):
        """
        Test the bottlenecks configuration reading function.
        
        Test if the computed values of the returned dataframe are in
        agreement with the input values.
        """ 
        for file in os.listdir('conf_test/'):
            file_name = 'conf_test/' + file
            bns = read_bottlenecks(self.road, file_name)
            bns_df=pd.read_csv(file_name, header = 1) 
            
            for i in bns_df.index:
                self.assertAlmostEqual(bns['start_index'][i]*self.road.cell_length,bns_df['start'][i],1)
                self.assertAlmostEqual(bns['end_index'][i]*self.road.cell_length,bns_df['end'][i],1)
                self.assertAlmostEqual(bns['ti_index'][i]*self.road.dt*60,bns_df['time_i'][i],1)
                self.assertAlmostEqual(bns['tf_index'][i]*self.road.dt*60,bns_df['time_f'][i],1)
    
    def test_update_bottlenecks(self):
        """
        Test the presence of a bottlenecks in a cell at a certain time.
        
        The Cell class attribute bn.reduction must be equal to the strength
        of the bottlenecks when it is ative. This methods tested the 
        function with several pre-prepared configurtion files.
        """
        for file in os.listdir('conf_test/'):
            file_name = 'conf_test/' + file
            bns = read_bottlenecks(self.road, file_name)
            bns_df= pd.read_csv(file_name, header = 1)
            
            for it in range(0,self.road.iteration,10):
                self.road.update_bottlenecks(bns,it)
                for i in bns_df.index:
                    if it in range(bns['ti_index'][i],bns['tf_index'][i]):
                        bn_index = bns['start_index'][i]
                        assert self.road.cell[bn_index].bn_reduction == bns['strength'][i] 
            
    def test_init(self):
        """
        Test Road class attributes after initialization.
        
        Test if the attributes are well computed, and check the 
        fairness of some costrains.
        """
        
        assert self.road.cong_v == -3600/(self.road.density_max * self.road.mean_time_gap) 
        assert self.road.iteration == round(self.road.simulation_time/self.road.dt)
        assert self.road.cell_length == self.road.free_v * self.road.dt
        assert self.road.n_cells == round(self.road.road_length/self.road.cell_length)
        assert self.road.max_flow == self.road.density_max*self.road.free_v*self.road.cong_v/(self.road.cong_v-self.road.free_v)
        assert self.road.p_c == self.road.max_flow/self.road.free_v
        
        assert self.road.cell_length < self.road.road_length 
        assert self.road.cong_v < 0
        assert self.road.p_c < self.road.density_max 

    def test_make_cells(self):
        """
        Test the building of the road with cells.
        
        Test number of cells, test if source and sink cells' variables 
        respect physical costrains.
        """
        assert len(self.road.cell) == self.road.n_cells + 2
        for c in self.road.cell:
            self.assertIsInstance(c,Cell)
        
        assert self.road.cell[0].demand/self.road.max_flow <= 1
        assert self.road.cell[-1].supply/self.road.max_flow <= 1
            
    def test_update_density(self):
        """
        Test density evolution in different times.
        
        Test if the density in each cell respect physical costrain.
        """
        for max_iter in range(1,100,10):
            for i in range(max_iter):
                self.road.update_density()
        
            for c in self.road.cell[1:-1]:
                assert c.density <= self.road.density_max
                assert c.density >= 0
                assert c.flow <= self.road.max_flow
                assert c.flow >= 0
            
    def test_simulation(self):
        """
        Test the otput of a simulation.
        
        The output must respect some constrains, moreover this methods
        tests if the density increase in a cell before an active bottlenecks.
        """
        bns = pd.DataFrame(columns = ['start_index','end_index','strength','ti_index','tf_index'],
                           data = [[10,10,1,0,30]])
        self.road.simulation(bns)
        
        output = np.array(self.road.data)
        assert len(self.road.data) == self.road.iteration+1
        assert not np.isnan(output).all()
        assert (output <= self.road.density_max+1).all()
        assert (output >= 0 ).all()
        
        #check evolution in a cell close to the bottlenecks
        #bns_output is the fraction of output data of a cell before the bottlenecks   
        bns_output = [ output[i][8] for i in range(30)]
        check = bns_output.copy()
        check.sort()
        
        assert bns_output == check
                     
    def test_update_capacity(self):
        """
        Test updating Cell method. 
        
        Test if with a chosen input it gets the correct output.
        """
        self.cell.update_capacity()
        old_c = self.cell.capacity
        
        self.cell.bn_reduction = 0.4
        self.cell.update_capacity()
        assert old_c > self.cell.capacity
    
    def test_flow_equilibrium(self):
        """
        Test updating Cell method. 
        
        Test if with a chosen input it gets the correct output.
        """
        self.cell.density = -1
        self.cell.flow_equilibrium()
        assert self.cell.flow == 0
        
        self.cell.density = self.road.density_max + 1
        self.cell.flow_equilibrium()
        assert self.cell.flow == 0
        
        self.cell.density = self.road.p_c
        self.cell.flow_equilibrium()
        assert self.cell.flow == self.road.max_flow
            
    def test_update_demand(self):
        """
        Test updating Cell method. 
        
        Test if with a chosen input it gets the correct output.
        """
        self.cell.density = self.road.p_c - 1
        self.cell.flow_equilibrium()
        self.cell.update_demand()
        assert self.cell.demand == self.cell.flow
        
        self.cell.density = self.road.p_c + 1
        self.cell.update_capacity()
        self.cell.update_demand()
        assert self.cell.demand == self.cell.capacity
        
    def test_update_supply(self):
        """
        Test updating Cell method. 
        
        Test if with a chosen input it gets the correct output.
        """
        self.cell.density = self.road.p_c + 1
        self.cell.flow_equilibrium()
        self.cell.update_supply()
        assert self.cell.supply == self.cell.flow
        
        self.cell.density = self.road.p_c - 1
        self.cell.update_capacity()
        self.cell.update_supply()
        assert self.cell.supply == self.cell.capacity
    
    