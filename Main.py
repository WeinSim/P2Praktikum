from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from Expressions import *
from LinRegUncertainty import *

def tv1():
    print()
    print("--- Teilversuch 1 ---")

    xa = [7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0]
    p = [722.4, 703.4, 688.4, 672.4, 654.4, 639.4, 624.4, 611.4, 598.4, 584.4]
    p0 = 722.4
    pInv = []
    for i in range(len(p)):
        pInv.append(p0 / p[i])

    coefs = np.polyfit(xa, pInv, 1)
    yInterUnc = linRegUncertainty(xa, pInv, coefs)[1]

    slope = coefs[0]
    slopeInv = 1.0 / slope
    print(f"Steigung = {slope}")
    print(f"1 / Steigung = {slopeInv}")

    pp = PdfPages("GraphTV1.pdf")
    plt.figure()
    plt.clf()

    plt.plot(xa, pInv, 'bo', label="Messwerte")
    reg = np.polyval(coefs, xa)
    plt.plot(xa, reg, 'r-', label="Ausgleichsgerade")
    plt.plot(xa, reg + yInterUnc, 'r--', linewidth=0.5, label="Unsicherheitsgeraden")
    plt.plot(xa, reg - yInterUnc, 'r--', linewidth=0.5)
    plt.xlabel("Kolbenposition [cm]")
    plt.ylabel("Atmosphärendruck / Druck")
    plt.legend()
    plt.title("Inverser Druck vs. Kolbenposition")

    pp.savefig()
    pp.close()

def tv2():
    print()
    print("--- Teilversuch 2 ---")

    t = [89.9, 75.2, 60.1, 45.0, 30.0, 15.1, 0.1]
    p = [584.4, 564.4, 542.4, 515.4, 492.4, 459.4, 428.4]

    pLast = p[len(p) - 1]
    for i in range(len(p)):
        p[i] /= pLast

    coefs = np.polyfit(t, p, 1)
    yInterUnc = linRegUncertainty(t, p, coefs)[1]

    slope = coefs[0]
    slopeInv = 1.0 / slope
    print(f"Steigung = {slope}")
    print(f"1 / Steigung = {slopeInv}")

    pp = PdfPages("GraphTV2.pdf")
    plt.figure()
    plt.clf()

    plt.plot(t, p, 'bo', label="Messwerte")
    fit = np.polyval(coefs, t)
    plt.xlabel("Temperatur [°C]")
    plt.plot(t, fit, 'r-', label="Ausgleichsgerade")
    plt.plot(t, fit + yInterUnc, 'r--', linewidth=0.5, label="Unsicherheitsgeraden")
    plt.plot(t, fit - yInterUnc, 'r--', linewidth=0.5)
    plt.ylabel("Druck / letzteer Druck")
    plt.title("Druck vs. Temperatur")
    plt.legend()

    pp.savefig()
    pp.close()

def tv4():
    print()
    print("--- Teilversuch 4 ---")

    t = [0.1, 16.2, 30.4, 44.6, 60.4, 75.0, 90.0]
    v = [5.3, 5.5, 5.9, 6.2, 6.6, 7.0, 7.3]

    v0 = v[0]
    for i in range(len(v)):
        v[i] /= v0

    coefs = np.polyfit(t, v, 1)
    yInterUnc = linRegUncertainty(t, v, coefs)[1]

    slope = coefs[0]
    slopeInv = 1.0 / slope
    print(f"Steigung = {slope}")
    print(f"1 / Steigung = {slopeInv}")

    pp = PdfPages("GraphTV4.pdf")
    plt.figure()
    plt.clf()

    plt.plot(t, v, 'bo', label="Messwerte")
    fit = np.polyval(coefs, t)
    plt.xlabel("Temperatur [°C]")
    plt.plot(t, fit, 'r-', label="Ausgleichsgerade")
    plt.plot(t, fit + yInterUnc, 'r--', linewidth=0.5, label="Unsicherheitsgeraden")
    plt.plot(t, fit - yInterUnc, 'r--', linewidth=0.5)
    plt.ylabel("Volumen / Anfangsvolumen")
    plt.title("Volumen vs. Temperatur")
    plt.legend()

    pp.savefig()
    pp.close()

def tv5():
    print()
    print("--- Teilversuch 5 ---")
    rho = Const(1000)
    g = Const(9.81)
    pi = Const(math.pi)
    p0_mmhg = Var(722.4, 0.25, "p0_mmhg")
    p0 = Mult(p0_mmhg, Const(133))
    massFull = Var(1.531, 0.00013, "mFull")
    massEmpty = Var(0.41703, 0.00003, "mEmpty")
    diameter = Var(0.016, 0.0005, "d")
    height = Var(0.172, 0.001, "h")
    t0 = Var(1.166, 0.020, "t0")
    tk = Var(0.760, 0.012, "tk")
    vPiston = Div(Sub(massFull, massEmpty), rho)
    a = Mult(pi, Pow(Div(diameter, Const(2)), 2))
    vColumn = Mult(height, a)
    v = Add(vPiston, vColumn)
    params = [massFull, massEmpty, diameter, height, p0_mmhg, t0, tk]
    print(f"V = {v.eval()}")
    print(f"∆V = {gaussian(v, params)}")
    num = Mult(Mult(Mult(Const(2), rho), g), v)
    den = Mult(p0, a)
    gamma = Mult(Div(num, den), Sub(Pow(Div(t0, tk), 2), Const(1)))
    print(f"gamma = {gamma.eval()}")
    print(f"∆gamma = {gaussian(gamma, params)}")

tv1()
tv2()
tv4()
tv5()
