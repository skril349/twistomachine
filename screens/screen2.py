# screen2.py

import tkinter as tk

def close_window(root, window):
    window.destroy()
    root.deiconify()

def create_screen(root, window_geometry):
    window = tk.Toplevel()
    window.geometry(window_geometry)
    window.title('Pantalla 2')

    label = tk.Label(window, text="Aquesta és la pantalla 2")
    label.pack(pady=20)
    btn_back = tk.Button(window, text="Torna enrere", command=lambda: close_window(root, window))
    btn_back.pack(side="bottom", pady=20)
    # Aquí pots afegir més widgets a la pantalla 1 com desitgis

    return window
