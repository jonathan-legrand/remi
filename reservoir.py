from scipy.special import softmax
from reservoirpy.nodes import Reservoir, Input, Ridge
from reservoirpy.observables import spectral_radius
import numpy as np
import pickle



class ReservoirModel:
    def __init__(self, reservoir_params, max_notes, softmax_gain=1):
        self.create_model(reservoir_params, max_notes)
        self.softmax_gain = softmax_gain

    def create_model(self, reservoir_params, max_notes):
        """Creates two reservoirs a first one used for state updates and making predictions called `reservoir`
        and a second temporary one to initialize a random matrix to make projection from dim_out to size w
        want for note prediction, which we will use as a random readout
        """
        # step 1 base reservoir
        self.reservoir = Reservoir(**reservoir_params, input_dim=max_notes+1)
        self.reservoir.initialize()
        self.states = []
        self.outputs = [np.zeros(max_notes + 1)]



        # step 2 output reservoir
        _ = Reservoir(max_notes + 1, input_dim=reservoir_params["units"])
        # initiliaze
        _.initialize()
        # get matrix
        self.readout = _.Win#.toarray()


    def predict_next_note(self, nb_pressed_keys):
        print('these are the outputs', self.outputs[-1])

        # make a pred using last output as new input
        state = self.reservoir(self.outputs[-1])

        # compute output
        output = (state @ self.readout.T)[0]
        presoftmax = np.copy(output)
        print("output before softmax", presoftmax)
        output = softmax(self.softmax_gain * output[:nb_pressed_keys + 1])
        postsoftmax = np.copy(output)
        print("output after softmax", postsoftmax)
        choice = np.random.choice(range(nb_pressed_keys + 1), p=output)

        # create one-hot vector of the input (and output) shape with 1 at the index of the choice
        output = np.eye(self.readout.shape[0])[choice]

        # update logs
        self.outputs.append(output)
        self.outputs = self.outputs[-20:]
        self.states.append(state)
        self.states = self.states[-20:]

        # print saving file
        if len(self.states)>0:
            np.save('states.npy', np.array(self.states))

        # write info to display on GUI
        to_gui = {
            "presoftmax":list(presoftmax),
            "postsoftmax": list(postsoftmax),
            "sample": list(output),
            "sample_idx": np.argmax(output),
        }


        return np.argmax(output), to_gui

    def set_spectral_radius(self, sr):
        print("sr", sr, type(sr))
        print("W", type(self.reservoir.get_param("W")))
        _epsilon = 1e-8  # used to avoid division by zero when rescaling spectral radius
        current_sr = spectral_radius(self.reservoir.get_param("W"))
        if -_epsilon < current_sr < _epsilon:
            current_sr = _epsilon  # avoid div by zero exceptions.
        self.reservoir.set_param("W", self.reservoir.get_param("W") * sr / current_sr)
        print("Old sr", current_sr)
        print("New sr", spectral_radius(self.reservoir.get_param("W")))



