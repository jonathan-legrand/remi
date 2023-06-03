from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import reservoir as rsv

from scipy.special import softmax

import numpy as np
# Adresse IP et port du client "send.py"
send_ip = "127.0.0.1"
send_port = 8000

# Création du client OSC pour envoyer des messages à "send.py"
client = udp_client.SimpleUDPClient(send_ip, send_port)

note_set = set()
param = {}

global reservoir
global w_in
global states
global to_press

def set_up():
    reservoir, W_in = rsv.create_model(100)
    states = np.zeros((10000, 20))
    to_press = np.zeros((1000, 9))

    return reservoir, W_in, states, to_press


reservoir, w_in, states, to_press = set_up()

i = 0 

def process_message(func):
    def wrapper(*args):
        func(*args)
        # try:
        #     func(*args)
        # except Exception as error:
        #     print(f"Error 400: Invalid Request : {error}")
    return wrapper

@process_message
def set_reservoir(address, *args):
    key = args[0]
    value = args[1]    
    # Faire quelque chose avec les paramètres reçus
    print(f"key : {key}")
    print(f"Value: {value}")
    if key == "N":
        reservoir, w_in = rsv.create_model(value)

    else:
        param[key] = value
        reservoir.set_param(key, value)


@process_message
def update_note(address, *args):
    pitch = args[0]
    velocity = args[1]
    
    if velocity == 0:
        note_set.remove(pitch)
    else :
        note_set.add(pitch)
    
    # Faire quelque chose avec les paramètres reçus
    print(f"Pitch : {pitch}")
    print(f"Velocity : {velocity}")
    print(f"Note set : {note_set}")

@process_message
def get_note(address, *args):

    print("note_set", note_set)
    # retrieve pressend notes 
    list_note = list(note_set)
    nb_pressed_keys = len(note_set)
    sorted_notes = sorted(list_note)
    # make a pred 
    state = reservoir(to_press[i])
    # dim reduction 
    reduced = state@w_in.T
    probs = softmax(reduced[0,:nb_pressed_keys+1])
    press = np.random.choice(np.arange(nb_pressed_keys+1), p=probs)

    # update logs 
    states[i] = state
    to_press[i][press] = 1

    print("press", press)
    print("list_note", list_note)
    print("press-1", press-1)

    if press!=0:
        client.send_message("/send_note_to_ableton", list_note[press-1])

if __name__ == "__main__":
    # Adresse IP et port sur lesquels écouter les messages OSC
    ip = "127.0.0.1"
    port = 9000
    
    # Création du dispatcher et ajout de la fonction de traitement
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/reservoir/set_reservoir", set_reservoir)
    dispatcher.map("/reservoir/update_note", update_note)
    dispatcher.map("/reservoir/get_note", get_note)
    
    # Création du serveur OSC
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    
    # Démarrage du serveur
    print(f"Écoute des messages OSC sur {ip}:{port}")
    server.serve_forever()

