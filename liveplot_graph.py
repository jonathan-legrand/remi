import matplotlib.pyplot as plt
plt.style.use("dark_background")

import numpy as np 

import matplotlib.animation as animation
import pickle
import networkx as nx 


def animate(i, pos):
    ax.clear()
    G = nx.from_numpy_matrix(pickle.load(open('tmp/W_res', 'rb')))
    nx.draw(G, ax=ax)

if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)

    G = nx.from_numpy_matrix(pickle.load(open('tmp/W_res', 'rb')))
    pos = nx.spring_layout(G)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),fargs=([pos]),
                            interval=200, blit=False)
    
    plt.show()

