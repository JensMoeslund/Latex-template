import matplotlib.pyplot as plt
import os
import matplotlib
import schemdraw as sd
from schemdraw import flow
from schemdraw import elements as elm
import schemdraw_addon as sda
import numpy as np

matplotlib.rcParams['font.serif'] = 'Palatino Linotype'
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.size'] = 20
matplotlib.rc('xtick', labelsize=25)
matplotlib.rc('ytick', labelsize=25)
file = (os.path.basename(__file__).replace(".py", ""))
filepath = os.path.dirname(__file__) + "/"
# ------------------------------------------------------------------------


with sd.Drawing(file=(filepath + file + ".pdf")) as d:
    # Boxes
    d += (i := flow.Box(w=2, h=1, anchor="center").at((0, 0))) \
        .label(color="red", label="initiator")
    d += (r := flow.Box(w=2, h=1, anchor="center").at((12, 0)))\
        .label(color="blue", label="reflector")
    d += (saw := flow.Box(w=1, h=0.75, anchor="center").at((2, 0)))\
        .label(color="black", label="group\ndelay")
    d += (saw2 := flow.Box(w=1, h=0.75, anchor="center").at((10, 0)))\
        .label(color="black", label="group\ndelay")

    # Lines
    d += flow.Line().at(i.E).to(saw.W)
    d += flow.Line().at(saw.N).up(1)
    d.push()
    d += flow.Line().to(d.here, dy=1,dx=1)
    d.pop()
    d += flow.Line().to(d.here, dy=1,dx=-1)

    d += flow.Line().at(r.W).to(saw2.E)
    d += flow.Line().at(saw2.N).up(1)
    d.push()
    d += flow.Line().to(d.here, dy=1,dx=1)
    d.pop()
    d += flow.Line().to(d.here, dy=1,dx=-1)

    # Arrows
    d += flow.Wire("n", k=-1, arrow="->").at(r.S).to(i.S) \
        .label(r"$\{ IQ_R(f_1), IQ_R(f_2), \cdots, IQ_R(f_K) \}$")

    # striped boxes
    d += flow.Wire("|-").at(i.E, dx=2.5, dy=2.5).to(r.W, dx=-2.5, dy=-1).linestyle("--")
    d += flow.Wire("-|").at(i.E, dx=2.5, dy=2.5).to(r.W, dx=-2.5, dy=-1).linestyle("--") \
        .label(r"$k \in \{1, 2, \cdots, K\}$", loc="top")
    # sine waves
    # d += (A := flow.Arc2().at(i.E, dx=1).to(r.W, dx=-1, dy=-1))
    # d += elm.Dot().at(A.mid)
    d += sda.SineWave(freq=5.1, amp=0.25, phase=0, numsegments=1000, arrow="->") \
        .at(i.E, dx=3, dy=1.5).to(r.W, dx=-3, dy=1.5).color("red") \
        .label(r"$f_k$", loc="left", ofst=(-0.35, -0.35),color="black")
    d += sda.SineWave(freq=5.1, amp=0.25, phase=1, numsegments=1000, arrow="->") \
        .at(r.W, dx=-3, dy=0).to(i.E, dx=3, dy=0).color("blue") \
        .label(r"$f_k$", loc="right", ofst=(0, -0.25),color="black")
    # d += sda.SineWave(freq=2,phase=1,amp=0.25).at((-5, 0)).to((-4, -1))
    # d += flow.Line().at((-5, 0)).to((-4, -1)).color("red")
