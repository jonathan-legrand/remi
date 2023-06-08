import tkinter as tk
import musicalbeeps
from tkinter import ttk

class PianoKey:
    def __init__(self, canvas, note, color, x, y, width, height):
        self.canvas = canvas
        self.note = note
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_pressed = False

    def draw(self):
        self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline='black')

    def press(self):
        self.is_pressed = True
        self.canvas.itemconfig(self.note, fill='red')
        self.play_note()
        # Autres actions à effectuer lorsque la touche est pressée

    def release(self):
        self.is_pressed = False
        self.canvas.itemconfig(self.note, fill=self.color)
        # Autres actions à effectuer lorsque la touche est relâchée

    def get_note(self):
        return self.note

    def isIn(self, mouse_x, mouse_y):
        return mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= self.y and mouse_y <= self.y + self.height

class PianoCanvas(tk.Canvas, musicalbeeps.Player):
    def __init__(self, parent, width, height, notes, tempo=0.2, octave = 4, volume = 1.0, mute_output = False):
        super().__init__(parent, width=width, height=height)
        musicalbeeps.Player.__init__(self, volume=volume, mute_output=mute_output)
        self.width = width
        self.height = height
        self.tempo = tempo
        self.octave = octave
        self.volume = volume
        self.mute_output = mute_output
        self.notes = notes
        self.white_keys = []
        self.black_keys = []
        self.bind("<Button-1>", self.canvas_click)
        self.create_keys()

    def create_keys(self):
        x = 0
        y = 0
        white_width = self.width / self.get_nb_white()
        white_height = self.height
        black_width = white_width / 2
        black_height = white_height / 2

        for note in self.notes:
            if '#' in note:
                key = PianoKey(self, note, 'black', x - black_width / 2, y, black_width, black_height)
                self.black_keys.append(key)
            else:
                key = PianoKey(self, note, 'white', x, y, white_width, white_height)
                x += white_width
                self.white_keys.append(key)

        self.draw_keys()

    def draw_keys(self):
        for k in self.white_keys:
            k.draw()

        for k in self.black_keys:
            k.draw()

    def get_nb_white(self):
        count = 0
        for note in self.notes:
            if not '#' in note:
                count += 1

        return count

    def canvas_click(self, event):
        # Actions à effectuer lors du clic sur le canvas
        #print("Clic détecté : x =", event.x, ", y =", event.y)
        keys = self.black_keys + self.white_keys
        for k in keys:
            if k.isIn(event.x, event.y):
                note = k.get_note()
                self.play_note(note, self.tempo)
                break

class ScalerFrame(tk.Frame):
    def __init__(self, parent, name, from_, to, orient=tk.HORIZONTAL):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.from_ = from_
        self.to = to
        self.orient = orient
        self.create_widgets()

    def create_widgets(self):
        # Création du label
        self.label = tk.Label(self, text=f"{self.name} :")
        self.label.pack(side=tk.TOP)

        self.scale = ttk.Scale(self, from_=self.from_, to=self.to, orient=self.orient)
        self.scale.set(0)  # Définit la valeur initiale du curseur
        self.scale.pack()

        # Lier un événement au déplacement du curseur
        self.scale.bind("<B1-Motion>", self.on_scale_move)

    def on_scale_move(self, event):
        value = int(self.scale.get())
        self.label.config(text=f"{self.name} : {value}")

class SynthesizerFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Configuration des notes de piano
        self.notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

        self.create_widgets()

    def create_widgets(self):
        # Création du curseur
        self.scale = ScalerFrame(self, name='Octave', from_=-2, to=8)
        self.scale.pack(padx=10, pady=10)

        # Création du canvas personnalisé
        piano_canvas = PianoCanvas(self, width=800, height=200, notes=self.notes)
        piano_canvas.pack()

if __name__ == "__main__":
    

    # Création de la fenêtre principale
    window = tk.Tk()
    window.title("Synthesizer")

    synth = SynthesizerFrame(window)
    synth.pack()

    # Lancement de la boucle principale
    window.mainloop()


