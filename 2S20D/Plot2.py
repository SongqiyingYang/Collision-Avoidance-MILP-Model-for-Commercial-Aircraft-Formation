from mpl_toolkits import mplot3d 
import matplotlib 
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import math

import pandas as pd
import numpy as np

T = 110 #total time in seconds 
delT = 0.8 #seconds per iteration 
N = round(T/delT) #iterations = N 
S = 2 #sides of each dimension 

jetwashTrack = 1

plotStop = N

A = 2 # number of formation aircraft
D = 3 # dimensions (2 = 2-D, 3 = 3-D) 
NI = 1 # number of non-cooperative intruders 

wingspan = 0.267
offset = np.zeros(A) 
sideCount = 0 
for ac in range(A): # setting aircraft spacing required from courseline for each side 
        offset[ac] = sideCount 
        if (ac % 2) == 0: 
            sideCount +=1

finalCourseWidth = np.zeros((D, A, S), dtype=float) #aircraft need to be on final altitude of z=0 
for ac in range(A): 
    if ac == 0: 
        finalCourseWidth[1, ac, 0] = 0 
        finalCourseWidth[1, ac, 1] = 0 
    else: 
        finalCourseWidth[1, ac, 0] = (0.8*wingspan)*offset[ac] #right side final course requirements for formation 
        finalCourseWidth[1, ac, 1] = (0.8*wingspan)*offset[ac] #left side final course requirements for formation 
    if D > 2: 
        finalCourseWidth[2, ac, 0] = 0.0 #bottom side final course requirements for formation 
        finalCourseWidth[2, ac, 1] = 0.0 #top side final course requirements for formation 

wind = np.zeros(D) 
wind[0:2] = [0.000,0.000] # wind in 1k ft/sec: wind direction from [x direction E+/ W-, y direction N+ / S-] 
if D > 2: 
    wind[2] = 0.000 # vertical wind from top (+) from bottom (-) 
windi = wind*delT # wind

#jetwash input 
jw = np.zeros(D) 
jw[1] = 0.7*wingspan 
if D > 2: 
    jw[2] = 0.7*wingspan
js = 0.005 # sink rate of jetwash and vortices in 1k*ft/s (300ft/min sink rate or btw 5-7 ft/sec) 
jsi = js*delT # 

wns = np.zeros(D) # wind (horizontal x and y) and sink rate (z) for jetwash 
wns = windi # wind per iteration input from top of code 
if D > 2: 
    wns[2] += jsi # sink rate input above

            

stringT = str(int(T)) 
            
Ps = round(plotStop) 
pTime = 0.01 #time delay between plotting points on all plots 
#plot widths 
xlim = 1 #feet*1k 
ylim = 1 #feet*1k 
zlim = 1 #feet*1k 

# plot colors 

ppc = {0:'b', 1:'cornflowerblue', 2:'deepskyblue', 3:'skyblue', 4:'green', 5:'limegreen', 6:'turquoise', 7:'aquamarine'} 
pc = {key: ppc[key] for key in range(A)} 
ppcNI = {3:'coral', 2:'tomato', 1:'orangered', 0:'red'} 
pcNI = {key: ppcNI[key] for key in range(NI)} 
    
    
N5 = round(5/delT) 
NN5 = (N/N5) 
if NN5 >= 10: 
    N5 = N5*2 
iN5 = 0 
jN5 = 0 


timeColor = {0:'black', 1:'dimgrey', 2:'darkgray', 3:'darkgoldenrod', 4:'hotpink', 5:'lightcoral', 6:'indianred', 7:'tomato', 8:'navajowhite', 9:'orange'} 
time = {key: timeColor[key] for key in range(10)} 


#load information
xMatrix0 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix0.csv", index_col=0).values
xMatrix1 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix1.csv", index_col=0).values

if D > 2:
    xMatrix2 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix2.csv", index_col=0).values

vMatrix0 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix0.csv", index_col=0).values
vMatrix1 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix1.csv", index_col=0).values

if D > 2:
    vMatrix2 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix2.csv", index_col=0).values


if D > 2:
    x = np.array([xMatrix0, xMatrix1, xMatrix2])
    v = np.array([vMatrix0, vMatrix1, vMatrix2])
else:
    x = np.array([xMatrix0, xMatrix1])
    v = np.array([vMatrix0, vMatrix1])

#print(xMatrix0)


# non-intruder
intruder_degree = 0
intruder_radians = math.radians(intruder_degree)
nix = np.zeros((D, N, NI))
niy = np.zeros((D,NI))
niy[0,0] = -1*math.cos(intruder_radians)
niy[1,0] = -1*math.sin(intruder_radians)
if D>2:
    niy[2,0] = 0.0

for iter in range(N):
    nix[0,iter,0] = 20*(1+math.cos(intruder_radians)) + iter*delT*niy[0,0]  #need to be futher design
    nix[1,iter,0] = 20*(math.sin(intruder_radians)) + iter*delT*niy[1,0]
    if D>2:
        nix[2,iter,0] = 0.0 + iter*delT*niy[2,0]


#Plotting
if D > 2: # 3D plot 
    
    fig, ax3 = plt.subplots(figsize=(16, 4)) 
    
    #plot limits 
    # find maximum values in the model solution in each dimension 
    xmax = 0
    xmin = 0 
    ymax = 0 
    ymin = 0 
    zmax = 0 
    zmin = 0 
    for i in range(N): 
        for ac in range(A): 
            for d in range(D): 
                if d == 0 and x[0, i, ac] > xmax: 
                    xmax = x[0, i, ac] 
                if d == 0 and x[0, i, ac]< xmin: 
                    xmin = x[0, i, ac] 
                if d == 1 and x[1, i , ac]> ymax: 
                    ymax = x[1, i, ac] 
                if d == 1 and x[1, i , ac] < ymin: 
                    ymin = x[1, i, ac] 
                if d == 2 and x[2, i, ac] > zmax: 
                    zmax = x[2, i, ac] 
                if d == 2 and x[2, i, ac] < zmin: 
                    zmin = x[2, i, ac]
                if xmin <10 and xmin > 0: 
                    xmin = -1 
                if xmin < 0 and xmin > -10: 
                    xmin = -10 
                if ymax < 0.5 and ymin > -0.5: 
                    ymax = 0.5
    for i in range(N): 
            for ni in range(NI): 
                for d in range(D):
                    if d == 0 and nix[0, i, ni] > xmax: 
                        xmax = nix[0, i, ni] 
                    if d == 0 and nix[0, i, ni]< xmin: 
                        xmin = nix[0, i, ni] 
                    if d == 1 and nix[1, i , ni]> ymax: 
                        ymax = nix[1, i, ni] 
                    if d == 1 and nix[1, i , ni] < ymin: 
                        ymin = nix[1, i, ni] 
                    if d == 2 and nix[2, i, ni] > zmax: 
                        zmax = nix[2, i, ni] 
                    if d == 2 and nix[2, i, ni] < zmin: 
                        zmin = nix[2, i, ni]
                    if xmin <10 and xmin > 0: 
                        xmin = -1 
                    if xmin < 0 and xmin > -10: 
                        xmin = -10 
                    if ymax < 0.5 and ymin > -0.5: 
                        ymax = 0.5


    # set plot limits to cover maximum and minimum values in each dimension 
    # 2-D view from side (x vs z) 
    if A > 1: 
        ax3.axhspan(-finalCourseWidth[2,1,0], finalCourseWidth[2,1,1], facecolor='0.9') 
    if xmax >= xmin: 
        ax3.set_xlim(0,1.2*xmax) 
    else: 
        ax3.set_xlim(0,1.2*xmax) 
    if zmax == -zmin: 
        ax3.set_ylim(-0.1, 0.1) 
    elif zmax >= -zmin: 
        ax3.set_ylim(-1.2*zmax,1.2*zmax) 
    else: 
        ax3.set_ylim(1.2*zmin,-1.2*zmin) 
    if zmax < 0.1 and zmin > -0.1: 
        ax3.set_ylim(-0.1, 0.1) 
    if A > 1 and finalCourseWidth[2,1,1] != 0:
        secax3 = ax3.secondary_yaxis('right') 
        secax3.set_ylabel('Final altitude constraint', alpha = 0.6) 
        secax3.set_yticks([])


    # plot labels 
    ax3.set_aspect('equal', adjustable='box')
    ax3.set_title("View from the side") 
    ax3.set_xlabel('Along-course position (x1000ft)') 
    ax3.set_ylabel('Altitude (x1000ft)') 
    ax3.grid() 
    
    
    # 3-D vertplot code 
    for i in range(Ps-1): 
        ef = 0 
        cp = 0 
        
        # 2-D view from side (x vs z) 
        for ac in range(A): 
            if i == (Ps-2): 
                ax3.plot([x[0,i,ac], x[0,i+1,ac]], [x[2,i,ac], x[2,i+1,ac]], pc[ac], marker='>') 
            elif iN5 == N5: 
                verts = [[v[0,i,ac], v[2,i,ac]*10], [-v[0,i,ac], 0], [0, -v[2,i,ac]*10], [v[0,i,ac], v[2,i,ac]*10]] 
                ax3.plot([x[0,i,ac], x[0,i+1,ac]], [x[2,i,ac], x[2,i+1,ac]], pc[ac], marker=verts) 
                ax3.plot(x[0,i,ac], [x[2,i,ac]], time[jN5], marker='H') 
            else:
                verts = [[v[0,i,ac], v[2,i,ac]*10], [-v[0,i,ac], 0], [0, -v[2,i,ac]*10], [v[0,i,ac], v[2,i,ac]*10]] 
                ax3.plot([x[0,i,ac], x[0,i+1,ac]], [x[2,i,ac], x[2,i+1,ac]], pc[ac], marker=verts)
        for ni in range(NI):
            if i == (Ps-2): 
                ax3.plot([nix[0,i,ni], nix[0,i+1,ni]], [nix[2,i,ni], nix[2,i+1,ni]], pcNI[ni], marker='<') 
            elif iN5 == N5: 
                verts = [[niy[0,ni], niy[2,ni]*10], [-niy[0,ni], 0], [0, -niy[2,ni]*10], [niy[0,ni], niy[2,ni]*10]] 
                ax3.plot([nix[0,i,ni], nix[0,i+1,ni]], [nix[2,i,ni], nix[2,i+1,ni]], pcNI[ni], marker=verts) 
                ax3.plot(nix[0,i,ni], [nix[2,i,ni]], time[jN5], marker='H')          
            else: 
                verts = [[niy[0,ni], niy[2,ni]*10], [-niy[0,ni], 0], [0, -niy[2,ni]*10], [niy[0,ni], niy[2,ni]*10]] 
                ax3.plot([nix[0,i,ni], nix[0,i+1,ni]], [nix[2,i,ni], nix[2,i+1,ni]], pcNI[ni], marker=verts)
        
        if iN5 == N5: 
            iN5 = 0 
            jN5 += 1 
            if jN5 == 10: 
                jN5 = 0 
        else: 
            iN5 += 1 
                
            plt.draw() 
        plt.draw() 
        plt.pause(pTime)
    
    plt.show()

else: 
    # figure and axes definition in the graph
    fig, ax = plt.subplots() 
    
    # axes parameterization 
    xmax = 0 
    xmin = 0 
    ymax = 0 
    ymin = 0 
    zmax = 0 
    zmin = 0 
    for i in range(N): 
        for ac in range(A+NI): 
            for d in range(D): 
                if d == 0 and x[0, i, ac].Xn > xmax: 
                    xmax = x[0, i, ac].Xn 
                if d == 0 and x[0, i, ac].Xn < xmin: 
                    xmin = x[0, i, ac].Xn 
                if d == 1 and x[1, i , ac].Xn > ymax: 
                    ymax = x[1, i, ac].Xn 
                if d == 1 and x[1, i , ac].Xn < ymin: 
                    ymin = x[1, i, ac].Xn 
                if d == 2 and x[2, i, ac].Xn > zmax: 
                    zmax = x[2, i, ac].Xn 
                if d == 2 and x[2, i, ac].Xn < zmin:
                    zmin = x[2, i, ac].Xn
    if xmax >= xmin: 
        ax.set_xlim(xmin,1.2*xmax) 
    else: 
        ax.set_xlim(1.2*xmin,1.2*xmax) 
    if ymax >= -ymin: 
        ax.set_ylim(-1.2*ymax,1.2*ymax)
    else: 
        ax.set_ylim(1.2*ymin,-1.2*ymin) 
        
    plt.title("Formation from above") 
    plt.xlabel("X position (x1000ft)") 
    plt.ylabel("Y position (x1000ft)") 
    
    
    tr = plt.annotate('Sec',(1.21*xmax, ymax), textcoords="offset points", xytext=(0,8), ha='center') 
    
    mng = plt.get_current_fig_manager() 
    mng.window.state("zoomed") 
    
    for i in range(Ps-1): 
        for ac in range(A+NI): 
            if ac < (A-I): 
                verts = [[v[0,i,ac].Xn, v[1,i,ac].Xn*10], [-v[0,i,ac].Xn, 0], [0, -v[1,i,ac].Xn*10], [v[0,i,ac].Xn, v[1,i,ac].Xn*10]] 
                if i == 0 and ac == 0: 
                    plt.plot([x[0,i,ac].Xn, x[0,i+1,ac].Xn], [x[1,i,ac].Xn, x[1,i+1,ac].Xn], pc[ac], label='formation', marker=verts) 
                else:
                    plt.plot([x[0,i,ac].Xn, x[0,i+1,ac].Xn], [x[1,i,ac].Xn, x[1,i+1,ac].Xn], pc[ac], marker=verts)
            if ac >= (A-I): 
                verts = [[v[0,i,ac].Xn, v[1,i,ac].Xn*10], [-v[0,i,ac].Xn, 0], [0, -v[1,i,ac].Xn*10], [v[0,i,ac].Xn, v[1,i,ac].Xn*10]] 
                if i ==0 and ac == A-I: 
                    plt.plot([x[0,i,ac].Xn, x[0,i+1,ac].Xn], [x[1,i,ac].Xn, x[1,i+1,ac].Xn], pcI[(ac-A-NI+1)], label='intruder', marker=verts) 
                else: 
                    plt.plot([x[0,i,ac].Xn, x[0,i+1,ac].Xn], [x[1,i,ac].Xn, x[1,i+1,ac].Xn], pcI[(ac-A-NI+1)], marker=verts)
        
        tr = plt.annotate(i/10,(1.21*xmax-1, ymax), textcoords="offset points", xytext=(0,-12), ha='center') 
        plt.draw() 
        plt.pause(pTime*10) 
        
        tr.remove() 
        ax.legend() 
    tr = plt.annotate(i/10,(1.21*xmax-1, ymax), textcoords="offset points", xytext=(0,-12), ha='center') 
    
    
    plt.show()