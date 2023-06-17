import matplotlib.pyplot as plt
from matplotlib import colors

plt.style.use("dark_background")
from sklearn.decomposition import PCA, IncrementalPCA


import numpy as np 

import matplotlib.animation as animation

def animate(i):
    # load data
    try:
        states_pca = np.load("tmp/states_pca.npy")
        pca_territories = np.load("tmp/pca_territories.npy", allow_pickle=True).item()

        if len(states_pca) < 2:
            pass

        else:
            scatters[1].set_offsets(states_pca)

            offset = 1

            ax.set_xlim(min(states_pca[:,0]-offset), max(states_pca[:,0])+offset)
            ax.set_ylim(min(states_pca[:,1]-offset), max(states_pca[:,1])+offset)

            alphas = np.linspace(0, .7, states_pca.shape[0])
            rgba_colors = np.ones((states_pca.shape[0], 4))
            rgba_colors[:, 3] = alphas

            rgba_colors[-1] = [1,0,0,1]

            scatters[1].set_color(rgba_colors)


            # PCA territories plot

            scatters[0].set_offsets(pca_territories["xys"])

            rgba_colors = np.array([colors.to_rgba(c) for c in ["blue", "red", "green", "yellow", "purple"]])
            rgba_colors = rgba_colors[pca_territories["pca_space_indices"]]
            rgba_colors[:,-1] = pca_territories["pca_space_probabilities"]
            scatters[0].set_color(rgba_colors)





    except Exception as e:
        print(e)


    return scatters,


if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)

    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])

    scatters = [
        ax.scatter([], [], s=1000),
        ax.scatter([],[], color="white"),
    ]

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                              interval=200, blit=False)

    # plt.title("Reservoir activations")
    plt.axis("off")
    
    plt.show()