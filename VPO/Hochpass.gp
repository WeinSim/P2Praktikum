f(x) = 1 - a / sqrt(x * x * rc * rc + 1)
rc = 0.001
a = 1
fit f(x) "Highpass.csv" using 1:2 via rc, a
plot "Highpass.csv" using 1:2 title "Messwerte" with linespoints ,\
    f(x) title "Fit"
set title "Highpass - Frequenz vs. Spannungsverhältnis"
set xlabel "Frequenz [Hz]"
set ylabel "Spannungsamplitude [V]"
replot