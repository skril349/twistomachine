# traction.py

import tkinter as tk

def close_window(root, window):
    window.destroy()
    root.deiconify()

def add_input_field(frame):
    entry = tk.Entry(frame)
    entry.pack(side='top', fill='x', padx=5, pady=5)
    input_fields.append(entry)

def print_inputs(fixed_entries, input_fields):
    # Imprimir els valors dels camps fixos
    for label, entry in fixed_entries.items():
        print(f"{label}: {entry.get()}")
    # Imprimir els valors dels camps dinàmics
    for i, entry in enumerate(input_fields):
        print(f"Trigger {i+1}: {entry.get()}")

def create_screen(root, window_geometry):
    window = tk.Toplevel()
    window.geometry(window_geometry)
    window.title('Pantalla traction')

    left_frame = tk.Frame(window)
    left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Diccionari per emmagatzemar els camps d'entrada fixos i les seves etiquetes
    fixed_entries = {}

    # Crear i afegir camps d'entrada fixos
    labels = ['Pause 1:', 'Distancia:', 'Pause2:', 'distancia return:', 'cicles:']
    for label in labels:
        row_frame = tk.Frame(left_frame)
        row_frame.pack(side='top', fill='x', padx=5, pady=5)
        lbl = tk.Label(row_frame, text=label, anchor='w')
        lbl.pack(side='left')
        entry = tk.Entry(row_frame)
        entry.pack(side='right', expand=True, fill='x')
        fixed_entries[label] = entry  # Guardar l'entrada amb l'etiqueta associada

    # Marc per als inputs dinàmics
    dynamic_frame = tk.Frame(left_frame)
    dynamic_frame.pack(side='top', fill='x', expand=True, padx=5, pady=5)

    # Botó per afegir inputs dinàmics
    btn_add = tk.Button(dynamic_frame, text="Add Trigger", command=lambda: add_input_field(dynamic_frame))
    btn_add.pack(side='top', fill='x', padx=5, pady=5)

    # Llista per emmagatzemar els camps d'entrada dinàmics
    global input_fields
    input_fields = []

    # Botó per tornar enrere
    btn_back = tk.Button(left_frame, text="Back", command=lambda: close_window(root, window))
    btn_back.pack(side='top', fill='x', padx=5, pady=5)

    # Botó per imprimir les dades
    btn_start = tk.Button(left_frame, text="Start button", command=lambda: print_inputs(fixed_entries, input_fields))
    btn_start.pack(side='bottom', fill='x', padx=5, pady=20)

    # Marc per la imatge
    right_frame = tk.Frame(window, borderwidth=2, relief='sunken')
    right_frame.pack(side='right', fill='both', expand=True)
    label_image = tk.Label(right_frame, text="Image")
    label_image.pack(expand=True)

    return window
