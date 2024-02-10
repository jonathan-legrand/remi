import matplotlib.pyplot as plt
# plt.style.use("dark_background")

import numpy as np 

import matplotlib.animation as animation
import pickle
import networkx as nx 
from scipy.special import softmax
import time

def create_graph(sim_matrix, state, seed, title="reservoir"):

    # Create a graph from the connectivity matrix
    G = nx.from_numpy_array(sim_matrix)
    np.random.seed(seed)
    # Get the positions of the nodes
    pos = nx.spring_layout(G, k = 0.5, seed=seed,weight='weight', )

    # Create the nodes
    node_x = [pos[i][0] for i in G.nodes()]
    node_y = [pos[i][1] for i in G.nodes()]

    sim_matrix = sim_matrix.toarray()
    thr = np.percentile(sim_matrix.flatten(), 95)
    thr_sim_matrix = sim_matrix
    thr_sim_matrix[thr_sim_matrix < thr] = 0
    # Add the edges
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_width = abs(thr_sim_matrix[edge[0], edge[1]])
        
        
        ax.plot([x0, x1], [y0, y1], color='black', linewidth=edge_width*0.5)

    #Add the nodes
    node_sizes = (abs(state) * 50).astype(int)
    scale_factor = 300
    # sizes = softmax(sizes[0])
    node_sizes = softmax(node_sizes)
    ax.scatter(node_x, node_y, s=node_sizes*scale_factor, c=[i for i in range(len(node_x))], cmap='turbo')

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
    except pickle.UnpicklingError:
        with open("tmp/reservoir_states.npy", "rb") as f:
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
        seed=1234
    )

if __name__=='__main__':
    fig, ax = plt.subplots(1, 1)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                            interval=200, blit=False)
    
    plt.show()