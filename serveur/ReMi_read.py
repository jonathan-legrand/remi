from pythonosc import dispatcher
from pythonosc import osc_server

# Adresse IP et port sur lesquels écouter les messages OSC
ip = "127.0.0.1"
port = 9000

def new_reservoir(*args):
    print(args)
    taille = args[0]
    leak_rate = args[1]
    spectral_radius = args[2]
    input_scaling = args[3]
    
    # Faire quelque chose avec les paramètres reçus
    print(f"Taille : {taille}")
    print(f"Leak Rate : {leak_rate}")
    print(f"Spectral Radius : {spectral_radius}")
    print(f"Input Scaling : {input_scaling}") 

def reset_reservoir(*args):
    print("Reçu un message OSC pour réinitialiser")

def get_reservoir(*args):
    print("get note")
    
links = {
"/reservoir/new" : new_reservoir,
"/reservoir/reset" : reset_reservoir,
"/reservoir/get" : get_reservoir,
}

def process_message(address, *args):
    not_find = True
    for l in links:
        if (l == address):
            try :
                not_find = False
                links[l](args)
                break;
            except Exception as error:
                print(f"Error 400: Invalid Request : {error}")
    if not_find :
        print(f"Adresse OSC non reconnue : {address}")

# Création du dispatcher et ajout de la fonction de traitement
dispatcher = dispatcher.Dispatcher()
for l in links:
    dispatcher.map(l, process_message)

# Création du serveur OSC
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

# Démarrage du serveur
print(f"Écoute des messages OSC sur {ip}:{port}")
server.serve_forever()
