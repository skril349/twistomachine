# traction.py

import tkinter as tk
from PIL import Image, ImageTk
import json
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
import Odrive.odrive_setup
from Odrive.odrive_setup import setup_odrive as setup_odrive
from Odrive.odrive_setup import execute_traction_movement as execute_traction_movement

def close_window(root, window):
    window.destroy()
    root.deiconify()

def add_input_field(container, input_fields):
    entry = tk.Entry(container)
    entry.pack(side='top', fill='x', padx=5, pady=5)
    input_fields.append(entry)

def delete_input_field(input_fields, container):
    if input_fields:
        entry_to_remove = input_fields.pop()
        entry_to_remove.pack_forget()
        entry_to_remove.destroy()
        container.pack_forget()
        container.pack(side='top', fill='x', expand=True, padx=5, pady=5)

def print_inputs(fixed_entries, input_fields):
    # Crear un diccionario para almacenar los valores de los campos
    input_data = {}

    # Almacenar los valores de los campos fijos en el diccionario
    for label, entry in fixed_entries.items():
        input_data[label] = entry.get()

    # Almacenar los valores de los campos dinámicos en el diccionario
    for i, entry in enumerate(input_fields):
        input_data[f"Trigger {i+1}"] = entry.get()

    execute_traction_movement(input_data)
    print("data = ",input_data)
    return input_data

def create_screen(root, window_geometry):
    window = tk.Toplevel()
    window.geometry(window_geometry)
    window.title('Pantalla traction')

    left_frame = tk.Frame(window)
    left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Diccionari per emmagatzemar els camps d'entrada fixos i les seves etiquetes
    fixed_entries = {}

    # Crear i afegir camps d'entrada fixos
    labels = ['Pause 1:', 'Distance 1:', 'Pause2:', 'Distance 2:', 'Cicles:']
    for label in labels:
        row_frame = tk.Frame(left_frame)
        row_frame.pack(side='top', fill='x', padx=5, pady=5)
        lbl = tk.Label(row_frame, text=label, anchor='w')
        lbl.pack(side='left')
        entry = tk.Entry(row_frame)
        entry.pack(side='right', expand=True, fill='x')
        fixed_entries[label] = entry  # Guardar l'entrada amb l'etiqueta associada

    # Contenidor per als inputs dinàmics i els botons
    dynamic_container = tk.Frame(left_frame)
    dynamic_container.pack(side='top', fill='x', expand=True, padx=5, pady=5)

    # Llista per emmagatzemar els camps d'entrada dinàmics
    input_fields = []

    buttons_frame = tk.Frame(left_frame)
    buttons_frame.pack(side='top', fill='x', padx=5, pady=5)

    # Botó per afegir inputs dinàmics
    btn_add = tk.Button(buttons_frame, text="Add Trigger", command=lambda: add_input_field(buttons_frame, input_fields))
    btn_add.pack(side='top', fill='x', padx=5, pady=5)

    # Botó per eliminar l'últim input dinàmic afegit
    btn_delete = tk.Button(buttons_frame, text="Delete Trigger", command=lambda: delete_input_field(input_fields, buttons_frame))
    btn_delete.pack(side='top', fill='x', padx=5, pady=5)

    # Botó per tornar enrere
    btn_back = tk.Button(left_frame, text="Back", command=lambda: close_window(root, window))
    btn_back.pack(side='bottom', fill='x', padx=5, pady=5)

    # Botó per imprimir les dades
    btn_start = tk.Button(left_frame, text="Start button", command=lambda: print_inputs(fixed_entries, input_fields))
    btn_start.pack(side='bottom', fill='x', padx=5, pady=20)

    # Carregar la imatge amb Pillow
    path = 'assets/traction_graph.png'  # Actualitza el camí segons la ubicació de les teves imatges
    pil_image = Image.open(path)
    img = ImageTk.PhotoImage(pil_image)
    # Crear el marc per a la imatge
    right_frame = tk.Frame(window, borderwidth=2, relief='sunken')
    right_frame.pack(side='right', fill='both', expand=True)

    # Crear el Label i establir la imatge
    label_image = tk.Label(right_frame, image=img)
    label_image.image = img  # Mantenir una referència!
    label_image.pack(expand=True)

    return window
