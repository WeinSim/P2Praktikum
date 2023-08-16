from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import math
from LinRegUncertainty import *

x = np.arange(0, 10, 1)
y = []
for i in range(len(x)):
    y.append(2 * x[i])
    y[i] += 0.5 * (rd.random() - 0.5)

print(x)
print(y)
coefs, cov = np.polyfit(x, y, 1, cov='True')
print("Coefs:")
print(coefs)
print("Covariance matrix:")
print(cov)

dsC = math.sqrt(cov[0][0])
dy0C = math.sqrt(cov[1][1])
(dsL, dy0L) = linRegUncertainty(x, y, coefs)
print("Covariance matrix uncertainties:")
print(f"d slope = {dsC}")
print(f"d y0 = {dy0C}")
print("Old uncertainties:")
print(f"d slope = {dsL}")
print(f"d y0 = {dy0L}")

pp = PdfPages("Test.pdf")
plt.figure()
plt.clf()
plt.plot(x, y, 'bo')
yfit = np.polyval(coefs, x)
dy = dy0C
plt.plot(x, yfit, 'r-')
plt.plot(x, yfit + dy, 'r--', linewidth='0.5')
plt.plot(x, yfit - dy, 'r--', linewidth='0.5')

pp.savefig()
pp.close()
