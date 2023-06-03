from pythonosc import udp_client

# Adresse IP et port du destinataire OSC
ip = "127.0.0.1"
port = 9000

# Création du client OSC
client = udp_client.SimpleUDPClient(ip, port)

# Envoi du message OSC
address = "/example/address"
args = 12345  # Exemple d'argument
client.send_message(address, args)

