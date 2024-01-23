# main.py

import tkinter as tk
from PIL import Image, ImageTk
from screens.screen1 import create_screen as create_screen1
from screens.screen2 import create_screen as create_screen2
from screens.screen3 import create_screen as create_screen3

def main_window():
    root = tk.Tk()
    root.title("Pantalla Principal")

    window_geometry = "600x400+100+100"
    root.geometry(window_geometry)

    for i in range(1, 4):
        path = f'assets/image{i}.png'  # Actualitza el camí segons la ubicació de les teves imatges
        try:
            pil_image = Image.open(path)
            img = ImageTk.PhotoImage(pil_image)
            # Assigna la funció de pantalla correcta a cada botó
            command_func = globals()[f'create_screen{i}']
            btn = tk.Button(root, image=img, command=lambda i=i: command_func(root, window_geometry))
            btn.image = img  # keep a reference!
            btn.pack(side="left", padx=10, pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")

    root.mainloop()

# Això iniciarà l'aplicació
main_window()
