# main.py

import tkinter as tk
from PIL import Image, ImageTk
from screens.traction import create_screen as create_screen1
from screens.twist import create_screen as create_screen2
from screens.twistandtrac import create_screen as create_screen3

def main_window():
    root = tk.Tk()
    root.title("Pantalla Principal")

    window_geometry = "800x600+100+100"
    root.geometry(window_geometry)

    # Crea una llista de funcions per a cada botó
    screen_functions = [create_screen1, create_screen2, create_screen3]

    for i, screen_function in enumerate(screen_functions):
        path = f'assets/image{i+1}.png'  # Actualitza el camí segons la ubicació de les teves imatges
        try:
            pil_image = Image.open(path)
            img = ImageTk.PhotoImage(pil_image)
            # Utilitza cada funció lambda amb la seva pròpia funció de pantalla
            btn = tk.Button(root, image=img, command=lambda screen_function=screen_function: screen_function(root, window_geometry))
            btn.image = img  # Manté una referència!
            btn.pack(side="left", padx=10, pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")

    root.mainloop()

# Això iniciarà l'aplicació
main_window()
