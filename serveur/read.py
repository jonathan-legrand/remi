from pythonosc import dispatcher
from pythonosc import osc_server

# Fonction de traitement des messages OSC reçus
def process_message(address, *args):
    print(f"Reçu un message OSC à l'adresse {address} avec les arguments : {args}")

# Adresse IP et port sur lesquels écouter les messages OSC
ip = "127.0.0.1"
port = 9000

# Création du dispatcher et ajout de la fonction de traitement
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/example/address", process_message)

# Création du serveur OSC
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

# Démarrage du serveur
print(f"Écoute des messages OSC sur {ip}:{port}")
server.serve_forever()

