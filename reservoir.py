import os

from scipy.special import softmax
from reservoirpy.nodes import Reservoir, Input, Ridge
from reservoirpy.observables import spectral_radius
import numpy as np
import pickle

from sklearn.decomposition import PCA, IncrementalPCA




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

        self.compute_color_preferences()

    def compute_color_preferences(self, softmax_gain=300000):
        print(self.readout.shape)
        readout_arr = self.readout.toarray()
        readout_softmax = softmax(readout_arr * softmax_gain, axis=0)

        # for i in range(20):
        #     print(readout_softmax[:,i])

        self.color_preferences_indices = np.argmax(readout_softmax, axis=0)
        self.color_preferences_strength = np.max(readout_softmax, axis=0)

        # self.color_preferences_strength

        if not os.path.exists("tmp/"):
            os.makedirs("tmp/")
        np.save('tmp/color_preferences_indices.npy', self.color_preferences_indices)
        np.save('tmp/color_preferences_strength.npy', self.color_preferences_strength)


    def predict_next_note(self, nb_pressed_keys):
        print('these are the outputs', self.outputs[-1])

        # make a pred using last output as new input
        state = self.reservoir(self.outputs[-1])

        output, presoftmax, postsoftmax, choice = self.predict_note_from_state(state, nb_pressed_keys)

        # update logs
        self.outputs.append(output)
        self.outputs = self.outputs[-30:]
        self.states.append(state[0])
        self.states = self.states[-30:]

        # print saving file
        if len(self.states)>2:

            states_pca = self.compute_pca()
            xys, pca_space_indices, pca_space_probabilities = self.projections_notes(nb_pressed_keys)

            if not os.path.exists("tmp/"):
                os.makedirs("tmp/")
            np.save('tmp/states.npy', np.array(self.states))
            np.save('tmp/states_pca.npy', states_pca)
            np.save('tmp/nb_pressed_keys.npy', nb_pressed_keys)
            np.save('tmp/pca_territories.npy', {
                "xys":xys,
                "pca_space_indices":pca_space_indices,
                "pca_space_probabilities":pca_space_probabilities
            }, allow_pickle=True)

        # write info to display on GUI
        to_gui = {
            "presoftmax":list(presoftmax),
            "postsoftmax": list(postsoftmax),
            "sample": list(output),
            "sample_idx": np.argmax(output),
        }


        return np.argmax(output), to_gui

    def predict_note_from_state(self, state, nb_pressed_keys):
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

        return output, presoftmax, postsoftmax, choice

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

    def compute_pca(self):
        self.pca = PCA(n_components=2, random_state=1)
        self.states_pca = self.pca.fit_transform(self.states)
        return self.states_pca

    def projections_notes(self, nb_pressed_keys, granularity_num=10):
        self.xlim_pca = (min(self.states_pca[:, 0]), max(self.states_pca[:, 0]))
        self.ylim_pca = (min(self.states_pca[:, 1]), max(self.states_pca[:, 1]))

        xs = np.linspace(self.xlim_pca[0], self.xlim_pca[1], granularity_num)
        ys = np.linspace(self.ylim_pca[0], self.ylim_pca[1], granularity_num)
        indices = []
        probabilities = []

        xys = np.transpose([np.tile(xs, len(ys)), np.repeat(ys, len(xs))])

        states = self.pca.inverse_transform(xys)

        print("states", states.shape)

        for s in states:
            output, presoftmax, postsoftmax, choice = self.predict_note_from_state(s[None,:], nb_pressed_keys)
            postsoftmax_argmax = np.argmax(postsoftmax)
            indices.append(postsoftmax_argmax)
            probabilities.append(postsoftmax[postsoftmax_argmax])

        return xys, np.array(indices), np.array(probabilities)


    def set_input_scaling(self, new_input_scaling, old_input_scaling):
        Win = self.reservoir.get_param("Win")
        self.reservoir.set_param("Win", Win / old_input_scaling * new_input_scaling)



