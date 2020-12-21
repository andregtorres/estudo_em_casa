import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero


def arrowed_spines(fig, ax):
    #global fig, ax
    #https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom','right','top','left']:
        ax.spines[side].set_visible(False)

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # removing the axis ticks
    #plt.xticks([]) # labels
    #plt.yticks([])
    #ax.xaxis.set_ticks_position('none') # tick markers
    #ax.yaxis.set_ticks_position('none')

    # get width and height of axes object to compute
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw = 1./20.*(ymax-ymin)
    hl = 1./20.*(xmax-xmin)
    lw = 1. # axis line width
    ohg = 0.3 # arrow overhang

    # compute matching arrowhead length and width
    yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width
    yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

    # draw x and y axis
    ax.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw = lw,
             head_width=hw, head_length=hl, overhang = ohg,
             length_includes_head= True, clip_on = False)

    ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw = lw,
             head_width=yhw, head_length=yhl, overhang = ohg,
             length_includes_head= True, clip_on = False)

Nframes=100
Npoints=200
ox2=0.2
oy2=0.2
margin=0.1


x=np.arange(Npoints)/Npoints
y=np.sin(2*np.pi*x)
for i in range(Nframes):
    x2=x+ox2/Nframes*(i)
    y2=np.sin(2*np.pi*x)+oy2/Nframes*(i)
    plt.figure()
    plt.xlim(0-margin,1+ox2+margin)
    plt.ylim(-1-margin,1+oy2+margin)

    plt.plot(x,y)
    if i>0:
        plt.plot(x2,y2)
    fig = plt.gcf()
    ax = plt.gca()
    arrowed_spines(fig, ax)
    plt.savefig("sin_xy_1/sin_xy_{0:04d}.png".format(i))
    plt.close()
