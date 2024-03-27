import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import GEO as gg



        
def plot_simulate_bubble_drift(year, Dt):
    
    fig, ax = gg.mappping(year)
    
    delta = dt.timedelta(hours = Dt)
    
    epb_dn = dt.datetime(year, 1, 1, 0) + delta
     
    plot_drift_velocities(ax, Dt, epb_dn)
    
    fig.suptitle(epb_dn.strftime("%H:%M:%S (UT)"), y = 0.7)
    
    return fig, epb_dn

year = 2014

twilight = 18


def save_intervals():
    
    for Dt in np.arange(0, 2, 0.02):
    
        plt.ioff()
        
        # fig, epb_dn = plot_simulate_bubble_drift(year, Dt)
        
        fig, ax = gg.mappping(year)
        
        delta = dt.timedelta(hours = Dt)
        
        epb_dn = dt.datetime(year, 1, 1, 0) + delta
         
        # plot_drift_velocities(ax, Dt, epb_dn)
        
        fig.suptitle(epb_dn.strftime("%H:%M:%S (UT)"), y = 0.7)
        
        name = epb_dn.strftime('%Y%m%d%H%M')
        print(name)
        fig.savefig(f'temp/{name}')
            
        plt.clf()   
        plt.close()