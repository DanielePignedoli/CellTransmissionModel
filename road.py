#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Road():
        
    #road params
    free_v : float  #km/hr
    cong_v : float = field(init=False) #km/hr
    mean_time_gap : float #sec
    road_length : float  #km
    density_max : float   #vehicles/km  (lane average)
    source : float = 0 #fraction of max_flow, acts as source flow
    sink : float = 1 #same as source, manage the out flow
  
    
    #parameters to initialise
    iteration : int = field(init=False)
    cell_length : float = field(init=False)
    n_cells : int = field(init=False)
    max_flow : float = field(init=False)    #max flow per lane
    p_c : float = field(init=False)        #crtical density
    
    #method parameter
    dt : float = field(default=1/600) #hr
    simulation_time : float = field(default=1/6) #hr, so 10 min
    
    #output
    data : list =  field(default_factory = list)
    
    def __post_init__(self):
        #computation of all other useful variables
        self.cong_v = -3600/(self.density_max * self.mean_time_gap) #negative velocity of traffic waves in congested regime
        self.iteration = round(self.simulation_time/self.dt)
        self.cell_length = self.free_v * self.dt
        self.n_cells = round(self.road_length/self.cell_length)
        self.max_flow = self.density_max*self.free_v*self.cong_v/(self.cong_v-self.free_v) #lanes averaged maximum flow
        self.p_c = self.max_flow/self.free_v #critical density, at which road change from fre to congested
        
    def make_cells(self):
        #this methods builds all the cells of the road
        self.cell = []
        for i in range(self.n_cells+2): # two more cells for source and sink
            self.cell.append(Cell(self))
        self.cell[0].demand = self.source*self.max_flow
        self.cell[-1].supply = self.sink*self.max_flow
    
    def update_density(self):
        #this method update each cell's variables, then compue the density starting from the flows at cells' boundaries
        
        for c in self.cell[1:-1]:
            c.update_capacity()
            c.flow_equilibrium()
            c.update_supply()
            c.update_demand()
        
        demands = [c.demand for c in self.cell[:-1]]
        supplies = [c.supply for c in self.cell[1:]]
        
        flows = np.minimum(demands, supplies) # flows at bounaries
        
        for num, c in enumerate(self.cell[1:-1]): #compute new density
            c.density = c.density +(flows[num] - flows[num+1])*self.dt/self.cell_length

    def update_bottlenecks(self, bottlenecks, it):
        #setting to zero bottlenecks strength
        for c in self.cell:
            c.bn_reduction = 0
        
        #check bottlenecks
        for row in bottlenecks.itertuples():
            #check bottlenecks' time position
            if it in range(row.ti_index, row.tf_index):
                #check bottlenecks' space position
                if self.cell[row.start_index:row.end_index]:
                    for c in self.cell[row.start_index:row.end_index]:
                        c.bn_reduction += row.strength
                #if for a traffic light one put same postion for start and end
                else:
                    for c in self.cell[row.start_index:row.end_index+1]:
                        c.bn_reduction += row.strength
                             
    def simulation(self,bottlenecks):
        self.data.append([c.density for c in self.cell[1:-1]])
        for i in range(self.iteration):
            self.update_bottlenecks(bottlenecks,i)
            self.update_density()
            self.data.append([c.density for c in self.cell[1:-1]])

@dataclass
class Cell():
    
    #road
    road : Road
    
    #cell variables
    density : float = field(default=0)
    flow : float = None
    bn_reduction : float = field(default = 0)  #strength of the bottleneck
    
    supply : float = field(init=False) # flow supply
    demand : float = field(init=False)   # flow demand
    capacity : float = field(init=False) # capacity of the cell
    
    #source&sink
    source : float = field(default = 0)  # fraction of capacity
    sink : float = field(default = 1)  # fraction of capacity

        
    def update_capacity(self):
        self.capacity = self.road.max_flow*(1-self.bn_reduction)

    def update_supply(self):
        if self.p_avg > self.road.p_c:
            self.supply = self.flow
        else:
            self.supply = self.capacity
    
    def update_demand(self):
        if self.p_avg <= self.road.p_c:
            self.demand = self.flow
        else:
            self.demand = self.capacity
        
    
    def flow_equilibrium(self):
        #p_avg is the lane averaged density
        self.p_avg = self.density
        
        #return the total flow in the cell, depending on the denisty (from the fundamental diagram)
        if self.p_avg<0:
            self.flow = 0
            
        elif self.p_avg <= self.road.p_c:
            self.flow = self.road.free_v*self.p_avg
            
        elif self.p_avg > self.road.density_max:
            self.flow = 0
            
        else:
            self.flow = (self.road.max_flow*(1-self.road.cong_v/self.road.free_v) + self.road.cong_v*self.p_avg)



    


