#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 12:39:52 2023

@author: nathan
"""

import tkinter as tk
import multiprocessing as mp
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

import pickle

TEXT_SIZE = 15
FONT = font=("Arial", TEXT_SIZE)

def round_list(numbers):
    rounded_numbers = [round(num, 3) for num in numbers]
    return rounded_numbers

def process_ableton_message(func):
    def wrapper(*args):
        try:
            func(*args)
        except Exception as error:
            print(f"Error 400: Invalid Request : {error}")

    return wrapper

class FloatEntry(tk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)
        
        # Create label
        self.label = tk.Label(self, text=label_text, font=FONT)
        self.label.pack(side="left")
        
        # Create entry
        self.entry = tk.Entry(self)
        self.entry.pack(side="left")
    
    def get_entry_value(self):
        return self.entry.get()
    
class VerticalListFrame(tk.Frame):
    def __init__(self, parent, numbers, bd=0, relief="solid"):
        super().__init__(parent, bd=1, relief="solid")
        self.bd = bd
        self.relief = relief
        self.label_list = []
        
        for number in numbers:
            label = tk.Label(self, text=str(number), bd=self.bd, relief=self.relief, font = FONT)
            self.label_list.append(label)
            label.pack(side="top", padx=5, pady=5)
            
    def refresh(self, vector:list, selected_index = None):
        for i, l in enumerate(self.label_list):
            if i < len(vector):
                l.config(text=str(vector[i]))
            else :
                l.config(text="None")
            l.config(fg=("black", "pale green")[i == selected_index])
        
class VectorFrame(tk.Frame):
    def __init__(self, parent, name, numbers, bd=0, relief="solid"):
        super().__init__(parent)
            
        # Création de la VerticalListFrame pour afficher les nombres
        self.vertical_list = VerticalListFrame(self, numbers, bd=bd, relief=relief)
        self.vertical_list.pack(side="top", pady=5)

        # Création du label pour afficher le nom
        self.name_label = tk.Label(self, text=name, font=FONT)
        self.name_label.pack(side="top", pady=5)
        
    def refresh(self, new_vector, selected_index = None):
        self.vertical_list.refresh(new_vector, selected_index=selected_index)

class ArrowFrame(tk.Frame):
    def __init__(self, parent, direction):
        super().__init__(parent)
        self.direction = direction
        self.canvas = tk.Canvas(self, width=50, height=50)
        self.canvas.pack()
        self.draw_arrow()

    def draw_arrow(self):
        if self.direction == "up":
            self.canvas.create_polygon(25, 0, 0, 50, 50, 50, fill="black")
        elif self.direction == "down":
            self.canvas.create_polygon(25, 50, 0, 0, 50, 0, fill="black")
        elif self.direction == "left":
            self.canvas.create_polygon(0, 25, 50, 0, 50, 50, fill="black")
        elif self.direction == "right":
            self.canvas.create_polygon(50, 25, 0, 0, 0, 50, fill="black")
            
class ReservoirFrame(tk.Frame):
    def __init__(self, parent, n=9):
        super().__init__(parent)
        numbers = [0 for i in range(n)]
        notes = [' ' for i in range(n)]
        self.frame1 = VectorFrame(self, "presoftmax", numbers)
        self.frame2 = VectorFrame(self, "postsoftmax", numbers)
        self.frame3 = VectorFrame(self, "sample", numbers)
        self.frame4 = VectorFrame(self, "Sorted notes", notes, bd = 1)
        self.arrow1 = ArrowFrame(self, "right")
        self.arrow2 = ArrowFrame(self, "right")
        self.arrow3 = ArrowFrame(self, "right")

        self.frame1.pack(side="left")
        self.arrow1.pack(side="left")
        self.frame2.pack(side="left")
        self.arrow2.pack(side="left")
        self.frame3.pack(side="left")
        self.arrow3.pack(side="left")
        self.frame4.pack(side="left")
        
    def refresh(self, presoftmax, postsoftmax, sample, sorted_notes, sample_idx):
        self.frame1.refresh(presoftmax)
        self.frame2.refresh(postsoftmax)
        self.frame3.refresh(sample)
        self.frame4.refresh(sorted_notes, sample_idx)
    
class Ware(tk.Tk):
    def __init__(self, ip, send_port):
        super().__init__()
              
        
        self.note_liste = []
        # Création du client OSC
        self.client = udp_client.SimpleUDPClient(ip, send_port)
        
        # Create a frame to hold the widgets
        self.frame = tk.Frame(self)
        # self.frame.pack(anchor="w", padx=10, pady=10)  # Right alignment with padding
        
        
        self.variable = tk.StringVar()
        self.variable.set("Waitting note...")
        
        # Création des boutons
        self.pitch_entry = FloatEntry(self.frame, "Pitch")
        self.velocity_entry = FloatEntry(self.frame, "Velocity")
        self.update_note_button = tk.Button(self.frame, text="Update note", command=self.update_note_clicked)
        self.key_entry = FloatEntry(self.frame, "key")
        self.value_entry = FloatEntry(self.frame, "value")
        self.set_reservoir_button = tk.Button(self.frame, text="Set reservoir", command=self.set_reservoir_clicked)
        self.get_button = tk.Button(self.frame, text="Get", command=self.get_button_clicked)
        self.note_label = tk.Label(self.frame, text=self.variable.get(), font=FONT)
        
        
        # Placement des boutons dans le frame
        self.pitch_entry.pack(anchor="w")
        self.velocity_entry.pack(anchor="w")
        self.update_note_button.pack()
        self.key_entry.pack(anchor="w")
        self.value_entry.pack(anchor="w")
        self.set_reservoir_button.pack()
        self.get_button.pack()
        self.note_label.pack()
        
        
        # Create a frame to hold the widgets
        self.reservoir_frame = ReservoirFrame(self)
        
        # reservoir data
        self.reservoir_frame.pack()
    
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
        sr = float(self.value_entry.get_entry_value())
        # Use lr and sr values for processing
        address = "/reservoir/set_reservoir"
        args = (lr, sr)  # Exemple d'argument
        self.client.send_message(address, args)
        
    def get_button_clicked(self):
        address = "/reservoir/get_note"
        args = ()  # Exemple d'argument
        self.client.send_message(address, args)
        
    def set_last_note(self, note):
        print(note)
        self.note_liste.append(note)
        print(self.note_liste)
        
    # Fonction de mise à jour de l'interface
    def update_interface(self):
        # Mettez ici votre code pour mettre à jour les éléments de l'interface
        #self.note_label.config(text=str(self.note_liste))


        try:
            with open('tmp/to_gui.obj', 'rb') as fp:
                to_gui = pickle.load(fp)
                print(to_gui)
                self.reservoir_frame.refresh(presoftmax = round_list(to_gui['presoftmax']), postsoftmax = round_list(to_gui['postsoftmax']), sample = round_list(to_gui['sample']), sorted_notes = to_gui['sorted_notes'], sample_idx = to_gui['sample_idx'])

        except (EOFError, FileNotFoundError) as e:
            pass

        # Appelez la fonction update_interface() à chaque pas de temps (par exemple, toutes les 100 ms)
        self.after(200, self.update_interface)
        
class Receiver():
    def __init__(self, ip, receive_port, win):
        # Création du dispatcher et ajout des fonctions de traitement
        disp = dispatcher.Dispatcher()
        disp.map("/send_note_to_ableton", self.add_note)
        
        # Création du serveur OSC
        self.server = osc_server.ThreadingOSCUDPServer((ip, receive_port), disp)
        
        self.win = win
        
    @process_ableton_message
    def add_note(self, address, *args):
        note = args[0]
        print("note", note)
        self.win.set_last_note(note)
        
    def listen(self):
        # Démarrage du serveur
        self.server.serve_forever()
            
class App():
    def __init__(self, ip, receive_port, send_port):
        # Création de la fenêtre principale
        self.window = Ware(ip, send_port)
        # # message udp
        # self.receiver = Receiver(ip, receive_port, self.window)

    def run_server(self):
        # Démarrage du serveur
        self.receiver.listen()
    
    def run_gui(self):
        # Démarrage de la boucle principale de la fenêtre
        self.window.update_interface()
        self.window.mainloop()
        
    def run(self):
        # Création des threads
        server_thread = mp.Process(target=self.run_server)
        gui_thread = mp.Process(target=self.run_gui)

        # Démarrage des threads
        server_thread.start()
        gui_thread.start()
        
        # Attendre la fin des threads
        server_thread.join()
        gui_thread.join()

if __name__ == "__main__":
    
    IP = "127.0.0.1"
    # port sur lesquels écouter les messages OSC
    RECIEVE = 8000
    # Adresse IP et port du destinataire OSC
    SEND = 9000
    
    app = App(IP, RECIEVE, SEND)
    app.run_gui()
    # app.run_server()


    


