import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs
import datetime as dt 
import numpy as np 
import base as b 

import PlasmaBubbles as pb 
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
    
    ax.plot(x, y)
   
    ax.fill(x, y, color = 'gray', alpha = 0.5)
    
def plot_terminator_line(dn):
    
    lon, lat = gg.terminator2(dn, 18)
    
    eq_lon, eq_lat = gg.load_equator(year, values = True)
    ilon, ilat = gg.intersection(eq_lon, eq_lat, lon, lat)
    
    ax.scatter(lon, lat, c = 'k', s = 5)
    
    ax.scatter(ilon, ilat, c = 'k', s = 5)


    if len(ilon) > 1 and len(ilat)>1:
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
                 semi_major=count)
        
    else:
        
        plot_ellipse(
                 ax, lon = epb_lon, 
                 semi_major=max_edge)
year = 2013
start = dt.datetime(year, 1, 1, 23, 0)

b.make_dir('temp')

def run(start_day, v0 = 100, x0 = -60):
    
    term = pb.terminator(x0, start_day, float_fmt = False) 
    count = 0
    for i, Dt in enumerate(np.arange(0, 2, 0.02)):
    
        # plt.ioff()
        
        delta = dt.timedelta(hours = Dt)
        
        time = start_day + delta
        
        fig, ax = mappping(time)

        
                
        
            
        
        # fig = plot_epb_drift(time, term, Dt)
        
        name = time.strftime('%Y%m%d%H%M')
        
        plt.show()
       
        # fig.savefig(f'temp/{name}')
        
        # plt.clf()   
        # plt.close()

# delta = dt.timedelta(hours = 3)
# time = start_day + delta
# fig = plot_epb_drift(time, start_day, v0 = 100, x0 = -60)

# run(start_day)



x0 = -60
term = pb.terminator(x0, start, float_fmt = False) 
v0 = 100
Dt = 1

def update(start, Dt):
    delta = dt.timedelta(hours = Dt)
    
    return start + delta
    

count = 0
for i, Dt in enumerate(np.arange(0, 2, 0.1)):
      
    time = update(start, Dt)
    
    fig, ax = mappping(time)
    
    ilon = plot_terminator_line(time)
    
    epb_lon = displacement(x0, velocity(v0), Dt)
    # if (time >= term):
    if (epb_lon > ilon):
        count += 1 
        growth_phase(ax, epb_lon, count)
   
            
            
            


plt.show()