import pandas as pd 
import numpy as np
import core as c
import datetime as dt
import random 
import matplotlib.pyplot as plt 


def random_days(start_date, end_date, n):
    
    total_days = (end_date - start_date).days
    
    random_dates = []
    for _ in range(n):
        random_days = random.randint(0, total_days)
        
        random_date = start_date + dt.timedelta(days=random_days)
    
        random_dates.append(random_date)
        
    return random_dates

def adding_non_occurrences(df):
    dn = df.index[0]
    
    dates = pd.date_range(
        df.index[0], 
        df.index[-1], 
        freq = '1M'
        )
    
    dates = {
        1: 30,
        2: 25,
        3: 0,
        4: 25,
        5: 15,
        6: 30,
        7: 30,
        8: 20, 
        9: 0,
        10: 20,
        11: 25, 
        12: 30
        }
    
    for month, num in dates.items():
        
        
        start = dt.datetime(dn.year, month, 1)
        end = dt.datetime(dn.year, month, 28)
        
        for dn in random_days(start, end, num):
            
            df.loc[dn] = 0
    
    
    df.loc[(df.index.month >= 5) & 
           (df.index.month <= 7), 'epb'] = 0

        
    return df

def simulate_cases(year):
    
    dates = pd.date_range(
        f'{year}-01-01', f'{year}-12-31', freq = '1D')
    
    df = pd.DataFrame({'epb': np.ones(len(dates))}, index = dates)
    
    return adding_non_occurrences(df)



def replace_simul_by_obs():
    year = 2015
    epb = simulate_cases(year)
    
    
    df = c.load_results('jic')
    
    df = df.loc[df.index.year == year]
    
    df['epb'] = epb['epb'].copy()
    
    ds = c.probability_distribution(
         df, 
         parameter = 'gamma'
         )  
 
def plot(ds, epb):
    
    
    
    fig, ax = plt.subplots(nrows = 2)
    ds1 = c.count_occurences(epb).month
    
    ds1.plot(kind = 'bar', ax = ax[0])
    
    ax[1].plot(ds['start'], ds['rate'])
    
    # ds1 = c.count_occurences(df).month
    
    # ds1['epb'].plot(kind = 'bar')
    
    # df['gamma'].plot()
    
    plt.plot(ds['start'], ds['rate'])