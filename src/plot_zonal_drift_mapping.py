import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs

def velocity(v):
    return v * 3.6
def displacement(x0, v0, dt):
    return x0 + v0 * dt / 111


def plot_drift_velocities(ax, Dt, epb_dn, x0 = -60):
    for i, v0 in enumerate([50, 100, 200]):
        
        #plot_terminator_and_equator(ax[i], epb_dn)
        
        epb_lon = displacement(x0, velocity(v0), Dt)
    
        gg.plot_ellipse(ax[i], lon = epb_lon)
    
        ax[i].set(title =  f'$v_{{zonal}}$ = {v0} m/s')

def mappping(year):
    fig, ax = plt.subplots(
        dpi=300,
        ncols = 1,
        figsize=(12, 12),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    # for i in range(3):
    gg.map_attrs(ax, year)
    gg.plot_rectangles_regions(ax, year)
    
    
    return fig, ax
import datetime as dt 
import numpy as np 
import base as b 



    
    
def ellipse(
        center, 
        angle = 95, 
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
    
    
year = 2013
v0 = 100
x0 = -60
Dt = 0
fig, ax = mappping(year)

dn = dt.datetime(year, 1, 1, 22)

lon, lat = gg.terminator2(dn, 18)
ax.scatter(lon, lat, c = 'k', s = 5)


epb_lon = displacement(x0, velocity(v0), Dt)

plot_ellipse(ax, lon = epb_lon)