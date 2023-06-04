#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 12:39:52 2023

@author: nathan
"""

import tkinter as tk
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

class FloatEntry(tk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)
        
        # Create label
        self.label = tk.Label(self, text=label_text)
        self.label.pack(side="left")
        
        # Create entry
        self.entry = tk.Entry(self)
        self.entry.pack(side="left")
    
    def get_entry_value(self):
        return self.entry.get()
    
class Ware(tk.Tk):
    def __init__(self, ip, send_port, receive_port):
        super().__init__()
        
        # Création du dispatcher et ajout de la fonction de traitement
        self.dispatcher = dispatcher.Dispatcher()
        #self.dispatcher.map("/reservoir/set_reservoir", set_reservoir)
            
        # Création du serveur OSC
        #server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
        
        # Création du client OSC
        self.client = udp_client.SimpleUDPClient(ip, send_port)
        
        # Create a frame to hold the widgets
        self.frame = tk.Frame(self)
        self.frame.pack(anchor="w", padx=10, pady=10)  # Right alignment with padding
        
        # Création des boutons
        self.pitch_entry = FloatEntry(self.frame, "Pitch")
        self.velocity_entry = FloatEntry(self.frame, "Velocity")
        self.update_note_button = tk.Button(self.frame, text="Update note", command=self.update_note_clicked)
        self.key_entry = FloatEntry(self.frame, "key")
        self.value_entry = FloatEntry(self.frame, "value")
        self.set_reservoir_button = tk.Button(self.frame, text="Set reservoir", command=self.set_reservoir_clicked)
        self.get_button = tk.Button(self.frame, text="Get", command=self.get_button_clicked)
        
        # Placement des boutons dans le frame
        self.pitch_entry.pack(anchor="w")
        self.velocity_entry.pack(anchor="w")
        self.update_note_button.pack()
        self.key_entry.pack(anchor="w")
        self.value_entry.pack(anchor="w")
        self.set_reservoir_button.pack()
        self.get_button.pack()
    
    def update_note_clicked(self):
        pitch = int(self.pitch_entry.get_entry_value())
        velocity = int(self.velocity_entry.get_entry_value())
        address = "/reservoir/update_note"
        args = (pitch, velocity)  # Exemple d'argument
        self.client.send_message(address, args)
        
    def set_reservoir_clicked(self):
        # N 1 a 10000
        # lr 10-3 a 1
        # sr 10-3 1000
        # input_scaling 10-3 1000
        lr = self.key_entry.get_entry_value()
        sr = 1
        # Use lr and sr values for processing
        address = "/reservoir/set_reservoir"
        args = (lr, sr)  # Exemple d'argument
        self.client.send_message(address, args)
        
    def get_button_clicked(self):
        address = "/reservoir/get_note"
        args = ()  # Exemple d'argument
        self.client.send_message(address, args)
    
if __name__ == "__main__":
    # Adresse IP et port du destinataire OSC
    ip = "127.0.0.1"
    send_port = 9000
    receive_port = 8000
    # Création de la fenêtre principale
    window = Ware(ip, send_port, receive_port)
    # Démarrage de la boucle principale de la fenêtre
    window.mainloop()

