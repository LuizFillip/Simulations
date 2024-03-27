import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs
import datetime as dt 
import numpy as np 
import base as b 

b.config_labels()


def velocity(v):
    return v * 3.6
def displacement(x0, v0, dt):
    return (x0 + v0 * dt / 111)  



def mappping(year):
    fig, ax = plt.subplots(
        dpi = 300,
        ncols = 1,
        figsize = (10,10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    # for i in range(3):
    gg.map_attrs(ax, year)
    gg.plot_rectangles_regions(ax, year, delta1 = 3)
    
    
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

def plot_ellipse(ax, year = 2014, lon = -60):
    
   
    eq_lon, eq_lat  = gg.load_equator(
        year, values = True)
    
    i = b.find_closest(eq_lon, lon)
    
    x, y = ellipse((eq_lon[i], eq_lat[i]))
    
    ax.plot(x, y)
   
    ax.fill(x, y, color = 'gray', alpha = 0.5)
    
def plot_terminator_line(ax, dn):
    
    lon, lat = gg.terminator2(dn, 18)
    ax.scatter(lon, lat, c = 'k', s = 5)
    
    eq_lon, eq_lat = gg.load_equator(year, values = True)


    ilon, ilat = gg.intersection(eq_lon, eq_lat, lon, lat)
    
    ax.scatter(ilon, ilat, marker = 'o', s = 100)


    if len(ilon) > 1 and len(ilat)>1:
        ilon = ilon[0]
        ilat = ilat[0]
        
    return ilon, ilat


import PlasmaBubbles as pb 


def plot_epb_drift(time, term, Dt, v0 = 100, x0 = -60):
    
    fig, ax = mappping(start_day.year)

    ax.set(title = time.strftime("%H:%M:%S (UT)"))

    ilon, ilat = plot_terminator_line(ax, time)

    epb_lon = displacement(x0, velocity(v0), Dt)

    if (time >= term) and (epb_lon > ilon):

        plot_ellipse(ax, lon = epb_lon)
            
    return fig

from tqdm import tqdm 

Dt = 2

year = 2013
start_day = dt.datetime(year, 1, 1, 21)

b.make_dir('temp')

def run(start_day, v0 = 100, x0 = -60):
    
    term = pb.terminator(x0, start_day, float_fmt = False) 
    
    for Dt in tqdm(np.arange(0, 7, 0.02), 'save frames'):
    
        plt.ioff()
        
        delta = dt.timedelta(hours = Dt)
        
        time = start_day + delta
       
        fig = plot_epb_drift(time, term, Dt)
        
        name = time.strftime('%Y%m%d%H%M')
       
        fig.savefig(f'temp/{name}')
            
        plt.clf()   
        plt.close()

# delta = dt.timedelta(hours = 3)
# time = start_day + delta
# fig = plot_epb_drift(time, start_day, v0 = 100, x0 = -60)

# plt.show()
v0 = 100
x0 = -60
run(start_day)