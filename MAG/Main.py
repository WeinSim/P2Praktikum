from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from LinRegUncertainty import *
from Expressions import *

def tv2():
    print()
    print("--- Teilversuch 2 ---")
    alpha = np.arange(0.0, 100, 10);
    sinAlpha = alpha.copy()
    for i in range(len(alpha)):
        sinAlpha[i] = math.sin(math.pi * alpha[i] / 180.0)
    beta = [312.8, 333.5, 354.0, 12.0, 30.5, 45.5, 61.0, 74.5, 87.0, 98.5]
    beta0 = beta[0]
    for i in range(len(beta)):
        if (i >= 3):
            beta[i] += 360
        beta[i] -= beta0
    phi = beta - alpha
    phiUncertainty = 0.8

    coefs= np.polyfit(sinAlpha, phi, 1)
    yInterUnc = linRegUncertainty(sinAlpha, phi, coefs)[1]
    reg0 = np.polyval(coefs, 0)
    print(f"Ausgleichsgerade ausgewertet bei x=0: {reg0}")
    print(f"Unsicherheit des Ordinatenabschnitts: {yInterUnc}")
    print(f"Verhältnis: {reg0 / yInterUnc}")

    pp = PdfPages("GraphTV2.pdf")

    plt.figure()
    plt.clf()

    plt.errorbar(sinAlpha, phi, np.ones(len(phi)) * phiUncertainty, fmt='None', label='Messreihe') #'bo')
    xcont = np.arange(-0.2, 1.2, 0.05)
    plt.plot(xcont, np.polyval(coefs, xcont), 'r-', linewidth=1.0, label='Ausgleichsgerade')
    plt.plot(xcont, np.polyval(coefs, xcont) - yInterUnc, 'r-', linewidth=0.3, label='Unsicherheitsgeraden')
    plt.plot(xcont, np.polyval(coefs, xcont) + yInterUnc, 'r-', linewidth=0.3)
    plt.title('phi vs. sin(alpha)')
    plt.xlabel('phi (°)')
    plt.ylabel('sin(alpha)')
    plt.legend()
    pp.savefig()

    pp.close()

def tv3():
    print()
    print("--- Teilversuch 3 ---")
    voltages = [1.07, 1.05, 1.11, 1.15, 1.00, 1.16, 1.17, 1.19, 1.12, 1.17, 1.12, 1.16, 1.17, 1.15, 1.10]
    mean = 0
    for v in voltages:
        mean += v
    mean /= len(voltages)
    print(f"U = {mean}")
    dv = (max(voltages) - min(voltages)) / 2
    print(f"delta U = {dv}")

    a = Var(0.00239, 0, "A")
    n = Var(82800, 0, "N")
    rpm = Var(16.6, 0, "rpm")
    u = Var(mean, 0.10, "U")
    params = [a, n, rpm, u]

    denConst = Const(2 * math.pi * 5/6 / 60)
    den = Mult(Mult(Mult(denConst, n), a), rpm)
    magnet = Div(u, den)
    print("Magnetfeld berechnet aus Induktion:")
    print(f"B = {magnet.eval()}")
    print(f"delta B = {gaussian(magnet, params)}")
    print("Magnetfeld berechnet aus Helmholtz-Spulenpaar:")
    n = Var(528, 0, "N")
    dAussen = Var(0.305, 0.001, "d_Aussen")
    dInnen = Var(0.252, 0.001, "d_Innen")
    mu0 = Const(4 * math.pi * 1e-7)
    i = Var(1.089, 0.014, "I")
    den = Div(Add(dAussen, dInnen), Const(4))
    magnet = Mult(Mult(Mult(mu0, Const((4/5) ** (3/2))), i), Div(n, den))
    params = [n, dAussen, dInnen, mu0]
    print(f"B = {magnet}")
    print(f"B = {magnet.eval()}")
    print(f"delta B = {gaussian(magnet, params)}")

def tv4():
    print()
    print("--- Teilversuch 4 ---")
    mu0 = Const(4 * math.pi * 1e-7)
    nf = Var(528, 0, "NF")
    ni = Var(82800, 0, "NI")
    a = Var(0.00239, 0.00001, "A")
    dAussen = Var(0.305, 0.001, "D_Außen")
    dInnen = Var(0.252, 0.001, "D_Innen")
    r = Div(Add(dAussen, dInnen), Const(4))
    c = Mult(Mult(mu0, Const(0.8 ** 1.5)), Div(Mult(Mult(ni, nf), a), r))
    print(f"c = {c}")
    print(f"c = {c.eval()}")
    params = [ a, dAussen, dInnen ]
    print(f"delta c = {gaussian(c, params)}")
    dis = [0.078, 0.13, 0.13, 0.40, 0.53]
    dts = [5, 3.5, 1.9, 4.2, 4.7]
    us = [0.013, 0.028, 0.051, 0.068, 0.079]
    du = 0.002
    for i in range(len(dis)):
         di = Var(dis[i], 0.013, f"i{i}")
         dt = Var(dts[i], 0.1, f"t{i}")
         didt = Div(di, dt)
         u = Mult(c, didt)
         paramsi = params.copy()
         paramsi.append(di)
         paramsi.append(dt)
         print()
         print(f"{i+1}:")
         ub = u.eval()
         print(f"U_b = {ub}")
         dub = gaussian(u, paramsi)
         print(f"delta U_b = {dub}")
         print(f"U_g = {us[i]} +/- {du}")
         distance = abs(ub - us[i])
         fraction = distance / (dub + du)
         print(f"Abstand: {fraction} * (delta U_b + delta U_g)")

tv2()
tv3()
tv4()
