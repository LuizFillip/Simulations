import matplotlib.pyplot as plt
import GEO as gg 
from simullations import displacement, velocity

def plot_drift_velocities(ax, Dt, epb_dn, x0 = -60):
    for i, v0 in enumerate([50, 100, 200]):
        
        plot_terminator_and_equator(ax[i], epb_dn)
        
        epb_lon = displacement(x0, velocity(v0), Dt)
    
        gg.plot_ellipse(ax[i], lon = epb_lon)
    
        ax[i].set(title =  f'$v_{{zonal}}$ = {v0} m/s')

def mappping(year):
    fig, ax = plt.subplots(
        dpi=300,
        ncols = 3,
        figsize=(16, 12),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    for i in range(3):
        gg.map_attrs(ax[i], year)
        plot_corners(ax[i], year, radius = 10)
        if i != 0:
            ax[i].set(
                xticklabels = [], 
                yticklabels = [], 
                ylabel = '', 
                xlabel = '')
    
    return fig, ax