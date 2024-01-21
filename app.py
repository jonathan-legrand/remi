from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import reservoir as rsv
from constants import *

from scipy.special import softmax
import pickle

import numpy as np

def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    assert octave in OCTAVES, errors['notes']
    assert 0 <= number <= 127, errors['notes']
    note = NOTES[number % NOTES_IN_OCTAVE]

    return note, octave

def process_ableton_message(func):
    def wrapper(*args):
        func(*args)
        # try:
        #     func(*args)
        # except Exception as error:
        #     print(f"Error 400: Invalid Request : {error}")

    return wrapper

class App:
    def __init__(self, max_notes=8):

        self.ip = "127.0.0.1"
        self.send_port = 8000
        self.receive_port = 9000

        self.client = udp_client.SimpleUDPClient(self.ip, self.send_port)

        self.note_set = set()
        self.max_notes = max_notes

        self.reservoir_params = {
            "units": 100,
            "lr": 1.0,
            "sr": 1.0,
            "input_scaling": 1.0,
            "noise_rc": 0.0,
            "noise_in": 0.0,
        }

        self.create_reservoir_model()

        print(self.reservoir_model.reservoir.input_scaling)

        # Création du dispatcher et ajout de la fonction de traitement
        self.dp = dispatcher.Dispatcher()
        self.dp.map("/reservoir/reset_reservoir", self.reset_reservoir)
        self.dp.map("/reservoir/set_reservoir_parameter", self.set_reservoir_parameter)
        self.dp.map("/reservoir/update_note", self.update_note)
        self.dp.map("/reservoir/get_note", self.get_note)

        

        # Création du serveur OSC
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.receive_port), self.dp)

        self.parameter_changes_to_apply = {}

    def start_server(self):
        print(f"Waiting for OSC messages on {self.ip}:{self.receive_port}")
        self.server.serve_forever()

    def create_reservoir_model(self):
        self.reservoir_model = rsv.ReservoirModel(self.reservoir_params, self.max_notes)



    @process_ableton_message
    def reset_reservoir(self, address, *args):
        print("Resetting reservoir")
        self.reservoir_model.create_model(self.reservoir_params, self.max_notes)

    @process_ableton_message
    def set_reservoir_parameter(self, address, *args):
        self.parameter_changes_to_apply[args[0]] = args[1]

    def apply_reservoir_parameters(self):
        for key, value in self.parameter_changes_to_apply.items():
            # Faire quelque chose avec les paramètres reçus
            print(f"key : {key}")
            print(f"Value: {value}")

            if key == "input_scaling":
                old_input_scaling = self.reservoir_params["input_scaling"]

            # update the value in param dictionary
            self.reservoir_params[key] = value

            if key == "units":

                # if the user wants to change the number of neurons, we have no choice but recreating the reservoir
                self.reservoir_model.create_model(self.reservoir_params, self.max_notes)
                print("Creating new reservoir with", value, "neurons")
            elif key == "sr":
                self.reservoir_model.set_spectral_radius(value)
            elif key == "softmax_gain":
                self.reservoir_model.softmax_gain = value
            elif key == "input_scaling":
                self.reservoir_model.set_input_scaling(value, old_input_scaling)
            else:
                self.reservoir_model.reservoir.set_param(key, value)

        self.parameter_changes_to_apply = {}



    @process_ableton_message
    def update_note(self, address, *args):
        pitch = args[0]

        velocity = args[1]

        # the key was released, we remove the note from the note options
        if velocity == 0:
            self.note_set.remove(pitch)
        # the key was pressed, we add the note to the note options
        else :
            self.note_set.add(pitch)

        print("New note set", self.note_set)

    @process_ableton_message
    def get_note(self, address, *args):

        self.apply_reservoir_parameters()
        
        note_idx, to_gui = self.reservoir_model.predict_next_note(nb_pressed_keys=len(self.note_set))

        
        # retrieve pressend notes
        note_list = list(self.note_set)
        note_list = sorted(note_list)

        to_gui["sorted_notes"] = ["--"] + [number_to_note(n)[0]+str(number_to_note(n)[1]) for n in note_list]
        print("sorted_notes", to_gui["sorted_notes"])

        print("note_idx", note_idx)

        if note_idx>0:
            print("note", note_list[note_idx-1], number_to_note(note_list[note_idx-1]))

        with open('tmp/to_gui.obj', 'wb') as fp:
            pickle.dump(to_gui, fp)

        # debug xav
        print("whole list", note_list)
        # print("current note",note_list[note_idx-1])

        # index 0 is silence (no note played)
        if note_idx!=0:
            self.client.send_message("/send_note_to_ableton", note_list[note_idx-1])
        else: #DEBUG: xav tries to debug that ableton live never stops playing the last note
            #self.client.send_message("/send_note_to_ableton", [])
            pass
            

if __name__ == "__main__":
    app = App()
    app.start_server()
    


