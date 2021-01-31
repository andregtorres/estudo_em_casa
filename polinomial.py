#André Torres
# 31.01.2021

import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import sys
from parabolas import arrowed_spines

plt.rcParams["mathtext.fontset"]="stix"
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

#y2.append((a0+(line[0]-a0)/Nframes*(i))*(x2[-1]+(x2[-1]-line[1])/Nframes*(i))**exp + y0+(y0-line[2])/Nframes*(i))

def getLims(x,y, x0, lines,exp, margin):
    xmins=[np.min(x)]
    xmaxs=[np.max(x)]
    ymins=[np.min(y)]
    ymaxs=[np.max(y)]
    for l in lines:
        xmins.append(np.min(x+l[1]))
        xmaxs.append(np.max(x+l[1]))
        x2=x+l[1]
        y2=l[0]*(x)**exp+l[2]
        ymins.append(np.min(y2))
        ymaxs.append(np.max(y2))
    return [(min(xmins)-margin[0],
            max(xmaxs)+margin[0]),
            (min(ymins)-margin[1],
             max(ymaxs)+margin[1])]
    '''
    return [(min(np.min(x),np.min(-x))-margin,
            max(np.max(x),np.max(-x))+margin),
            (min(np.min(y),np.min(y))-margin,
            max(np.max(y),np.max(y))+margin)]
    '''

def composeLabel(l, a, x0, y0, exp):
    lab=u"${}(x)=".format(l)
    if np.abs(a) < 1:
        lab= lab +u"{0:.1f}".format(a)
    elif a ==1:
        lab= lab
    else:
        lab= lab +u"{}".format(int(a))
    if x0==0:
        lab= lab +u"x^{}".format(exp)
    elif x0>0:
        lab= lab +u"(x-{})^{}".format(int(x0),exp)
    elif x0<0:
        lab= lab +u"(x+{})^{}".format(int(-x0),exp)
    if y0<0:
        lab= lab +u"-{}".format(int(-y0))
    if y0>0:
        lab= lab +u"+{}".format(int(y0))
    lab= lab +u"$"
    return lab

name="test"
bgcolor="#f4f4f4"
color1="#134872"
color2="#e04146"
colors=[color1,color2,"g","cyan"]

a0=1
x0=0
y0=0
x2=[]
y2=[]
bg=True
ticks=False
points=True
labels=True
arrow=False
label=None
letters=["f","g","h"]
funcs=["1", "2", "3"]
exp=1
markers=[]
lines=[]
if __name__=="__main__":
    if len(sys.argv)>1:
        name=sys.argv[1]
        a0=float(sys.argv[2])
        x0=float(sys.argv[3])
        y0=float(sys.argv[4])
    if len(sys.argv)>4:
        for j,i in enumerate(sys.argv[5:]):
            if i== "-t":
                ticks=True
            if i== "-b":
                bg=False
            if i== "-a":
                arrow=True
            if i== "-e":
                func=sys.argv[5+j+1]
                if func not in funcs:
                    print(func," not a valid function, use ", funcs)
                else:
                    exp=int(func)
            if i[:2]== "-p":
                markers_raw=sys.argv[5+j][2:].split(" ")
                for m in range(int(len(markers_raw)/4)):
                    markers.append((float(markers_raw[4*m]),float(markers_raw[4*m+1]),int(markers_raw[4*m+2]),markers_raw[4*m+3]))
            if i[:2]== "-f":
                newLine_raw=sys.argv[5+j][2:].split(" ")
                lines.append([float(param) for param in newLine_raw])

    print("A criar video em {}".format(name))
    Nframes=100
    Npoints=200

    xmax=4
    margin=(1,2**exp)

    x=np.linspace(-xmax+x0,xmax+x0,Npoints)
    y=a0*(x-x0)**exp + y0
    lims=getLims(x,y,x0,lines,exp,margin)
    if ticks:
        xpoints=np.arange(lims[0][0],lims[0][1])
        ypoints=np.arange(lims[1][0],lims[1][1])
    else:
        xpoints=[]
        ypoints=[]
        if x0 != 0:
            xpoints=[x0]
        if y0 != 0:
            ypoints=[y0]

    print("ticks: ", ticks)
    print("points: ", points)
    print("exp: ", exp)
    print("arrow: ", arrow)
    print("points: ", markers)
    print("lines: ", lines)
    xCoordsToShow=[]
    yCoordsToShow=[]
    xLabelsToShow=[]
    yLabelsToShow=[]
    #animation loop
    for i in range(Nframes+1):
        x2=[]
        y2=[]
        for line in lines:
            x2.append(np.array(x+(line[1]-x0)/Nframes*(i)))
            y2.append((a0+(line[0]-a0)/Nframes*(i))*(x)**exp + y0+(line[2]-y0)/Nframes*(i))

        #plot and limits
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

        #ticks
        ax.axes.get_xaxis().set_ticks(xpoints)
        ax.axes.get_yaxis().set_ticks(ypoints)

        #Axis
        arrowed_spines(fig, ax)
        plt.xlabel(r'$\mathit{x}$',size=30)
        plt.ylabel(r"$y$",rotation=0,size=30,)
        coordy=-lims[1][0]/(lims[1][1]-lims[1][0])
        coordx=-lims[0][0]/(lims[0][1]-lims[0][0])-0.05
        ax.xaxis.set_label_coords(1,coordy)
        ax.yaxis.set_label_coords(coordx,0.95)

        #arrow
        if arrow:
            if i>0:
                for nLine,line in enumerate(lines):
                    plt.plot([0,line[1]], [line[2]]*2,":k")
                    plt.plot([line[1]]*2, [0,line[2]],":k")
                    plt.arrow(x0, y0, line[1], line[2], color=colors[1+nLine], linewidth=3, head_width=0.5,length_includes_head=True)


        #labels
        legLabels=[ composeLabel(letters[0],a0,x0,y0,exp)]

        #points on function
        if markers != []:
            for m in markers:
                if i==Nframes:
                    plt.plot([0,m[0]], [m[1],m[1]],":k")
                    plt.plot([m[0],m[0]], [0,m[1]],":k")
                    plt.plot(m[0],m[1], "o", markersize=8, color=colors[m[2]])
                    if m[0] not in xCoordsToShow or m[1] not in yCoordsToShow:
                        xCoordsToShow.append(m[0])
                        yCoordsToShow.append(m[1])
                        labx, laby =m[3].split(",") #comma separates x,y
                        if labx == ".": # . indicates number, - nothing
                            xLabelsToShow.append(str(int(m[0])))
                            print(m[0], int(m[0]), str(int(m[0])))
                        elif labx == "-":
                            xLabelsToShow.append("")
                        else:
                            xLabelsToShow.append(labx)
                        if laby == ".": # . indicates number, - nothing
                            yLabelsToShow.append(str(int(m[1])))
                        elif laby == "-":
                            yLabelsToShow.append("")
                        else:
                            yLabelsToShow.append(laby)
            ax.axes.get_xaxis().set_ticks(xCoordsToShow)
            ax.axes.get_xaxis().set_ticklabels(xLabelsToShow)
            ax.axes.get_yaxis().set_ticks(yCoordsToShow)
            ax.axes.get_yaxis().set_ticklabels(yLabelsToShow)

        #plot first line
        plt.plot(x,y, linewidth=4, color=color1)
        if points:
            plt.plot(x[0],y[0], "o", markersize=8, color=color1)
            plt.plot(x[-1],y[-1], "o", markersize=8, color=color1)
        #plot other lines
        if i>0:
            for j in range(len(x2)):
                plt.plot(x2[j],y2[j], linewidth=4, color=colors[j+1])
                if points:
                    plt.plot(x2[j][0],y2[j][0], "o", markersize=8, color=colors[j+1])
                    plt.plot(x2[j][-1],y2[j][-1], "o", markersize=8, color=colors[j+1])
        #legend
        if i>0:
            for nLine,line in enumerate(lines):
                legLabels.append( composeLabel(letters[nLine+1], *line, exp))
        if labels:
            l=ax.legend(legLabels, fontsize=22, markerscale=0, frameon=False, facecolor=bgcolor, handlelength=0, handletextpad=0,labelspacing=0.1, loc='center right', bbox_to_anchor=(1.0,1.2))
            l.get_texts()[0].set_color(color1)
            l.legendHandles[0].set_visible=False
            try:
                for nLine,line in enumerate(lines):
                    l.get_texts()[1+nLine].set_color(colors[1+nLine])
                    l.legendHandles[1+nLine].set_visible=False
            except:
                pass
        plt.tight_layout()

        #save figures
        if i<Nframes+1:
            plt.savefig(name+"/frame_{0:04d}.png".format(i), facecolor=fig.get_facecolor())
        if i==0:
            plt.savefig(name+"/primeiroFrame.png", facecolor=fig.get_facecolor())
        if i==Nframes:
            plt.savefig(name+"/ultimoFrame.png", facecolor=fig.get_facecolor())
        plt.close()
        if (i+1)%int(Nframes/10)==0:
            print('.', end='', flush=True)
    print("\nDONE")
