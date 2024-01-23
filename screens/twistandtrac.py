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
    left_frame = tk.Frame(window)  # Puedes cambiar el color de fondo según tus preferencias
    left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Marc per als inputs de Triggers
    middle_frame = tk.Frame(window)  # Puedes cambiar el color de fondo según tus preferencias
    middle_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Marc per a les imatges
    right_frame = tk.Frame(window)  # Puedes cambiar el color de fondo según tus preferencias
    right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)



    buttonN_frame = tk.Frame(left_frame)  # Puedes cambiar el color de fondo según tus preferencias
    buttonN_frame.pack(side='bottom', fill='x', expand=True, padx=10, pady=10)

    # Llista per guardar els grups d'inputs de N
    n_input_list = []

    # Botons per gestionar els inputs de N
    btn_add_n = tk.Button(left_frame, text="Add btn N", command=lambda: add_input_group(buttonN_frame, n_input_list))
    btn_add_n.pack(anchor="ne",fill='x',  padx=5, pady=5)

    btn_delete_n = tk.Button(left_frame, text="Delete Btn N", command=lambda: delete_input_group(n_input_list))
    btn_delete_n.pack(anchor="nw",fill='x',  padx=5, pady=5)

    # Botons de control
    btn_start = tk.Button(middle_frame, text="Start btn", command=lambda: print("Start"))
    btn_start.pack(side='bottom', padx=5, pady=5)

    btn_back = tk.Button(middle_frame, text="Back", command=lambda: close_window(root, window))
    btn_back.pack(side='bottom', padx=5, pady=5)

    trigger_frame = tk.Frame(middle_frame)  # Puedes cambiar el color de fondo según tus preferencias
    trigger_frame.pack(side='bottom', fill='x', expand=True, padx=10, pady=10)
    # Llista per guardar els inputs de Triggers
    trigger_list = []

    # Botons per gestionar els inputs de Triggers
    btn_add_trigger = tk.Button(middle_frame, text="Add btn trigger", command=lambda: add_trigger(trigger_frame, trigger_list))
    btn_add_trigger.pack(side='top',fill='x',  padx=5, pady=5)

    btn_delete_trigger = tk.Button(middle_frame, text="Delete btn trigger", command=lambda: delete_trigger(trigger_list))
    btn_delete_trigger.pack(side='top',fill='x',  padx=5, pady=5)

    

    # Carrega i mostra les imatges

      # Carregar la imatge amb Pillow
    path1 = 'assets/traction_graph.png'  # Actualitza el camí segons la ubicació de les teves imatges
    pil_image = Image.open(path1)
    img1 = ImageTk.PhotoImage(pil_image)
    # Crear el marc per a la imatge
    right_frame_image = tk.Frame(right_frame, borderwidth=2, relief='sunken')
    right_frame_image.pack(side='top')

    # Crear el Label i establir la imatge
    label_image = tk.Label(right_frame_image, image=img1)
    label_image.image = img1  # Mantenir una referència!
    label_image.pack(expand=False)

    path2 = 'assets/twist_graph.png'  # Actualitza el camí segons la ubicació de les teves imatges
    pil_image = Image.open(path2)
    img2 = ImageTk.PhotoImage(pil_image)
    # Crear el marc per a la imatge
    right_frame_image2 = tk.Frame(right_frame, borderwidth=2, relief='sunken')
    right_frame_image2.pack(side='bottom')

    # Crear el Label i establir la imatge
    label_image2 = tk.Label(right_frame_image2, image=img2)
    label_image2.image = img2  # Mantenir una referència!
    label_image2.pack(expand=False)

    
    return window
