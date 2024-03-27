# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:19:49 2024

@author: Luiz
"""

import datetime as dt 
import numpy as np 
import base as b 


def plot_drift_velocities(ax, Dt, epb_dn, x0 = -60):
    for i, v0 in enumerate([50, 100, 200]):
                
        epb_lon = displacement(x0, velocity(v0), Dt)
    
        gg.plot_ellipse(ax[i], lon = epb_lon)
    
        ax[i].set(title =  f'$v_{{zonal}}$ = {v0} m/s')
