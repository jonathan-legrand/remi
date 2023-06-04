import matplotlib.pyplot as plt 

import numpy as np 

import matplotlib.animation as animation

def animate(i):
    # load data
    states = np.load("states.npy")
    states = np.squeeze(states)
    ax.set_ylim([-1,1])
    ax.set_xlim([0,states.shape[0]])    
    print("this is the shape", states.shape)

    to_use = min(states.shape[1], 20)

    if len(states.shape) == 1:
        pass

    # case where we restart
    elif states.shape[0] < len(datas[0]):
        for i in range(to_use):
            datas[i] += list(states[:, i])
            lines[i].set_data(np.arange(states.shape[0]), datas[i])

    else:
        for i in range(to_use):
            datas[i] += list(states[len(datas[i]):, i])
            lines[i].set_data(np.arange(states.shape[0]), datas[i])


    print("this is the shape", states.shape)
    print("arrange", np.arange(states.shape[0]).shape)

    # states_plot.set_data(np.arange(states.shape[0][j:]), states[j])

    # states_plot.set_data(np.tile(np.arange(states.shape[0])[None,j:], (20, 1)), states[j:,:20])

    return lines,


def init():
    for line in lines:
        line.set_data([],[])
    return lines


if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)
    print(ax)
    # ax.set_ylim([-1,1])
    # ax.set
    # states = np.load("states.npy")
    # states = np.squeeze(states)
    j = 0 

    lines = []
    datas = []

    for index in range(20):
        lobj = ax.plot([],[],lw=2)[0]
        lines.append(lobj)
        datas.append([])
    
    # states_plot, = ax.plot([], [])
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                              interval=25, blit=False)
    
    plt.show()