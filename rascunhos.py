from matplotlib.pyplot import figure, show
from numpy import arange, sin, pi

t = arange(0, 100, 1)
y = [i for i in range(100)]
for i in range(10):
	y[i] = i**2
for i in range(10,30):
	y[i] = 100
fig = figure(1)
ax1 = fig.add_subplot(111)
ax1.plot(t, y)
ax1.set_ylabel('Número de ações')
ax1.set_xlabel('Tempo')
ax1.set_title('Ações distribuídas no tempo')
show()