import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import PlasmaBubbles as pb 
import datetime as dt
import base as b 
import GEO as gg 


def sunset_like(
        df, 
        dn, 
        duration = 5
        ):
    
    '''
    Occurrences by terminator
    '''
        
    for offset, lon in enumerate(df.columns):
        
        delta = dt.timedelta(hours = duration)
        
        term = pb.terminator(int(lon), dn, float_fmt = False)
        
        df[lon].loc[
            (df.index < term) | 
            (df.index > term + delta)
            ] = 0
    
    return df



def set_data(dn, hours = 13):
    
    delta = dt.timedelta(hours = hours)
    times = pd.date_range(
        dn, dn + delta, 
        freq = '1min'
        )
    
    arr = np.ones((len(times),  4))
    columns = np.arange(-80, -40, 10)
    
    df = pd.DataFrame(arr, columns = columns, index = times)
    
    
    # df = sunset_like(df, dn)
    
    
    return df


def sunset_occurence():
    
    return

def non_occurrence(df, col = -80):
    df[col] = 0
    return df
     
# df = set_data(dn)

# df = zeros_from_terminator(df, dn, col_start=col)
    

def last_occurrence(df, col):
    return df[df[col] == 1].index.max() 


def add_zeros(
        df, 
        delta_hours = 3, 
        dn = None, 
        lon_start = -60, 
        duration = 4
        ):
    
    if dn is None:
        dn = df.index[0]
    
    delta = dt.timedelta(hours = duration)
    
    dt_start = dn + dt.timedelta(hours = delta_hours)
    
    df[lon_start].loc[
         (df.index < dt_start) | 
         (df.index > dt_start + delta)
         ] = 0
    
    return df


dn = dt.datetime(2013, 12, 24, 20)

df = set_data(dn, hours = 10)

df[[-80, -70]] = np.nan

df = df.dropna(axis = 1)

fig, ax = plt.subplots(
    figsize = (10, 6),
    nrows = 2,
    sharex = True, 
    sharey = True,
    dpi = 300
    )

plt.subplots_adjust(hspace = 0.1)
start_hours = 2
df = add_zeros(df, dn = None, delta_hours = start_hours+ 1, lon_start = -60)

df = add_zeros(df, dn = None, delta_hours = start_hours , lon_start = -50)

y = 1.2

longs = [-50, -60]

for i, ax in enumerate(ax.flat):
    
    col = longs[i]
    
    ax.plot(df[col], lw = 2)
    
    dusk = pb.terminator(col, dn, float_fmt = False)
    
    ax.axvline(dusk, lw = 2)
    
    midnight = gg.local_midnight(dn, col + 5, delta_day = 1)
    
    ax.axvline(
        midnight, 
        lw = 2,
        color = 'b',
        )
    
    ax.set(ylim = [-0.1, 1.1], 
           yticks =[0, 1])
    
    ax.text(0.1, 0.8, col, transform = ax.transAxes)
    
    if i == 0:
        ax.text(dusk, y, 'Terminator', 
                    transform = ax.transData)
            
        ax.text(midnight, y, 'midnight', 
                color = 'b',
                transform = ax.transData)
    else:
        
        b.format_time_axes(ax)


plt.show()