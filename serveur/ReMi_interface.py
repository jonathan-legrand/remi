#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 12:39:52 2023

@author: nathan
"""

import tkinter as tk
from pythonosc import udp_client

# Adresse IP et port du destinataire OSC
ip = "127.0.0.1"
port = 9000

# Création du client OSC
client = udp_client.SimpleUDPClient(ip, port)

def new_button_clicked(taille = 100, lr=0.5, sr=0.9, ic=0.7):
    # Envoi du message OSC
    address = "/reservoir/new"
    args = (taille, lr, sr, ic)  # Exemple d'argument
    client.send_message(address, args)

def reset_button_clicked():
    # Envoi du message OSC
    address = "/reservoir/reset"
    args = 12345  # Exemple d'argument
    client.send_message(address, args)

def get_button_clicked():
    # Envoi du message OSC
    address = "/reservoir/get"
    args = 12345  # Exemple d'argument
    client.send_message(address, args)

# Création de la fenêtre principale
window = tk.Tk()

# Création des boutons
new_button = tk.Button(window, text="New", command=new_button_clicked)
reset_button = tk.Button(window, text="Reset", command=reset_button_clicked)
get_button = tk.Button(window, text="Get", command=get_button_clicked)

# Placement des boutons dans la fenêtre
new_button.pack()
reset_button.pack()
get_button.pack()

# Démarrage de la boucle principale de la fenêtre
window.mainloop()