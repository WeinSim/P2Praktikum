from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from Expressions import *
from LinRegUncertainty import *

divDelta = 2 ** 0.5 / 30

def tv2():
    print()
    print("--- Teilversuch 2 ---")
    evalVoltage(23.4, 8.38, 5, "Simon")
    print()
    evalVoltage(24.0, 8.57, 10, "Yannic")

def evalVoltage(uOV, uMV, uDiv, name):
    print(f"{name}:")
    dUO = uDiv * divDelta
    uO = Var(uOV, dUO, "U_O")
    dUM = 0.01 * uMV + 3 * 0.01
    uM = Var(uMV, dUM, "U_M")
    uEff = Div(uO, Const(2 * (2 ** 0.5)))
    params = [ uO, uM ]
    print(f"∆U_O = {dUO}")
    print(f"∆U_M = {dUM}")
    print("U_Eff aus Oszillatorwert berechnet:")
    print(f"U_Eff = {uEff.eval()}")
    print(f"∆U_Eff = {gaussian(uEff, params)}")
    print("U_M vom vom Multimeter gemessen:")
    print(f"U_M = {uM.eval()}")
    print(f"∆U_M = {gaussian(uM, params)}")

def tv3():
    print()
    print("--- Teilversuch 3 --")
    evalAngle(0.000465, 399, 2.58, 2.39, "Simon")
    print()
    evalAngle(0.00136, 300, 2.65, 1.47, "Yannic")

def evalAngle(dtV, fV, xAV, dxV, name):
    print(f"{name}:")
    ddt = 0.001 * divDelta
    print(f"∆t = {ddt}")
    dt = Var(dtV, 0.001 * divDelta, "dt")
    f = Var(fV, 0.5, "f")
    dPhiA = Mult(dt, Mult(Const(2 * math.pi), f))
    dxa = 0.5 * divDelta
    print(f"∆x = {dxa}")
    xA = Var(xAV, dxa, "x_A")
    dx = Var(dxV, 0.5 * divDelta, "dx")
    sinPhi1 = Div(dx, xA)
    dPhiB1 = Asine(sinPhi1)
    dPhiB2 = Sub(Const(math.pi), dPhiB1)
    params = [ dt, f ]
    print("Berechnung durch t-y Graphen:")
    print(f"phi = {dPhiA.eval()}")
    print(f"∆phi = {gaussian(dPhiA, params)}")
    params = [ xA, dx ]
    print("Berechnung durch Lissajous-Ellipse:")
    print(f"phi_1 = {dPhiB1.eval()}")
    print(f"∆phi_1 = {gaussian(dPhiB1, params)}")
    print(f"phi_2 = {dPhiB2.eval()}")
    print(f"∆phi_2 = {gaussian(dPhiB2, params)}")
    
def tv5():
    print()
    print("--- Teilversuch 5 ---")
    u1 = [ 0.857, 0.697, 0.561, 0.457, 0.369, 0.301, 0.241, 0.197, 0.161, 0.129 ]
    u2 = [ 7.85, 5.73, 3.65, 2.45, 1.69, 1.17, 0.80, 0.52, 0.36, 0.24 ]
    (slopeV1, dSlope1) = evalCapVolt(u1, 0.1, 10)
    print()
    (slopeV2, dSlope2) = evalCapVolt(u2, 1, 1)
    print()

    slope1 = Var(slopeV1, dSlope1, "s1")
    tauS1 = Div(Const(-1), slope1)
    params = [ slope1 ]
    print("Tau berechnet aus der Steigung der Ausgleichsgerade für x1:")
    print(f"tau_1 = {tauS1.eval()}")
    print(f"∆tau_1 = {gaussian(tauS1, params)}")

    slope2 = Var(slopeV2, dSlope2, "s2")
    tauS2 = Div(Const(-1), slope2)
    params = [ slope2 ]
    print("Tau berechnet aus der Steigung der Ausgleichsgerade für x10:")
    print(f"tau_2 = {tauS2.eval()}")
    print(f"∆tau_2 = {gaussian(tauS2, params)}")

    r = Var(1e6, 1e4, "R")
    c = Var(1e-6, 1e-8, "C")
    tau = Mult(r, c)
    params = [ r, c ]
    print("Tau berechnet aus R * C:")
    print(f"tau_0 = {tau.eval()}")
    print(f"∆tau_0 = {gaussian(tau, params)}")

    difference = abs(tauS1.eval() - tau.eval())
    unc = gaussian(tau, params) + gaussian(tauS1, [ slope1 ]) 
    ratio = difference / unc

    print()
    print("Verhältnis aus Differenz von tau_0 und tau_1 und der Summe ihrer Unsicherheiten:")
    print(ratio)

def evalCapVolt(us, divU, tk):
    tms = [ 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000 ]
    t = []
    for tm in tms:
        t.append(tm / 1000.0)
    lnU = []
    for u in us:
        lnU.append(math.log(u))
    coefs, cov = np.polyfit(t, lnU, 1, cov=True)

    slope = coefs[0]
    dSlope = cov[0][0] ** 0.5
    yInter = coefs[1]
    dYInter = linRegUncertainty(t, lnU, coefs)[1]
    
    pp = PdfPages(f"GraphTV5_x{tk}.pdf")
    plt.figure()
    plt.clf()

    plt.plot(t, lnU, 'bo', label="Messwerte")
    fit = np.polyval(coefs, t)
    plt.plot(t, fit, 'r-', label="Ausgleichsgerade")
    plt.plot(t, fit - dYInter, 'r--', label="Fehlergeraden")
    plt.plot(t, fit + dYInter, 'r--')

    plt.xlabel("Zeit [s]")
    plt.ylabel("ln(U / V)")
    plt.title("Entladen eines Kondensators\nKondensatorspannung vs. Zeit")
    plt.legend()

    pp.savefig()
    pp.close()

    print(f"Tastkopf x{tk}:")
    print(f"Steigung = {slope}")
    print(f"∆Steigung = {dSlope}")

    return (slope, dSlope)

tv2()
tv3()
tv5()
