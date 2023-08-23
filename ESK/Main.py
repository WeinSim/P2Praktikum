from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from Expressions import *
from LinRegUncertainty import *

def tv1():
    i = [ 11.53, 14.74, 18.12, 21.51, 24.6, 27.8, 31.2, 34.2, 37.7, 40.8, 44.4 ]
    u = [ 1.492, 1.483, 1.462, 1.453, 1.437, 1.425, 1.406, 1.396, 1.381, 1.367, 1.351 ]

    coefs = np.polyfit(i, u, 1)

    pp = PdfPages("GraphTV1.pdf")
    plt.figure()
    plt.clf()

    plt.plot(i, u, 'bo', label='Messwerte')
    fitLabel = "Ausgleichsgerade: y = m * x + t\nm = %.5f\nt = %.5f" % (coefs[0], coefs[1])
    plt.plot(i, np.polyval(coefs, i), 'r-', label=fitLabel)

    plt.xlabel("Stromstärke [mA]")
    plt.ylabel("Klemspannung [V]")
    plt.title("Klemmspannung vs. Stromstärke")
    plt.legend()
    pp.savefig()
    pp.close()

def tv2():
    u = [ 0, 2.05, 3.95, 5.97, 8.08, 10.02, 12.08, 14.04, 15.99, 17.97, 19.91 ]
    i = [ 0, 0.62, 1.19, 1.80, 2.45, 3.04, 3.67, 4.28, 4.85, 5.46, 6.05 ]
    
    coefs, cov = np.polyfit(u, i, 1, cov=True)
    slopeUnc = cov[0][0] ** 0.5

    pp = PdfPages("GraphTV2.pdf")
    plt.figure()
    plt.clf()

    plt.plot(u, i, 'bo', label='Messwerte')
    fitLabel = "Ausgleichsgerade: y = m * x + t\nm = %.5f\nt = %.5f\n∆m = %.5f" % (coefs[0], coefs[1], slopeUnc)
    plt.plot(u, np.polyval(coefs, u), 'r-', label=fitLabel)

    plt.xlabel("Spannung [V]")
    plt.ylabel("Stromstärke [mA]")
    plt.title("Stromstärke vs. Spannung")
    plt.legend()
    pp.savefig()
    pp.close()

def tv3():
    s = [ 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000 ]
    u = [ 0.0126, 0.994, 1.985, 2.96, 3.95, 4.94, 5.93, 6.91, 7.90, 8.88, 9.87 ]

    coefs = np.polyfit(s, u, 1)

    pp = PdfPages("HelipotGraphTV3.pdf")
    plt.figure()
    plt.clf()

    plt.plot(s, u, 'bo', label='Messwerte')
    fitLabel = "Ausgleichsgerade: y = m * x + t\nm = %.5f\nt = %.5f" % (coefs[0], coefs[1])
    plt.plot(s, np.polyval(coefs, s), 'r-', label=fitLabel)

    plt.xlabel("Helipot Skalenwerte")
    plt.ylabel("Ausgangsspannung [V]")
    plt.title("Helipot Skalenwert vs. Ausgangsspannung")
    plt.legend()
    pp.savefig()
    pp.close()

    l = [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ]
    u = [ 0.65, 1.32, 1.97, 2.63, 3.28, 3.94, 4.59, 5.24, 5.88, 6.48 ]

    coefs = np.polyfit(l, u, 1)

    pp = PdfPages("DrahtSpannungenTV3.pdf")
    plt.figure()
    plt.clf()

    plt.plot(l, u, 'bo', label='Messwerte')
    fitLabel = "Ausgleichsgerade: y = m * x + t\nm = %.5f\nt = %.5f" % (coefs[0], coefs[1])
    plt.plot(l, np.polyval(coefs, l), 'r-', label=fitLabel)

    plt.xlabel("Länge des Drahtstückes [cm]")
    plt.ylabel("Spannungsabfall [V]")
    plt.title("Drahtlänge vs. Spannungsabfall")
    plt.legend()
    pp.savefig()
    pp.close()

def tv4():
    print("--- Teilversuch 4 ---")
    x0 = Const(1000)
    xsn = Var(481, 0.5, "x_sn")
    usn = Var(1, 0.0001, "U_sn")
    u0 = Mult(Div(x0, xsn), usn)
    xg = Var(748.5, 0.5, "x_g")
    ug = Mult(Div(xg, x0), u0)
    params = [ xsn, usn, xg ]
    print(f"u0 = {u0.eval()}")
    print(f"∆u0 = {gaussian(u0, params)}")
    print(f"ug = {ug.eval()}")
    print(f"∆ug = {gaussian(ug, params)}")

def tv5():
    print("--- Teilversuch 5 ---")
    i = [ 2.81, 0.59, 1.48, 0.73, 1.32, 1.32, 1.32, 1.32 ] 
    u = [ -10.06, 1.96, 10.06, 1.96, 2.91, 5.17 ]
    iUncPercent = 1.3
    iUncDigits = 7
    uUncPercent = 0.9
    uUncDigits = 4
    di = []
    du = []
    for j in range(len(i)):
        di.append(0.01 * iUncPercent * abs(i[j]) + 0.01 * iUncDigits)
        print("I_%d = %.2f +/- %.4f" % (j, i[j], di[j]))
        print("I_%d_min = %.4f" % (j, i[j] - di[j]))
        print("I_%d_max = %.4f" % (j, i[j] + di[j]))
        print()
    print()
    for j in range(len(u)):
        du.append(0.01 * uUncPercent * abs(u[j]) + 0.01 * uUncDigits)
        print("U_%d = %.2f +/- %.4f" % (j, u[j], du[j]))
        print("U_%d_min = %.4f" % (j, u[j] - du[j]))
        print("U_%d_max = %.4f" % (j, u[j] + du[j]))
        print()

    print()
    print("Knoten A:")
    printEq(i, di, "I", (0, ), (5, 2))
    print()

    print("Knoten B:")
    printEq(i, di, "I", (5, ), (1, 3))
    print()

    print("Knoten C:")
    printEq(i, di, "I", (1, 3), (4, ))
    print()

    print("Knoten D:")
    printEq(i, di, "I", (2, 7), (0, ))
    print()

    print("Masche BC:")
    printEq(u, du, "U", (1, ), (3, ))
    print()

    print("Masche EAD:")
    printEq(u, du, "U", (0, ), (2, ))
    print()

    print("Masche ABCD:")
    printEq(u, du, "U", (2, ), (3, 4, 5))
    print()

def printEq(values, uncertainties, name, right, left):
    lleft = generateEq(values, uncertainties, name, left)
    lright = generateEq(values, uncertainties, name, right)
    for i in range(3):
        print(f"{lleft[i]} = {lright[i]}")
    i = 3
    print("Links Min:")
    print(f"{lleft[i]} = {lleft[i + 1]} = {lleft[i + 2]}")
    i = 6
    print("Links Max:")
    print(f"{lleft[i]} = {lleft[i + 1]} = {lleft[i + 2]}")
    i = 3
    print("Rechts Min:")
    print(f"{lright[i]} = {lright[i + 1]} = {lright[i + 2]}")
    i = 6
    print("Rechts Max:")
    print(f"{lright[i]} = {lright[i + 1]} = {lright[i + 2]}")

# i1 + i2
# 0.5 + 1.8
# 2.3
# i1 - ∆i1 + i2 - ∆i2 
# 0.5 - 0.1 + 1.8 - 0.1
# 2.1
# 0.5 + 0.1 + 1.8 + 0.1
# 2.5
def generateEq(values, uncertainties, name, indices):
    ret = []
    s = ""
    for i in indices:
        s += f"{name}_{i} + "
    s = s[:-3]
    ret.append(s)
    s = ""
    total = 0
    for i in range(len(indices)):
        val = values[indices[i]]
        s += "%.2f + " % val
        total += val
        unc = uncertainties[indices[i]]
    s = s[:-3]
    ret.append(s)
    s = "%.2f" % total
    ret.append(s)

    s = ""
    for i in indices:
        s += f"{name}_{i}_min + "
    s = s[:-3]
    ret.append(s)
    s = ""
    total = 0
    for i in range(len(indices)):
        val = values[indices[i]]
        unc = uncertainties[indices[i]]
        val -= unc
        s += "%.4f + " % val
        total += val
    s = s[:-3]
    ret.append(s)
    s = "%.4f" % total
    ret.append(s)

    s = ""
    for i in indices:
        s += f"{name}_{i}_max + "
    s = s[:-3]
    ret.append(s)
    s = ""
    total = 0
    for i in range(len(indices)):
        val = values[indices[i]]
        unc = uncertainties[indices[i]]
        val += unc
        s += "%.4f + " % val
        total += val
    s = s[:-3]
    ret.append(s)
    s = "%.4f" % total
    ret.append(s)

    return ret

tv1()
tv2()
tv3()
tv4()
tv5()
