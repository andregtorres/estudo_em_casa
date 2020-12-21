#André Torres
# 21.12.2020

import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import sys

plt.rcParams["mathtext.fontset"]="stix"
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)

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

def getLims(x,y,ox2,oy2, margin):
    y2=(x-x0)**2+y0+oy2
    return [(min(np.min(x),np.min(x+ox2))-margin,max(np.max(x),np.max(x+ox2))+margin),(min(np.min(y),np.min(y2))-margin,   max(np.max(y),np.max(y2))+margin)]

name="test"
a0=1
x0=0
y0=0
a2=1
ox2=1
oy2=2
ticks=False
arrow=False
if __name__=="__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]
        a2=float(sys.argv[2])
        ox2=float(sys.argv[3])
        oy2=float(sys.argv[4])
    if len(sys.argv)>4:
        for i in sys.argv[5:]:
            if i== "-t":
                ticks=True
            if i== "-a":
                arrow=True

    print("A criar video em {}".format(name))
    Nframes=100
    Npoints=200

    xmax=4
    margin=0.5

    xpoints=[ox2]
    ypoints=[oy2]

    x=np.linspace(-xmax,xmax,Npoints)
    y=a0*(x-x0)**2+y0
    lims=getLims(x,y,ox2,oy2,margin)

    for i in range(Nframes):
        x2=x+ox2/Nframes*(i)
        y2=(a0+(a2-a0)/Nframes*(i))*(x-x0)**2+y0+oy2/Nframes*(i)
        plt.figure(dpi=200)
        plt.xlim(lims[0])
        plt.ylim(lims[1])
        plt.plot(x,y)
        if i>0:
            plt.plot(x2,y2)
        if arrow:
            plt.arrow(x0, y0, ox2, oy2, color="k", head_width=0.3,length_includes_head=True)
            plt.plot([0,ox2], [oy2]*2,":k")
            plt.plot([ox2]*2, [0,oy2],":k")
        fig = plt.gcf()
        ax = plt.gca()
        if not ticks:
            ax.axes.get_xaxis().set_ticks(xpoints)
            ax.axes.get_yaxis().set_ticks(ypoints)
        arrowed_spines(fig, ax)
        plt.xlabel(r'$\mathit{x}$',size=20)
        plt.ylabel(r"$y$",rotation=0,size=20)
        ax.xaxis.set_label_coords(1,0)
        ax.yaxis.set_label_coords(0.5,1)
        plt.savefig(name+"/frame_{0:04d}.png".format(i))
        if i==0:
            plt.savefig(name+"/primeiroFrame.png")
        if i==Nframes-1:
            plt.savefig(name+"/ultimoFrame.png")
        plt.close()
        if i+1%int(Nframes/10)==0:
            print('.', end='', flush=True)
    print("\nDONE")
