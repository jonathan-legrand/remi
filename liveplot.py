import matplotlib.pyplot as plt
plt.style.use("dark_background")

import pickle

from cmcrameri import cm


import numpy as np 

import matplotlib.animation as animation

def animate(i):
    # load data
    try:
        states = np.load("tmp/states.npy")
        ax[0].set_ylim([-1, 1])
        ax[0].set_xlim([0, states.shape[0]])

        if len(states) > 0:

            color_preferences_indices = np.load("tmp/color_preferences_indices.npy")
            color_preferences_strength = np.load("tmp/color_preferences_strength.npy")
            n_choices = np.load("tmp/nb_pressed_keys.npy") + 1

            color_preferences_strength = color_preferences_strength[np.where(color_preferences_indices < n_choices)]
            color_preferences_indices = color_preferences_indices[np.where(color_preferences_indices < n_choices)]

            states = states[:,np.where(color_preferences_indices < n_choices)][:,0,:]

            strength_indices = color_preferences_strength.argsort()[::-1]
            color_preferences_strength = color_preferences_strength[strength_indices]
            color_preferences_indices = color_preferences_indices[strength_indices]
            states = states[:,strength_indices]

            to_show = min(states.shape[1], 100)
            for i in range(to_show):
                lines[i].set_alpha(color_preferences_strength[i])
                lines[i].set_color(cm.hawaii(color_preferences_indices[i]/8))
                lines[i].set_data(np.arange(states.shape[0]), states[:, i])


            # update scatter on right
            with open('tmp/to_gui.obj', 'rb') as fp:
                to_gui = pickle.load(fp)
                postsoftmax = to_gui["postsoftmax"]
                print([[0]*len(postsoftmax), postsoftmax])
                scatter.set_offsets([[0,p] for p in postsoftmax])
                scatter.set_color(cm.hawaii([i/8 for i in range(len(postsoftmax))]))

    except Exception as e:
        print(e)


    return lines, scatter,


def init():
    for line in lines:
        line.set_data([],[])
    return lines


if __name__=='__main__':
    fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios':[10,1]})

    lines = []

    for index in range(100):
        lobj = ax[0].plot([],[],lw=1)[0]
        lines.append(lobj)

    scatter = ax[1].scatter([], [], s=500, alpha=.7)

    ax[0].set_axis_off()
    ax[1].set_axis_off()

    ax[1].set_ylim([0,1])

    # states_plot, = ax.plot([], [])
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                              interval=200, blit=False)

    # plt.title("Reservoir activations")

    plt.show()