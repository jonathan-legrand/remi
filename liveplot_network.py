import matplotlib.pyplot as plt
# plt.style.use("dark_background")

import numpy as np 

import matplotlib.animation as animation
import pickle
import networkx as nx 
from scipy.special import softmax
import time

# def sigmoid(x):
#     return 1 / (1 + np.exp(-x))

def create_graph(
        sim_matrix,
        state, 
        seed, 
        title="reservoir", 
        scale_factor=25, 
        edge_scaling=1
    ):

    # Create a graph from the connectivity matrix
    G = nx.from_numpy_array(sim_matrix)
    np.random.seed(seed)
    # Get the positions of the nodes
    pos = nx.spring_layout(G, k = 0.5, seed=seed,weight='weight', )

    # Create the nodes
    # print(G.nodes())
    stacked_pos = np.stack(tuple(pos.values()))
    node_x = stacked_pos[:,0]
    node_y = stacked_pos[:,1]
    sim_matrix = sim_matrix.toarray()
    thr = np.percentile(sim_matrix.flatten(), 0)
    thr_sim_matrix = sim_matrix
    thr_sim_matrix[thr_sim_matrix < thr] = 0
    thr_sim_matrix = softmax(thr_sim_matrix, axis=1)
    # Add the edges
    indices_nodes = np.stack(G.edges())
    # print(pos[indices_nodes[0]])
    # TODO: optimisation by removing the loop (nightmare.com)
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        # TODO: handle negatives
        edge_width = abs(thr_sim_matrix[edge[0], edge[1]])
        # TODO: bipolar cbar for negative/positive values
        ax.plot([x0, x1], [y0, y1], color='black', linewidth=edge_width*edge_scaling)


    #Add the nodes
    # node_sizes = (abs(state) * 50).astype(int)
    # displace values to avoid < 0 (tanh activation function)
    node_sizes = (state + 1) * scale_factor
    print(node_sizes)
    ax.scatter(node_x, node_y, s=node_sizes, c=[i for i in range(len(node_x))], cmap='turbo')

    # Update the layout
    # Update the layout
    ax.set_title(title)
    ax.axis('off')  # No axis

    return fig, ax 


def animate(i):
    
    ax.clear()
    #states = np.load("tmp/states.npy", allow_pickle=True)
    try:
        with open("tmp/reservoir_states.npy", "rb") as f:
            states = np.load(f, allow_pickle=True)
    except ValueError:
        time.sleep(0.01)
        with open("tmp/reservoir_states.npy", "rb") as f:
            states = np.load(f, allow_pickle=True)

    except pickle.UnpicklingError as error:
        with open("tmp/reservoir_states.npy", "rb") as f:
            print(f' {error} EXCEPTION CATCHED!!!!!!!!!!!')
            states = np.load(f, allow_pickle=False)
            
    # load the "tmp/W_res.pkl" file with pickle
    try:
        with open("tmp/W_res.pkl", "rb") as f:
            W_res = pickle.load(f)
    except EOFError:
        time.sleep(0.01)
        with open("tmp/W_res.pkl", "rb") as f:
            W_res = pickle.load(f)

        

    return create_graph(
        W_res,
        states,
        seed=1234,
        scale_factor=1000,
        edge_scaling=1
    )

if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                            interval=200, blit=False)
    
    plt.show()