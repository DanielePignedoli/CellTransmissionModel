#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def plot_data(road, filename):
    """
    Plot the density evolution of the simulation.
    
    Display a colormap with increasing time on the y-axis, and road position on
    the x-axis. The more intense the colour, the higher the density of the cell.
    
    Parameters
    ----------
    road : road.Road
        Road object of the actual simulation.
    filename : str
        Filename of the output file.
    """
    #save -> file name of the output image
    fig, ax = plt.subplots(figsize=(8,5))
    im = ax.pcolormesh(road.data, cmap = 'PuBu')
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
    
    fig.savefig(filename)
    


