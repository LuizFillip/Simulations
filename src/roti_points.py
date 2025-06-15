import PlasmaBubbles as pb 
import numpy as np 
import pandas as pd 
import datetime as dt 




class prns:
    """Creating a prn list for each constellation"""
    
    def __init__(self):
        pass
    @staticmethod
    def format_prn(constelation, num):
        if num < 10:
            prn = f"{constelation}0{num}"
        else:
            prn = f"{constelation}{num}"
        return prn
    
    @staticmethod
    def prn_list(constelation = "G", number = 32):
        call = prns()
        return [call.format_prn(constelation, num) 
                for num in range(1, number + 1)]
    
    @property
    def gps_and_glonass(self):
        return (prns().prn_list("G", 32) +
                prns().prn_list("R", 24))
        



def adapt_circle_to_range(x_range, y_range, num_points=100):

    x_min, x_max = x_range
    y_min, y_max = y_range
    
    center_x = (x_max + x_min) / 2
    center_y = (y_max + y_min) / 2
    radius_x = (x_max - x_min) / 2
    radius_y = (y_max - y_min) / 2

    angles = np.linspace(0, 2 * np.pi, num_points)
    x = center_x + radius_x * np.cos(angles)
    y = center_y + radius_y * np.sin(angles)
    
    return x, y



def point_on_frame(start, lons, lats):
        
    x_range = (lons, -70)
    y_range = (lats, -20)
    
    
    end = start + dt.timedelta(hours = 3)
    index = pd.date_range(start, end, freq = '1min')
    lon, lat = adapt_circle_to_range(
        x_range, y_range, num_points=len(index))
    points = np.random.uniform(0, 0.1, len(index))
    data = {'roti': points, 'lon': lon, 'lat': lat}
    return pd.DataFrame(data, index = index)


def simulate_roti_points(
        df, 
        lons = -80, 
        lats = -2): 

    
    times = pd.date_range(
        df.index[0], df.index[-1], periods=10)
    out = []
    for i, start in enumerate(times, start = 1):
        
        
        
        for prn in prns().prn_list():
            lon_start = lons + np.random.randint(10)
            lat_start = lats - np.random.randint(10)
            ds = point_on_frame(start, lon_start, lat_start)
        
            ds['prn'] =  prn 
            ds['sts'] = 'fake'
            out.append(ds)
           
    ds = pd.concat(out)
    return ds.loc[ds.index < df.index[-1]]
  
