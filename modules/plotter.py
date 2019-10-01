"""
Filename:    plotter.py
Author:      Deanna Nash, dlnash@ucsb.edu
Description: Functions for plotting
"""

import numpy as np
import colorsys
from matplotlib.colors import LinearSegmentedColormap # Linear interpolation for color maps

def loadCPT(path):
    """A function that loads a .cpt file and converts it into a colormap for the colorbar.
    
    This code was adapted from the GEONETClass Tutorial written by Diego Souza, retrieved 18 July 2019. 
    https://geonetcast.wordpress.com/2017/06/02/geonetclass-manipulating-goes-16-data-with-python-part-v/
    
    Parameters
    ----------
    path : 
        Path to the .cpt file
        
    Returns
    -------
    cpt :
        A colormap that can be used for the cmap argument in matplotlib type plot.
    """
    
    try:
        f = open(path)
    except:
        print ("File ", path, "not found")
        return None
 
    lines = f.readlines()
 
    f.close()
 
    x = np.array([])
    r = np.array([])
    g = np.array([])
    b = np.array([])
 
    colorModel = 'RGB'
 
    for l in lines:
        ls = l.split()
        if l[0] == '#':
            if ls[-1] == 'HSV':
                colorModel = 'HSV'
                continue
            else:
                continue
        if ls[0] == 'B' or ls[0] == 'F' or ls[0] == 'N':
            pass
        else:
            x=np.append(x,float(ls[0]))
            r=np.append(r,float(ls[1]))
            g=np.append(g,float(ls[2]))
            b=np.append(b,float(ls[3]))
            xtemp = float(ls[4])
            rtemp = float(ls[5])
            gtemp = float(ls[6])
            btemp = float(ls[7])
 
        x=np.append(x,xtemp)
        r=np.append(r,rtemp)
        g=np.append(g,gtemp)
        b=np.append(b,btemp)
 
    if colorModel == 'HSV':
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
        r[i] = rr ; g[i] = gg ; b[i] = bb
 
    if colorModel == 'RGB':
        r = r/255.0
        g = g/255.0
        b = b/255.0
 
    xNorm = (x - x[0])/(x[-1] - x[0])
 
    red   = []
    blue  = []
    green = []
 
    for i in range(len(x)):
        red.append([xNorm[i],r[i],r[i]])
        green.append([xNorm[i],g[i],g[i]])
        blue.append([xNorm[i],b[i],b[i]])
 
    colorDict = {'red': red, 'green': green, 'blue': blue}
    # Makes a linear interpolation
    cpt = LinearSegmentedColormap('cpt', colorDict)
    
    return cpt


def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap