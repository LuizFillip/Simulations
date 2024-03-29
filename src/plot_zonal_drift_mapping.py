import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs
import datetime as dt 
import numpy as np 
import base as b 
from tqdm import tqdm 


b.config_labels()


def velocity(v):
    return v * 3.6
def displacement(x0, v0, dt):
    return (x0 + v0 * dt / 111)  



def mappping(time):
    fig, ax = plt.subplots(
        dpi = 300,
        ncols = 1,
        figsize = (10,10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    gg.map_attrs(ax, time.year)
    gg.plot_rectangles_regions(ax, time.year, delta1 = 3)
    
    ax.set(title = time.strftime("%H:%M:%S (UT)"))

    return fig, ax


def ellipse(
        center, 
        angle = 110, 
        semi_major = 10.0, 
        semi_minor = 1.0
        ):
     
    
    angle_rad = np.deg2rad(angle)
    
    t = np.linspace(0, 2 * np.pi, 100)
 
    x = (center[0] + semi_major * np.cos(t) * 
         np.cos(angle_rad) - semi_minor * np.sin(t) * 
         np.sin(angle_rad))
    
    y = (center[1] + semi_major * np.cos(t) * 
         np.sin(angle_rad) + semi_minor * 
         np.sin(t) * np.cos(angle_rad))
    
    return x, y

def plot_ellipse(
        ax, 
        year = 2014, 
        lon = -60, 
        semi_major = 10.0
        ):
    
   
    eq_lon, eq_lat  = gg.load_equator(
        year, values = True)
    
    i = b.find_closest(eq_lon, lon)
    
    x, y = ellipse(
        (eq_lon[i], eq_lat[i]), 
        semi_major = semi_major
        )
    
    ax.plot(x, y, color = 'k')
   
    ax.fill(x, y, color = 'gray', alpha = 0.5)
    
def plot_terminator_line(ax, dn):
    
    te_lon, te_lat = gg.terminator2(dn, 18)
    
    eq_lon, eq_lat = gg.load_equator(dn.year, values = True)
    
    ilon, ilat = gg.intersection(eq_lon, eq_lat, te_lon, te_lat)
    
    ax.scatter(te_lon, te_lat, c = 'k', s = 5)
    
    ax.scatter(ilon, ilat, c = 'k', s = 5)


    if len(ilon) > 1 and len(ilat) > 1:
        ilon = ilon[0]
        ilat = ilat[0]
        
    return ilon




def growth_phase(
        ax, 
        epb_lon, 
        count, 
        max_edge = 10
        ):
    
    if count <= max_edge: 

        plot_ellipse(
                 ax, lon = epb_lon, 
                 semi_major = count
                 )
        
    else:
        
        plot_ellipse(
                 ax, 
                 lon = epb_lon, 
                 semi_major = max_edge
                 )
        
    return None



def save_figs(fig, time):
    b.make_dir('temp')
    name = time.strftime('%Y%m%d%H%M')
    fig.savefig(f'temp/{name}')
    return 


def update(start, Dt):
    delta = dt.timedelta(hours = Dt)
    return start + delta

def sunset_developing(ax, ilon, Dt, count, x0 = -60, v0 = 100):
    
    ax.text(
        0.1, 0.8, 
        '$V_{zonal}$ = ' + f'{v0} m/s', 
        transform = ax.transAxes
        )
    
    epb_lon = displacement(x0, velocity(v0), Dt)
    
    if (epb_lon > ilon):
        count += 1 
        growth_phase(ax, epb_lon, count)
        
    return count


def sunset_chain_occurrence(start, v0 = 100):

    longs_start = [-50, -60, -70, -80]
    
    counts = {x0: 0 for x0 in longs_start}
        
    for Dt in np.arange(0, 3, 0.02):
        
        plt.ioff()
        time = update(start, Dt)

        fig, ax = mappping(time)
        ilon = plot_terminator_line(ax, time)
        
        for x0 in longs_start:
            counts[x0] = sunset_developing(
                ax, 
                ilon, 
                Dt, 
                counts[x0], 
                x0 = x0, 
                v0 = v0
                )
            
            
        save_figs(fig, time)
        
        plt.clf()   
        plt.close()
            
            
            

start = dt.datetime(2013, 1, 1, 22, 0)

sunset_chain_occurrence(start, v0 = 100)
    
    
b.images_to_movie(
        path_in = 'temp/', 
        path_out = '',
        movie_name = 'test',
        fps = 12
        )