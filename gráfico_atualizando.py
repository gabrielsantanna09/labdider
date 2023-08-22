from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig = plt.figure()
axis = plt.axes(xlim=(0, 4), ylim=(-2, 2))
line, = axis.plot([], [], lw=3)
x_fiora = []

def init():
    line.set_data([], [])
    return line,


def animate(i):
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    x_fiora = x
    return line,


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=200, interval=20, blit=True)

print(x_fiora)
plt.show()

#anim.save('continuousSineWave.mp4',
 #           writer='ffmpeg', fps=30)