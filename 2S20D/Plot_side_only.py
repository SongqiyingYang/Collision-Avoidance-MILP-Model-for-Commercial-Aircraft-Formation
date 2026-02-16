import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import math

import pandas as pd
import numpy as np

T = 110  # total time in seconds

delT = 0.8  # seconds per iteration
N = round(T / delT)  # iterations = N
S = 2  # sides of each dimension

plotStop = N

A = 2  # number of formation aircraft
D = 3  # dimensions (2 = 2-D, 3 = 3-D)
NI = 1  # number of non-cooperative intruders

wingspan = 0.267

offset = np.zeros(A)
sideCount = 0
for ac in range(A):  # setting aircraft spacing required from courseline for each side
    offset[ac] = sideCount
    if (ac % 2) == 0:
        sideCount += 1

finalCourseWidth = np.zeros((D, A, S), dtype=float)  # aircraft need to be on final altitude of z=0
for ac in range(A):
    if ac == 0:
        finalCourseWidth[1, ac, 0] = 0
        finalCourseWidth[1, ac, 1] = 0
    else:
        finalCourseWidth[1, ac, 0] = (0.8 * wingspan) * offset[ac]
        finalCourseWidth[1, ac, 1] = (0.8 * wingspan) * offset[ac]
    if D > 2:
        finalCourseWidth[2, ac, 0] = 0.0
        finalCourseWidth[2, ac, 1] = 0.0

wind = np.zeros(D)
wind[0:2] = [0.000, 0.000]
if D > 2:
    wind[2] = 0.000
windi = wind * delT

# jetwash input
jw = np.zeros(D)
jw[1] = 0.7 * wingspan
if D > 2:
    jw[2] = 0.7 * wingspan
js = 0.005
jsi = js * delT

wns = np.zeros(D)
wns = windi
if D > 2:
    wns[2] += jsi

Ps = round(plotStop)
pTime = 0.01

ppc = {
    0: "b",
    1: "cornflowerblue",
    2: "deepskyblue",
    3: "skyblue",
    4: "green",
    5: "limegreen",
    6: "turquoise",
    7: "aquamarine",
}
pc = {key: ppc[key] for key in range(A)}
ppcNI = {3: "coral", 2: "tomato", 1: "orangered", 0: "red"}
pcNI = {key: ppcNI[key] for key in range(NI)}

N5 = round(5 / delT)
NN5 = (N / N5)
if NN5 >= 10:
    N5 = N5 * 2
iN5 = 0
jN5 = 0

timeColor = {
    0: "black",
    1: "dimgrey",
    2: "darkgray",
    3: "darkgoldenrod",
    4: "hotpink",
    5: "lightcoral",
    6: "indianred",
    7: "tomato",
    8: "navajowhite",
    9: "orange",
}
time = {key: timeColor[key] for key in range(10)}

# load information
xMatrix0 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix0.csv", index_col=0).values
xMatrix1 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix1.csv", index_col=0).values
xMatrix2 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124xMatrix2.csv", index_col=0).values

vMatrix0 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix0.csv", index_col=0).values
vMatrix1 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix1.csv", index_col=0).values
vMatrix2 = pd.read_csv("vertical_only/2S20D/2S0D110T1100124vMatrix2.csv", index_col=0).values

x = np.array([xMatrix0, xMatrix1, xMatrix2])
v = np.array([vMatrix0, vMatrix1, vMatrix2])

# non-intruder
intruder_degree = 0
intruder_radians = math.radians(intruder_degree)
nix = np.zeros((D, N, NI))
niy = np.zeros((D, NI))
niy[0, 0] = -1 * math.cos(intruder_radians)
niy[1, 0] = -1 * math.sin(intruder_radians)
niy[2, 0] = 0.0

for iter in range(N):
    nix[0, iter, 0] = 20 * (1 + math.cos(intruder_radians)) + iter * delT * niy[0, 0]
    nix[1, iter, 0] = 20 * (math.sin(intruder_radians)) + iter * delT * niy[1, 0]
    nix[2, iter, 0] = 0.0 + iter * delT * niy[2, 0]

# side-only plot (x vs z)
fig, ax = plt.subplots(figsize=(14, 3))

# plot limits from formation + intruder
xmax = np.max([np.max(x[0, :, :]), np.max(nix[0, :, :])])
xmin = np.min([np.min(x[0, :, :]), np.min(nix[0, :, :])])
zmax = np.max([np.max(x[2, :, :]), np.max(nix[2, :, :])])
zmin = np.min([np.min(x[2, :, :]), np.min(nix[2, :, :])])

# add margins
xpad = 0.05 * (xmax - xmin) if xmax > xmin else 1.0
zpad = 0.1 * (zmax - zmin) if zmax > zmin else 0.1
xlim = (xmin - xpad, xmax + xpad)
ylim = (zmin - zpad, zmax + zpad)

ax.set_xlim(xlim)
ax.set_ylim(ylim)

# x-axis tick interval: 10
xtick_start = math.floor(xlim[0] / 10) * 10
xtick_end = math.ceil(xlim[1] / 10) * 10
ax.set_xticks(np.arange(xtick_start, xtick_end + 1e-6, 10))

# plot labels
ax.set_title("View from the side")
ax.set_xlabel("Along-course position (x1000ft)")
ax.set_ylabel("Altitude (x1000ft)")
ax.grid(True)

# optional final altitude constraint shading
if A > 1 and finalCourseWidth[2, 1, 1] != 0:
    ax.axhspan(-finalCourseWidth[2, 1, 0], finalCourseWidth[2, 1, 1], facecolor="0.9")

for i in range(Ps - 1):
    for ac in range(A):
        if i == (Ps - 2):
            ax.plot([x[0, i, ac], x[0, i + 1, ac]], [x[2, i, ac], x[2, i + 1, ac]], pc[ac], marker=">")
        elif iN5 == N5:
            verts = [[v[0, i, ac], v[2, i, ac] * 10], [-v[0, i, ac], 0], [0, -v[2, i, ac] * 10], [v[0, i, ac], v[2, i, ac] * 10]]
            if i == 0 and ac == 0:
                ax.plot([x[0, i, ac], x[0, i + 1, ac]], [x[2, i, ac], x[2, i + 1, ac]], pc[ac], label="formation", marker=verts)
            else:
                ax.plot([x[0, i, ac], x[0, i + 1, ac]], [x[2, i, ac], x[2, i + 1, ac]], pc[ac], marker=verts)
            ax.plot(x[0, i, ac], [x[2, i, ac]], time[jN5], marker="H")
        else:
            verts = [[v[0, i, ac], v[2, i, ac] * 10], [-v[0, i, ac], 0], [0, -v[2, i, ac] * 10], [v[0, i, ac], v[2, i, ac] * 10]]
            if i == 0 and ac == 0:
                ax.plot([x[0, i, ac], x[0, i + 1, ac]], [x[2, i, ac], x[2, i + 1, ac]], pc[ac], label="formation", marker=verts)
            else:
                ax.plot([x[0, i, ac], x[0, i + 1, ac]], [x[2, i, ac], x[2, i + 1, ac]], pc[ac], marker=verts)

    for ni in range(NI):
        if i == (Ps - 2):
            ax.plot([nix[0, i, ni], nix[0, i + 1, ni]], [nix[2, i, ni], nix[2, i + 1, ni]], pcNI[ni], marker="<")
        elif iN5 == N5:
            verts = [[niy[0, ni], niy[2, ni] * 10], [-niy[0, ni], 0], [0, -niy[2, ni] * 10], [niy[0, ni], niy[2, ni] * 10]]
            if i == 0 and ni == 0:
                ax.plot([nix[0, i, ni], nix[0, i + 1, ni]], [nix[2, i, ni], nix[2, i + 1, ni]], pcNI[ni], label="intruder", marker=verts)
            else:
                ax.plot([nix[0, i, ni], nix[0, i + 1, ni]], [nix[2, i, ni], nix[2, i + 1, ni]], pcNI[ni], marker=verts)
            ax.plot(nix[0, i, ni], [nix[2, i, ni]], time[jN5], marker="H")
        else:
            verts = [[niy[0, ni], niy[2, ni] * 10], [-niy[0, ni], 0], [0, -niy[2, ni] * 10], [niy[0, ni], niy[2, ni] * 10]]
            if i == 0 and ni == 0:
                ax.plot([nix[0, i, ni], nix[0, i + 1, ni]], [nix[2, i, ni], nix[2, i + 1, ni]], pcNI[ni], label="intruder", marker=verts)
            else:
                ax.plot([nix[0, i, ni], nix[0, i + 1, ni]], [nix[2, i, ni], nix[2, i + 1, ni]], pcNI[ni], marker=verts)

    if iN5 == N5:
        iN5 = 0
        jN5 += 1
        if jN5 == 10:
            jN5 = 0
    else:
        iN5 += 1

    ax.legend()
    plt.draw()
    plt.pause(pTime)

plt.show()
