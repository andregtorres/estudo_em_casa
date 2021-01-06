#André Torres
# 06.01.2021

import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import sys
from parabolas import arrowed_spines

plt.rcParams["mathtext.fontset"]="stix"
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)

def getLims(x,y,ox2,oy2, margin):
    #y2=(x-x0)**2+y0+oy2
    y2=np.sin(2*np.pi*x)+y0+oy2
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
    margin=1
    T=4

    xpoints=[ox2]
    ypoints=[oy2]

    x=np.linspace(-xmax,xmax,Npoints)
    y=a0*np.sin(2*np.pi*x/T)+y0
    lims=getLims(x,y,ox2,oy2,margin)

    for i in range(Nframes):
        x2=x+ox2/Nframes*(i)
        #y2=(a0+(a2-a0)/Nframes*(i))*(x-x0)**2+y0+oy2/Nframes*(i)
        y2=(a0+(a2-a0)/Nframes*(i))*np.sin(2*np.pi*(x-x0)/T)+y0+oy2/Nframes*(i)
        plt.figure(dpi=200)
        plt.xlim(lims[0])
        plt.ylim(lims[1])

        fig = plt.gcf()
        ax = plt.gca()
        if not ticks:
            ax.axes.get_xaxis().set_ticks(xpoints)
            ax.axes.get_yaxis().set_ticks(ypoints)
        arrowed_spines(fig, ax)
        if arrow:
            plt.plot([0,ox2], [oy2]*2,":k")
            plt.plot([ox2]*2, [0,oy2],":k")
        plt.xlabel(r'$\mathit{x}$',size=30)
        plt.ylabel(r"$y$",rotation=0,size=30)
        coordy=-lims[1][0]/(lims[1][1]-lims[1][0])
        coordx=-lims[0][0]/(lims[0][1]-lims[0][0])
        ax.xaxis.set_label_coords(1,coordy)
        ax.yaxis.set_label_coords(coordx,1)

        plt.plot(x,y, linewidth=4, color="#134872")
        if i>0:
            plt.plot(x2,y2, linewidth=4, color="#e04146")
            if arrow:
                plt.arrow(x0, y0, ox2, oy2, color="r", linewidth=3, head_width=0.2,length_includes_head=True)


        plt.savefig(name+"/frame_{0:04d}.png".format(i))
        if i==0:
            plt.savefig(name+"/primeiroFrame.png")
        if i==Nframes-1:
            plt.savefig(name+"/ultimoFrame.png")
        plt.close()
        if i+1%int(Nframes/10)==0:
            print('.', end='', flush=True)
    print("\nDONE")
