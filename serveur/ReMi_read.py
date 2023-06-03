from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Adresse IP et port du client "send.py"
send_ip = "127.0.0.1"
send_port = 8000

# Création du client OSC pour envoyer des messages à "send.py"
client = udp_client.SimpleUDPClient(send_ip, send_port)

note_set = {}

def process_message(func):
    def wrapper(*args):
        try:
            func(*args)
        except Exception as error:
            print(f"Error 400: Invalid Request : {error}")
    return wrapper

@process_message
def set_reservoir(address, *args):
    key = args[0]
    value = args[1]
    
    # Faire quelque chose avec les paramètres reçus
    print(f"key : {key}")
    print(f"Value: {value}")

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
    print("get note")
    client.send_message("/", note_set)

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

