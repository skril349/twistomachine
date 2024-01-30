# twistandtrac.py

import tkinter as tk
from PIL import Image, ImageTk
import json
import threading
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
from Functions.structuring_json import processar_json as processar_json
import Odrive.odrive_setup
from Odrive.odrive_setup import setup_odrive as setup_odrive
from Odrive.odrive_setup import execute_movement_sequences as execute_movement_sequences
from screens.graphics_twistandtrac import create_twistandtrac_plot_screen as create_twistandtrac_plot_screen  # Importa la función desde graphics.py

def close_window(root, window):
    window.destroy()
    root.deiconify()



def add_input_group(container, input_list):
    # Crea un nou marc per al grup d'inputs
    frame = tk.Frame(container)
    frame.pack(side='top', fill='x', padx=5, pady=5)

    index_label = tk.Label(frame, text=f'Pos {len(input_list) + 1}:', font=('Helvetica', 12, 'bold'))
    index_label.pack(side='left', padx=2)

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

# Aquesta és la nova funció que controla la repetició del moviment del motor
def repeat_motor_movement(fixed_entries, input_fields, root, window_geometry, num_cycles):
    for _ in range(num_cycles):
        motor_thread = threading.Thread(target=lambda: start_button_action(fixed_entries, input_fields, root, window_geometry))
        motor_thread.start()
        motor_thread.join()  # Esperar que el cicle actual acabi

# Modifica la funció start_motor_and_graphic per llançar el loop de cicles en un nou fil
def start_motor_and_graphic(fixed_entries, input_fields, root, window_geometry, cycles_entry):
    num_cycles = int(cycles_entry.get())

    # Crea i inicia un nou fil per a la repetició del moviment del motor
    motor_loop_thread = threading.Thread(target=lambda: repeat_motor_movement(fixed_entries, input_fields, root, window_geometry, num_cycles))
    motor_loop_thread.start()

    # Iniciar la visualización de gráficos en el fil principal
    create_twistandtrac_plot_screen(root, window_geometry)


def start_button_action(n_input_list, trigger_list, root, window_geometry):
    # Recopilar los valores de los inputs de N
    n_values = []
    for group in n_input_list:
        inputs = group[1]
        n_values.append({
            'time': inputs['time'].get(),
            'Dx': inputs['Dx'].get(),
            'N': inputs['N'].get()
        })
    trigger_values = []
    for group in trigger_list:
        inputs = group[1]
        trigger_values.append({
            'Pos': inputs['Pos'].get(),
            'Trigger': inputs['Trigger'].get(),
        })

    

    # Crear un diccionario con los valores recopilados
    data = {
        'N_inputs': n_values,
        'Triggers': trigger_values
    }

    # Imprimir la cadena JSON en la terminal
    Dx, time, N, Trigger = processar_json(data)
    print("Dx:", Dx)
    print("time:", time)
    print("N:", N)
    print("Trigger:", Trigger)

    execute_movement_sequences(Dx, time, N, Trigger)

def delete_input_group(input_list):
    if input_list:
        frame, inputs = input_list.pop()
        frame.destroy()  # Elimina el marc i tots els widgets dins d'ell


def add_trigger(container,trigger_list):
    frame = tk.Frame(container)
    frame.pack(side='top', fill='x', padx=5, pady=5)

    # Crea i afegeix els inputs al marc
    inputs = {
        'Pos': tk.Entry(frame, width=20),
        'Trigger': tk.Entry(frame, width=20),
    }
    inputs['Pos'].pack(side='left', padx=2)
    inputs['Trigger'].pack(side='left', padx=2)

    trigger_list.append((frame, inputs))


def delete_trigger(trigger_list):
    if trigger_list:
        frame, entry = trigger_list.pop()
        frame.destroy()

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
    title_label = tk.Label(left_frame, text="Pause                     Dx                    N", font=('Helvetica', 12, 'bold'))
    title_label.pack(side='top', pady=5)
    # Botons de control

    cycles_frame = tk.Frame(middle_frame)
    cycles_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    cycles_label = tk.Label(cycles_frame, text="Cicles:", font=('Helvetica', 12))
    cycles_label.pack(side='left', padx=2)

    cycles_entry = tk.Entry(cycles_frame, width=20)
    cycles_entry.pack(side='left', padx=2)
    cycles_entry.insert(0, "1")  # Estableix el valor per defecte a 1



    btn_start = tk.Button(middle_frame, text="Start", command=lambda: start_motor_and_graphic(n_input_list, trigger_list, root, window_geometry, cycles_entry))
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
    trigger_title = tk.Label(middle_frame, text="Number Pos         Trigger", font=('Helvetica', 12, 'bold'))
    trigger_title.pack(side='top', pady=5)
    

    # Carrega i mostra les imatges

      # Carregar la imatge amb Pillow
    path1 = 'assets/tract_and_twist.png'  # Actualitza el camí segons la ubicació de les teves imatges
    pil_image = Image.open(path1)
    img1 = ImageTk.PhotoImage(pil_image)
    # Crear el marc per a la imatge
    right_frame_image = tk.Frame(right_frame, borderwidth=2, relief='sunken')
    right_frame_image.pack(side='top')

    # Crear el Label i establir la imatge
    label_image = tk.Label(right_frame_image, image=img1)
    label_image.image = img1  # Mantenir una referència!
    label_image.pack(expand=True)

    # path2 = 'assets/twist_graph.png'  # Actualitza el camí segons la ubicació de les teves imatges
    # pil_image = Image.open(path2)
    # img2 = ImageTk.PhotoImage(pil_image)
    # # Crear el marc per a la imatge
    # right_frame_image2 = tk.Frame(right_frame, borderwidth=2, relief='sunken')
    # right_frame_image2.pack(side='bottom')

    # # Crear el Label i establir la imatge
    # label_image2 = tk.Label(right_frame_image2, image=img2)
    # label_image2.image = img2  # Mantenir una referència!
    # label_image2.pack(expand=False)

    
    return window
