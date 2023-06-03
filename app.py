from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import reservoir as rsv

from scipy.special import softmax

import numpy as np


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

    def start_server(self):
        print(f"Waiting for OSC messages on {self.ip}:{self.receive_port}")
        self.server.serve_forever()

    def create_reservoir_model(self):
        self.reservoir_model = rsv.ReservoirModel(self.reservoir_params, self.max_notes+1)



    @process_ableton_message
    def reset_reservoir(self, address, *args):
        print("Resetting reservoir")
        self.create_reservoir_model()

    @process_ableton_message
    def set_reservoir_parameter(self, address, *args):
        key = args[0]
        value = args[1]
        # Faire quelque chose avec les paramètres reçus
        print(f"key : {key}")
        print(f"Value: {value}")

        # update the value in param dictionary
        self.reservoir_params[key] = value

        if key == "units":
            # if the user wants to change the number of neurons, we have no choice but recreating the reservoir
            self.create_reservoir_model()
            print("Creating new reservoir with", value, "neurons")
        elif key == "sr":
            print("WARNING: can't change spectral radius yet")
        else:
            self.reservoir_model.reservoir.set_param(key, value)


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

        note_idx = self.reservoir_model.predict_next_note(nb_pressed_keys=len(self.note_set))

        # retrieve pressend notes
        note_list = list(self.note_set)
        note_list = sorted(note_list)

        print("note_idx", note_idx)
        if note_idx>0:
            print("note", note_list[note_idx-1])

        # index 0 is silence (no note played)
        if note_idx!=0:
            self.client.send_message("/send_note_to_ableton", note_list[note_idx-1])

if __name__ == "__main__":

    app = App()
    app.start_server()
    


