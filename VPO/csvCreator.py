def createPassCSV(f, uin, uout, name):
    with open(f"{name}.csv", "w") as file:
        file.write(f"#{name}\n")
        file.write("#Frequenz #U_in #U_out\n")
        for i in range(len(f)):
            file.write(f"{f[i] * 1000} {uout[i] / uin[i]}\n")
    file.close()


def createCSV(f, u, name):
    with open(f"{name}.csv", "w") as file:
        file.write(f"#{name}\n")
        file.write("#Frequenz #U\n")
        for i in range(len(f)):
            file.write(f"{f[i] * 1000} {u[i]}\n")
    file.close()


f = [
    0.10092,
    0.71522,
    1.00557,
    1.20928,
    1.80817,
    2.51731,
    3.00068,
    3.51339,
    4.02968,
    4.99631,
]
uin = [1.87, 1.87, 1.90, 1.89, 1.87, 1.89, 1.88, 1.89, 1.88, 1.90, 1.88]
uout = [1.86, 1.70, 1.57, 1.49, 1.22, 0.972, 0.862, 0.754, 0.674, 0.612, 0.550]
createPassCSV(f, uin, uout, "Lowpass")

f = [0.10117, 0.25061, 0.49757, 0.70856, 1.00676, 2.00239, 3.00003, 4.04029, 5.03989]
uin = [1.86, 1.88, 1.89, 1.89, 1.89, 1.88, 1.89, 1.88, 1.87]
uout = [0.123, 0.283, 0.560, 0.736, 0.968, 1.43, 1.63, 1.69, 1.77]
createPassCSV(f, uin, uout, "Highpass")

f = [
    3.00921,
    3.12156,
    3.20387,
    3.30987,
    3.39326,
    3.51814,
    3.60884,
    3.77003,
    3.81335,
    3.90383,
    4.00445,
    4.49326,
    5.00357,
    5.51334,
    6.01857,
]
u = [
    0.384,
    0.479,
    0.578,
    0.770,
    0.994,
    1.15,
    1.07,
    0.932,
    0.772,
    0.664,
    0.553,
    0.308,
    0.214,
    0.165,
    0.134,
]
createCSV(f, u, "Resonanzkurve")