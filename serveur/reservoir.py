from scipy.special import softmax
from reservoirpy.nodes import Reservoir, Input, Ridge
import numpy as np


def create_model(res_size:int, lr:float=0.5, sr:float=0.9):
    """Creates two reservoirs a first used for state updates and making predictions called `reservoir`
    and a second called `res_out` to initialize a random matrix to make projection from dim_out to size w
    want for key prediction

    Args:
        res_size (int): size of adjacency matrix for reservoir
        lr (float, optional): Leaking rate. Defaults to 0.5.
        sr (float, optional): Spectral radius. Defaults to 0.9.
    """
    # step 1 base reservoir
    reservoir = Reservoir(20, lr=0.5, sr=0.9)

    # step 2 output reservoir 
    _ = Reservoir(5, input_dim=20)
    # initiliaze 
    _.initialize()
    # get matrix 
    W_in = _.Win.toarray()

    return reservoir, W_in

def make_prediction(X:np.array, reservoir:Reservoir, W_in:np.array):
    """
    Returns a prediction for next key to play

    Args:
        X (np.array): timeseries use for prediction
        reservoir (Reservoir): reservoir
        W_in (np.array): projection matrix
    """ 
    # predict next state 
    state =  reservoir(X)

    # dimensionality reduction 
    probas = softmax(state@W_in.T)

    # return in one hot encoding 
    key = np.random.choice(np.arange(5), p=probas[0])

    return key 

if __name__=='__main__':

    # init a big array for buffer
    values = np.zeros((10000, 5))
    values[0][np.random.choice(np.arange(5))] = 1
    reservoir, w_in = create_model(100, lr=0.5, sr=0.9)
    i = 0
    while True:
        key = make_prediction(values[i], reservoir, w_in)
        values[i+1][key] = 1
        i += 1 


    
    
    

