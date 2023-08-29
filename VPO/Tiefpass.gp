f(x) = a/sqrt(x * x * rc * rc + 1)
rc = 0.0001
a = 1
fit f(x) "Lowpass.csv" using 1:2 via rc, a
plot "Lowpass.csv" using 1:2 title "Messwerte" with linespoints ,\
    f(x) title "Fit"
set title "Tiefpass - Frequenz vs. Spannungsverhältnis"
set xlabel "Frequenz [Hz]"
set ylabel "Spannungsamplitude [V]"
replot