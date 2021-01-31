#André Torres
# 24.01.2021

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

def getLims(x,y,x0,y0, margin, refy):
    if refy:
        return [(min(np.min(x),np.min(-x))-margin,
                max(np.max(x),np.max(-x))+margin),
                (min(np.min(y),np.min(y))-margin,
                max(np.max(y),np.max(y))+margin)]
    else:
        return [(np.min(x)-margin,np.max(x)+margin),
                (min(np.min(y),np.min(-y))-margin,
                max(np.max(y),np.max(-y))+margin)]


name="test"
bgcolor="#f4f4f4"
color1="#134872"
color2="#e04146"
a0=1
x0=0
y0=0
a2=1
ox2=1
oy2=2
bg=False
ticks=False
arrow=False
points=True
refy=True
labels=True
funcs=["1", "2", "3"]
exp=1
markers=[]
if __name__=="__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]
        a2=float(sys.argv[2])
        x0=float(sys.argv[3])
        y0=float(sys.argv[4])
    if len(sys.argv)>4:
        for j,i in enumerate(sys.argv[5:]):
            if i== "-t":
                ticks=True
            if i== "-a":
                arrow=True
            if i== "-b":
                bg=True
            if i=="-x":
                refy=False
            if i=="-y":
                refy=True
            if i== "-e":
                func=sys.argv[5+j+1]
                if func not in funcs:
                    print(func," not a valid function, use ", funcs)
                else:
                    exp=int(func)
            if i[:2]== "-p":
                print(sys.argv[5+j:])
                markers_raw=sys.argv[5+j][2:].split(" ")
                print(markers_raw)
                for m in range(int(len(markers_raw)/2)):
                    markers.append((float(markers_raw[2*m]),float(markers_raw[2*m+1])))
                print(markers)

    print("A criar video em {}".format(name))
    Nframes=100
    Npoints=200

    xmax=4
    margin=exp

    x=np.linspace(-xmax+x0,xmax+x0,Npoints)
    y=a0*(x-x0)**exp + y0
    lims=getLims(x,y,x0,y0,margin, refy)

    if ticks:
        xpoints=np.arange(lims[0][0],lims[0][1])
        ypoints=np.arange(lims[1][0],lims[1][1])
    else:
        xpoints=[]
        ypoints=[]
        if x0 != 0:
            xpoints=[x0]
            if refy:
                xpoints.append(-x0)
        if y0 != 0:
            ypoints=[y0]
            if not refy:
                ypoints.append(-y0)

    print("arrow: ", arrow)
    print("ticks: ", ticks)
    print("points: ", points)
    print("exp: ", exp)
    for i in range(Nframes):
        if refy:
            xp=(xmax+x0)*np.cos(np.pi/Nframes*i)
            xn=(-xmax+x0)*np.cos(np.pi/Nframes*i)
            x2=np.linspace(xn,xp,Npoints)
            y2=a0*(x-x0)**exp + y0
        else:
            x2=x
            y2=y*np.cos(np.pi/Nframes*i)

        fig=plt.figure(dpi=200)
        plt.xlim(lims[0])
        plt.ylim(lims[1])

        #fig = plt.gcf()
        ax = plt.gca()
        #background
        if bg:
            fig.patch.set_facecolor(bgcolor)
            ax.set_facecolor(bgcolor)
            #fig.patch.set_alpha(0)
            #ax.patch.set_alpha(0)
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
        legLabels=[ u"$f$"]
        if markers != []:
            for m in markers:
                plt.plot([0,m[0]], [m[1],m[1]],":k")
                plt.plot([m[0],m[0]], [0,m[1]],":k")
                plt.plot(m[0],m[1], "o", markersize=8, color=color1)
            ax.axes.get_xaxis().set_ticks(np.array(markers).T[0].tolist())
            ax.axes.get_yaxis().set_ticks(np.array(markers).T[1].tolist())
        plt.plot(x,y, linewidth=4, color=color1)
        if points:
            plt.plot(x[0],y[0], "o", markersize=8, color=color1)
            plt.plot(x[-1],y[-1], "o", markersize=8, color=color1)

        if i>0:
            plt.plot(x2,y2, linewidth=4, color=color2)
            plt.plot(x2[0],y2[0], "o", markersize=8, color=color2)
            plt.plot(x2[-1],y2[-1], "o", markersize=8, color=color2)
            if arrow:
                plt.arrow(x0, y0, ox2, oy2, color="r", linewidth=3, head_width=0.2,length_includes_head=True)
            legLabels=[ u"$f$", u"$g$"]
        if labels:
            l=ax.legend(legLabels, fontsize=22, markerscale=0, frameon=False, facecolor=bgcolor, handlelength=0, handletextpad=0,labelspacing=0.1, loc='center left', bbox_to_anchor=(1.0,1.0))
            l.get_texts()[0].set_color(color1)
            l.legendHandles[0].set_visible=False
            try:
                l.get_texts()[1].set_color(color2)
                l.legendHandles[1].set_visible=False
            except:
                pass
        #plt.grid()
        plt.savefig(name+"/frame_{0:04d}.png".format(i), facecolor=fig.get_facecolor())
        if i==0:
            plt.savefig(name+"/primeiroFrame.png", facecolor=fig.get_facecolor())
        if i==Nframes-1:
            plt.savefig(name+"/ultimoFrame.png", facecolor=fig.get_facecolor())
        plt.close()
        if i+1%int(Nframes/10)==0:
            print('.', end='', flush=True)
    print("\nDONE")
