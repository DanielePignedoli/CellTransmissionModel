#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def plot_data(road, filename : str = None, cmap = 'PuBu'):
    #save -> file name of the output image
    fig, ax = plt.subplots(figsize=(8,5))
    cmap = plt.get_cmap(cmap)
    
    im = ax.pcolormesh(road.data, cmap = cmap)
    fig.colorbar(im)
    
    #title
    ax.set_title('Density distribution over time' , fontsize = 14)
    
    #x axis
    ax.set_xlabel('position (km)', fontsize = 12)
    xticks = [round(i*road.cell_length,2) for i in range(0,road.n_cells,2)]
    plt.xticks(range(0,road.n_cells, 2),xticks)
    
    #y axis
    yticks = [round(i*road.dt*60,1) for i in range(0,road.iteration,10)]
    plt.yticks(range(0,road.iteration,10),yticks)
    ax.set_ylabel('time (min)', fontsize = 12)
        
    fig.tight_layout()
    if filename:
        fig.savefig(filename)
    fig.show()


def plot3d(road,filename : str = None):
    
    data=road.data
    fig = plt.figure(figsize=(8,5))
    ax = plt.axes(projection='3d')
    #ax=Axes3D(fig)
    
    #Z = np.array(data)
    
    x = range(len(data[0]))
    y = range(len(data))
    
    #X,Y = np.meshgrid(x,y)
    
    for time in y:
        ax.plot3D(x,[time]*len(x),data[time], c = 'b',alpha = 0.2)   

    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
    #ax.plot_wireframe(X,Y,Z)
    
    #title
    ax.set_title('Density distribution over time' , fontsize = 14)
    
    #x axis
    ax.set_xlabel('position (km)', fontsize = 12,labelpad= 10)
    xticks = [round(i*road.cell_length,2) for i in range(0,road.n_cells,3)]
    plt.xticks(range(0,road.n_cells, 3),xticks, rotation = 30)
    
    #y axis
    yticks = [round(i*road.dt*60,1) for i in range(0,road.iteration,10)]
    plt.yticks(range(0,road.iteration,10),yticks)
    ax.set_ylabel('time (min)', fontsize = 12)
    
    #z axis
    ax.set_zlabel('density', fontsize=12)
    
    #fig.tight_layout()
    
    #ax.view_init(40, 120)
    
    fig.show()
    if filename:
        fig.savefig(filename)
    fig.show()
