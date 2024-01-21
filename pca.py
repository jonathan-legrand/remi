import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse
from matplotlib import colors

from cmcrameri import cm


plt.style.use("dark_background")


import numpy as np 

import matplotlib.animation as animation

ROTATE = True #Rotate PCA or not

def animate(i):
    # load data
    try:
        states_pca = np.load("tmp/states_pca.npy")
        pca_territories = np.load("tmp/pca_territories.npy", allow_pickle=True).item()

        if len(states_pca) < 2:
            pass

        else:

            # Sometimes there is a discontinuous flip in PCA. We try to avoid that by flipping new PCA if it makes it closer to previous PCA
            old_states_pca = np.array(trajectory_line.get_data()).T

            best = 0

            print(len(old_states_pca), len(states_pca))

            if len(old_states_pca) in [len(states_pca) - 1, len(states_pca)]:

                if ROTATE:
                    states_pca_flipped_x = np.copy(states_pca)
                    states_pca_flipped_x[:,0] = -states_pca_flipped_x[:,0]
                    states_pca_flipped_y = np.copy(states_pca)
                    states_pca_flipped_y[:,1] = -states_pca_flipped_y[:,1]
                    states_pca_flipped_xy = np.copy(states_pca)
                    states_pca_flipped_xy = -states_pca_flipped_xy

                    diff_orig = mse(old_states_pca, states_pca[-len(old_states_pca):])
                    diff_flipped_x = mse(old_states_pca, states_pca_flipped_x[-len(old_states_pca):])
                    diff_flipped_y = mse(old_states_pca, states_pca_flipped_y[-len(old_states_pca):])
                    diff_flipped_xy = mse(old_states_pca, states_pca_flipped_xy[-len(old_states_pca):])

                    best = np.argmin([diff_orig, diff_flipped_x, diff_flipped_y, diff_flipped_xy])

                
                    if best == 1:
                        states_pca = states_pca_flipped_x
                        pca_territories["xys"][:,0] = -pca_territories["xys"][:,0]

                    if best == 2:
                        states_pca = states_pca_flipped_y
                        pca_territories["xys"][:, 1] = -pca_territories["xys"][:, 1]
                    if best == 3:
                        states_pca = states_pca_flipped_xy
                        pca_territories["xys"] = -pca_territories["xys"]

            trajectory_line.set_data(states_pca[:,0], states_pca[:,1])
            trajectory_scatter.set_offsets(states_pca)

            offset = 1

            # test size window
            ax.set_xlim(min(states_pca[:,0]-offset), max(states_pca[:,0])+offset)
            ax.set_ylim(min(states_pca[:,1]-offset), max(states_pca[:,1])+offset)

            alphas = np.linspace(0, 1, states_pca.shape[0])
            rgba_colors = np.ones((states_pca.shape[0], 4))
            rgba_colors[:, 3] = alphas

            rgba_colors[-1] = [1,0,0,1]

            trajectory_scatter.set_color(rgba_colors)


            # PCA territories plot

            territory_scatter.set_offsets(pca_territories["xys"])

            # rgba_colors = np.array([colors.to_rgba(c) for c in ["blue", "red", "green", "purple", "yellow"]])
            rgba_colors = np.array([cm.hawaii(i/8) for i in range(9)])
            rgba_colors = rgba_colors[pca_territories["pca_space_indices"]]
            rgba_colors[:,-1] = pca_territories["pca_space_probabilities"] * 1
            territory_scatter.set_color(rgba_colors)

            granularity_num = int(pca_territories["xys"].shape[0]**(1/2))
            print("granularity_num", granularity_num)

            im = rgba_colors.reshape(granularity_num,granularity_num,-1) * 1

            if ROTATE:
                if best==1:
                    im = im[:,::-1]
                elif best==2:
                    im = im[::-1,:]
                elif best==3:
                    im = im[::-1,::-1]

            xlim = (np.min(states_pca[:,0]), np.max(states_pca[:,0]))
            ylim = (np.min(states_pca[:,1]), np.max(states_pca[:,1]))
            x_offset = (xlim[1]-xlim[0]) / (granularity_num*2)
            y_offset = (ylim[1]-ylim[0]) / (granularity_num*2)

            territory_imshow.set_array(im)
            territory_imshow.set_extent([
                                            xlim[0] - x_offset,
                                            xlim[1] + x_offset,
                                            ylim[0] - y_offset,
                                            ylim[1] + y_offset
            ])



            print("best", best)

    except Exception as e:
        print(e)


    return trajectory_scatter, trajectory_line, territory_imshow, territory_scatter


if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)

    # test size window
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])

    territory_imshow = ax.imshow(np.random.random((5,5)), interpolation="lanczos", origin="lower")
    territory_scatter = ax.scatter([], [], s=100)
    trajectory_line, = ax.plot([], [], lw=.3, color="white")#, alpha=0)
    trajectory_scatter = ax.scatter([],[], color="white")#, s=0)


    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                              interval=200, blit=False)

    # plt.title("Reservoir activations")
    plt.axis("off")
    plt.show()