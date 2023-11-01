import matplotlib.pyplot as plt
import numpy as np

def plot_function(f,tmin,tmax,xlabel=None,ylabel=None,axes=False, **kwargs):
    ts = np.linspace(tmin,tmax,1000)
    if xlabel:
        plt.xlabel(xlabel,fontsize=18)
    if ylabel:
        plt.ylabel(ylabel,fontsize=18)
    plt.plot(ts, [f(t) for t in ts], **kwargs)
    if axes:
        total_t = tmax-tmin
        plt.plot([tmin-total_t/10,tmax+total_t/10],[0,0],c='k',linewidth=1)
        plt.xlim(tmin-total_t/10,tmax+total_t/10)
        xmin, xmax = plt.ylim()
        plt.plot([0,0],[xmin,xmax],c='k',linewidth=1)
        plt.ylim(xmin,xmax)