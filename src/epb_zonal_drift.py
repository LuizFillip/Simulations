


def velocity(v):
    return v * 3.6
def displacement(x0, v0, dt):
    return x0 + v0 * dt / 111


        
def plot_simulate_bubble_drift(year, Dt):
    
    fig, ax = mappping(year)
    
    delta = dt.timedelta(hours = Dt)
    
    epb_dn = dt.datetime(year, 1, 1, 0) + delta
     
    plot_drift_velocities(ax, Dt, epb_dn)
    
    fig.suptitle(epb_dn.strftime("%H:%M:%S (UT)"), y = 0.7)
    
    return fig, epb_dn

year = 2014

twilight = 18


# df = b.load(
#     pb.epb_path(
#         year, path = 'events3'
#         )
#     )

# ds = b.sel_times(df, dn, hours = 12)


for Dt in np.arange(0, 2, 0.02):

    plt.ioff()
    
    # fig, epb_dn = plot_simulate_bubble_drift(year, Dt)
    
    fig, ax = mappping(year)
    
    delta = dt.timedelta(hours = Dt)
    
    epb_dn = dt.datetime(year, 1, 1, 0) + delta
     
    plot_drift_velocities(ax, Dt, epb_dn)
    
    fig.suptitle(epb_dn.strftime("%H:%M:%S (UT)"), y = 0.7)
    
    name = epb_dn.strftime('%Y%m%d%H%M')
    print(name)
    fig.savefig(f'temp/{name}')
        
    plt.clf()   
    plt.close()