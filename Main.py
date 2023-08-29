from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from Expressions import *
from LinRegUncertainty import *

def tv2():
    print()
    print("--- Teilversuch 2 ---")

    r = Var(10e3, 0.01 * 10e3, "R")
    c = Var(10e-9, 0.05 * 10e-9, "C")
    w = Div(Const(1), Mult(r, c))
    
    params = [ r, c ]
    theoVal = w.eval()
    theoUnc = gaussian(w, params)
    print("Theoretisch berechneter Wert von w_g:")
    print(f"w = {theoVal}")
    print(f"∆w = {theoUnc}")
    print()

    rc = Var(6.40e-4, 0.12e-4, "RC")
    a = Var(0.994, 0.008, "a")
    factor = Pow(Sub(Const(2), Pow(a, -2)), 0.5)
    w = Mult(Div(Const(2 * math.pi), rc), factor)
    val = w.eval()
    params = [ rc, a ]
    unc = gaussian(w, params)
    evalPass(val, unc, theoVal, theoUnc, "Tiefpass")

    rc = Var(0.0018, 0.000118, "RC")
    a = Var(0.947, 0.02589, "a")
    factor = Pow(Sub(Pow(Div(a, Const(1 - 1 / 2 ** 0.5)), 2), Const(1)), 0.5)
    w = Mult(Div(Const(2 * math.pi), rc), factor)
    val = w.eval()
    params = [ rc, a ]
    unc = gaussian(w, params)
    evalPass(val, unc, theoVal, theoUnc, "Hochpass")

def evalPass(val, unc, theoVal, theoUnc, name):
    print(f"{name}:")
    print(f"w = {val}")
    print(f"∆w = {unc}")
    diff = abs(val - theoVal)
    print(f"Differenz zum theoretischen Wert: {diff}")
    print(f"Verhältnis aus dieser zur Summe der Unsicherheiten: {diff / (theoUnc + unc)}")

def tv3():
    print()
    print("--- Teilversuch 3 ---")

    l = Var(0.198, 0, "L")
    c = Var(10e-9, 0.05 * 10e-9, "C")
    f = Pow(Mult(Const(2 * math.pi), Pow(Mult(l, c), 0.5)), -1)
    params = [ l, c ]
    fVal = f.eval()
    fUnc = gaussian(f, params)
    print("Theoretischer Wert von f0:")
    print(f"f = {fVal}")
    print(f"∆f = {fUnc}")
    val = 3503.76
    unc = 0.10
    diff = abs(val - fVal)
    print(f"Differenz zum theoretischen Wert: {diff}")
    print(f"Verhältnis aus dieser zur Summe der Unsicherheiten: {diff / (unc + fUnc)}")

tv2()
tv3()
