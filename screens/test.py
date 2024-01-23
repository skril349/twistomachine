# twistandtrac.py

import tkinter as tk
from PIL import Image, ImageTk

def close_window(root, window):
    window.destroy()
    root.deiconify()

def add_input_group(container, input_list):
    # Crea un nou marc per al grup d'inputs
    frame = tk.Frame(container)
    frame.pack(side='top', fill='x', padx=5, pady=5)

    # Crea i afegeix els inputs al marc
    inputs = {
        'time': tk.Entry(frame, width=20),
        'Dx': tk.Entry(frame, width=20),
        'N': tk.Entry(frame, width=20),
    }
    inputs['time'].pack(side='left', padx=2)
    inputs['Dx'].pack(side='left', padx=2)
    inputs['N'].pack(side='left', padx=2)

    # Afegeix el marc al llistat d'inputs
    input_list.append((frame, inputs))

def delete_input_group(input_list):
    if input_list:
        frame, inputs = input_list.pop()
        frame.destroy()  # Elimina el marc i tots els widgets dins d'ell

def add_trigger(container, trigger_list):
    entry = tk.Entry(container, width=20)
    entry.pack(side='top', fill='x', padx=5, pady=5)
    trigger_list.append(entry)

def delete_trigger(trigger_list):
    if trigger_list:
        entry = trigger_list.pop()
        entry.destroy()

def create_screen(root, window_geometry):
    window = tk.Toplevel()
    window.geometry(window_geometry)
    window.title('Pantalla twistandtrac')

 
     # Marc per als inputs de time, Dx, i N
    left_frame = tk.Frame(window)
    left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Marc per als inputs de Triggers
    middle_frame = tk.Frame(window)
    middle_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Marc per a les imatges
    right_frame = tk.Frame(window)
    right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)


    # Llista per guardar els grups d'inputs de N
    n_input_list = []

    # Botons per gestionar els inputs de N
    btn_add_n = tk.Button(left_frame, text="Add btn N", command=lambda: add_input_group(left_frame, n_input_list))
    btn_add_n.pack(side='left', padx=5, pady=5)

    btn_delete_n = tk.Button(left_frame, text="Delete Btn N", command=lambda: delete_input_group(n_input_list))
    btn_delete_n.pack(side='left', padx=5, pady=5)

    # Llista per guardar els inputs de Triggers
    trigger_list = []

    # Botons per gestionar els inputs de Triggers
    btn_add_trigger = tk.Button(middle_frame, text="Add btn trigger", command=lambda: add_trigger(middle_frame, trigger_list))
    btn_add_trigger.pack(side='left', padx=5, pady=5)

    btn_delete_trigger = tk.Button(middle_frame, text="Delete btn trigger", command=lambda: delete_trigger(trigger_list))
    btn_delete_trigger.pack(side='left', padx=5, pady=5)

    # Botons de control
    btn_start = tk.Button(middle_frame, text="Start btn", command=lambda: print("Start"))
    btn_start.pack(side='bottom', padx=5, pady=5)

    btn_back = tk.Button(middle_frame, text="Back", command=lambda: close_window(root, window))
    btn_back.pack(side='bottom', padx=5, pady=5)

    # Carrega i mostra les imatges

    image_paths = ['assets/image1.png', 'assets/image2.png']  # Actualitza els camins de les imatges
    images = []
    for path in image_paths:
        pil_image = Image.open(path)
        img = ImageTk.PhotoImage(pil_image)
        images.append(img)  # Mantenir una referència a l'objecte PhotoImage
        label = tk.Label(right_frame, image=img)
        label.pack(fill='both', expand=True, padx=10, pady=10)

    return window
