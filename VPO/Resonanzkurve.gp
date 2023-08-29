f(x) = a / (2 * sigma) * exp(-abs(x - mu) / sigma)
a = 1000
mu = 3500
sigma = 1000
clear
fit f(x) "Resonanzkurve.csv" using 1:2 via a, mu, sigma
plot "Resonanzkurve.csv" using 1:2 title "Messwerte" with linespoints, f(x) title "Fit"
set title "Resonanzkurve Serienschwingkreis"
set xlabel "Frequenz [Hz]"
set ylabel "Spannungsamplitude [V]"
replot