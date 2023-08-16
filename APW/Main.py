from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from LinRegUncertainty import *
from Expressions import *

def tv1():
    print()
    print("--- Teilversuch 1 ---")
    tPb = [0, 5, 10, 15, 20, 25, 80, 85, 90, 95, 100, 105, 110, 115, 120,
           135, 140, 150, 180, 210, 240, 270, 300, 330, 360, 390]
    thetaPb = [24.1, 24.4, 23.7, 24.3, 24.4, 24, 26.1, 27.8, 28.3, 28.3,
               28.4, 28.1, 27.7, 27, 28.5, 28.1, 28.4, 28.0, 27.6, 28.1,
               28.0, 27.7, 27.8, 27.9, 27.7, 27.9]
    evaluate(tPb, thetaPb, 1.943690, 80.3, 1.115600, 69, 0.207, "Blei")
    print()
    tAl = [0, 5, 10, 15, 20, 25, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110,
           115, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    thetaAl = [23.3, 23, 23, 23.3, 23, 23, 27.7, 29.1, 28.5, 31.3, 31.6,
               32.2, 32.4, 32.8, 32.7, 32.9, 32.6, 32.9, 32.4, 28.2, 28.5,
               27.9, 27.5, 27.4, 27.7, 27.6]
    numUpshift = 16
    amountUpshift = -4
    for i in range(6, 19):
        thetaAl[i] += amountUpshift
    evaluate(tAl, thetaAl, 0.482970, 78.0, 1.123150, 72, 0.027, "Aluminium")

    print(f"3 * R = {3 * 8.31}")

def evaluate(t, theta, mass, theta0, measureFull, tMix, mMass, name):
    print(f"{name}: ")
    numPoints1 = 6
    t1 = []
    theta1 = []
    for i in range(numPoints1):
        t1.append(t[i])
        theta1.append(theta[i])
    coefs1 = np.polyfit(t1, theta1, 1)

    numPoints2 = 9
    t2 = []
    theta2 = []
    for i in range(len(t) - numPoints2 - 1, len(t)):
        t2.append(t[i])
        theta2.append(theta[i])
    coefs2 = np.polyfit(t2, theta2, 1)

    uncertainties1 = linRegUncertainty(t1, theta1, coefs1)
    mixTempTime = Var(tMix, 5, "t")
    yIntercept1 = Var(coefs1[1], uncertainties1[1], "yInter")
    slope1 = Var(coefs1[0], uncertainties1[0], "slope")
    kaloriTemp = Add(Mult(mixTempTime, slope1), yIntercept1)
    params = [mixTempTime, yIntercept1, slope1]
    print(f"Kalorimetertemperatur = {kaloriTemp.eval()}")
    print(f"delta T (min/max) = {minMax(kaloriTemp, params)}")

    uncertainties2 = linRegUncertainty(t2, theta2, coefs2)
    yIntercept2 = Var(coefs2[1], uncertainties2[1], "yInter")
    slope2 = Var(coefs2[0], uncertainties2[0], "slope")
    mixTemp = Add(Mult(mixTempTime, slope2), yIntercept2)
    params = [mixTempTime, yIntercept2, slope2]
    print(f"Mischtemperatur = {mixTemp.eval()}")
    print(f"delta T (min/max) = {minMax(mixTemp, params)}")

    massMeasureFull = Var(measureFull, 0.000010, "m_Voll")
    massMeasureEmpty = Var(0.306600, 0.000010, "m_Leer")
    wasserWert = Const(0.08)
    cWater = Const(4180)
    massBlock = Var(mass, 0.000010, "m_s")
    thetaS = Var(theta0, 0.001 * theta0 + 0.7, "theta_s")
    mWater = Add(Sub(massMeasureFull, massMeasureEmpty), wasserWert)
    num = Mult(Mult(cWater, mWater), Sub(mixTemp, kaloriTemp))
    den = Mult(massBlock, Sub(thetaS, mixTemp))
    cS = Div(num, den)
    molarMass = Const(mMass)
    cM = Mult(cS, molarMass)
    params = [mixTempTime, yIntercept1, slope1, yIntercept2, slope2, massMeasureFull,
              massMeasureEmpty, massBlock, thetaS]
    print(f"Spezifische Wärmekapazität {name} = {cS.eval()}")
    print(f"delta c {name} = {minMax(cS, params)}")
    print(f"Molare Wärmekapazität {name} = {cM.eval()}")
    print(f"delta c_M {name} = {minMax(cM, params)}")

    pp = PdfPages(f"GraphTV1{name}.pdf")

    plt.figure()
    plt.clf()

    plt.plot(t, theta, 'bo', label=f"Messwerte {name}")
    tCont = np.arange(min(t), max(t), 1)
    plt.plot(tCont, np.polyval(coefs1, tCont), 'r-', label='Ausgleichsgeraden')
    thetaCont = np.polyval(coefs1, tCont)
    plt.plot(tCont, thetaCont, 'r-')
    plt.plot(tCont, thetaCont + uncertainties1[1], 'r--', linewidth='0.5', label='Unsicherheitsgeraden')
    plt.plot(tCont, thetaCont - uncertainties1[1], 'r--', linewidth='0.5')
    thetaCont = np.polyval(coefs2, tCont)
    plt.plot(tCont, thetaCont, 'r-')
    plt.plot(tCont, thetaCont + uncertainties2[1], 'r--', linewidth='0.5')
    plt.plot(tCont, thetaCont - uncertainties2[1], 'r--', linewidth='0.5')
    plt.title(f"{name} - Temperatur vs. Zeit")
    plt.xlabel('Zeit (s)')
    plt.ylabel('Temperatur (°C)')
    plt.legend()
    pp.savefig()

    pp.close()

def tv2():
    print()
    print("--- Teilversuch 2 ---")
    qv = Const(199e3)
    m0 = Var(2.46224, 0.00001, "m0")
    m1 = Var(2.05876, 0.00001, "m1")
    t0 = Var(124, 0.5, "t0")
    t1 = Var(284, 0.5, "t1")
    dt = Sub(t1, t0)
    dmdt = Const(-0.0012 / 60)
    deltaM = Mult(dt, dmdt)
    mv = Add(Sub(m0, m1), deltaM)
    mx = Var(0.48297, 0.00001, "mx")
    temp1 = Var(23.9, 0, "temp1")
    temp1.uncertainty = 0.001 * temp1.value + 0.7
    temp1.value += 273.15
    temp2 = Var(77, 0, "temp2")
    deltaT = Sub(temp1, temp2)
    c = Div(Mult(mv, qv), Mult(mx, deltaT))
    params = [m0, m1, t0, t1, mx, temp1, temp2]
    print(f"c = {c}")
    print(f"c = {c.eval()}")
    print(f"∆c = {gaussian(c, params)}")

def tv4():
    print()
    print("--- Teilversuch 4 ---")
    ts = [60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 250]
    ps = [0, 0.1, 0.8, 1.6, 3.2, 5.8, 9.2, 14.8, 22.4, 32.7, 39.0]
    tInv = []
    lnP = []
    for i in range(1, len(ts)):
        t = ts[i] + 273.15
        tInv.append(-1.0 / t)
        p = ps[i] + 1
        lnP.append(math.log(p))

    coefs = np.polyfit(tInv, lnP, 1)
    (slopeUnc, yInterUnc) = linRegUncertainty(tInv, lnP, coefs)
    print(f"Steigung = {coefs[0]}")
    print(f"delta Steigung = {slopeUnc}")

    k = Const(1.38065e-23)
    e = Const(1.6e-19)
    NA = Const(6.022e23)
    slopeVar = Var(coefs[0], slopeUnc, "Steigung")
    eb = Mult(slopeVar, k)
    ebEV = Div(eb, e)
    ebMol = Mult(eb, NA)
    params = [slopeVar]
    print("In Joule / Molekül:")
    print(f"E_b = {eb.eval()}")
    print(f"delta E_b = {gaussian(eb, params)}")

    print("In eV / Molekül:")
    print(f"E_b = {ebEV.eval()}")
    uncertainty = gaussian(ebEV, params)
    print(f"delta E_b = {uncertainty}")
    expected = 0.4
    print(f"Erwarteter Wert: E_erwartet = {expected}")
    difference = abs(ebEV.eval() - expected)
    print(f"Unterschied: |E_b - E_erwartet| = {difference} = {difference / uncertainty} * delta E_b")

    print("In Joule / Mol:")
    print(f"E_b = {ebMol.eval()}")
    print(f"delta E_b = {gaussian(ebMol, params)}")

    pp = PdfPages("GraphTV4.pdf")
    plt.figure()
    plt.clf()

    plt.plot(tInv, lnP, 'bo', label='Messwerte')
    tCont = np.arange(min(tInv), max(tInv), (max(tInv) - min(tInv)) / 50)
    regLine = np.polyval(coefs, tCont)
    plt.plot(tCont, regLine, 'r-', label='Ausgleichsgerade')
    plt.plot(tCont, regLine - yInterUnc, 'r--', linewidth='0.5', label="Unsicherheitsgeraden")
    plt.plot(tCont, regLine + yInterUnc, 'r--', linewidth='0.5')
    plt.title("Druck vs. Temperatur")
    plt.xlabel("-1/T [K^-1]")
    plt.ylabel("ln(p / bar)")
    plt.legend()

    pp.savefig()
    pp.close()
    
def tv5():
    print()
    print("--- Teilversuch 5 ---")
    t = [80, 100, 130, 160, 190, 210, 240, 270, 300]
    u = [0.012, 0.021, 0.032, 0.049, 0.066, 0.081, 0.107, 0.163, 0.173]
    t0 = 23.4
    t04 = (t0 + 273.15) ** 4
    t4 = []
    for i in range(len(u)):
        t4.append((t[i] + 273.15) ** 4 - t04)

    coefs = np.polyfit(t4, u, 1)
    yInterUnc = linRegUncertainty(t4, u, coefs)[1]

    print(f"y-Achsenabschnitt = {coefs[1]}")
    print(f"∆y-Achsenabschnitt = {yInterUnc}")

    pp = PdfPages("GraphTV5.pdf")
    plt.figure()
    plt.clf()

    plt.plot(t4, u, 'bo', label='Messwerte')
    tCont = np.arange(min(t4), max(t4), (max(t4) - min(t4)) / 50)
    uCont = np.polyval(coefs, tCont)
    plt.plot(tCont, uCont, 'r-', label='Ausgleichsgerade')
    plt.plot(tCont, uCont - yInterUnc, 'r--', linewidth='0.5', label='Unsicherheitsgeraden')
    plt.plot(tCont, uCont + yInterUnc, 'r--', linewidth='0.5')
    plt.title("Spannung vs. Temperatur")
    plt.xlabel("T^4 - T_0^4 [K^4]")
    plt.ylabel("Spannung [mV]")
    plt.legend()

    pp.savefig()
    pp.close()

tv1()
tv2()
tv4()
tv5()
