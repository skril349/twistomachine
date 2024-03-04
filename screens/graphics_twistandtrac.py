import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import threading
from datetime import datetime
import sys
sys.path.append('../')  # Asegúrate de actualizar esta ruta
from Odrive.odrive_setup import get_motor0_data as get_motor0_data
from Odrive.odrive_setup import get_motor1_data, trigger_twistandtrac_list

time_initial = None
now = datetime.now()


def close_window(root, window, positions0, positions1, currents0, currents1, intensities0, intensities1, voltages, torques0, torques1, timestamps):
    # Limpia todos los arrays
    positions0.clear()
    positions1.clear()
    currents0.clear()
    currents1.clear()
    intensities0.clear()
    intensities1.clear()
    voltages.clear()
    torques0.clear()
    torques1.clear()
    timestamps.clear()
    
    # Restablece time_initial a None
    global time_initial
    time_initial = None
    
    window.destroy()

def update_twistandtrac_plot(root, position_label, position2_label, intensity_label, 
               voltage_label, torque_label, positions0, positions1, currents0, currents1, intensities0, 
               intensities1, voltages, torques0, torques1, position_ax, current_ax, intensity_ax, 
               voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, 
               torque_canvas, timestamps):
    global time_initial
    current_time = time.time()

    if time_initial is None:
        time_initial = current_time
    
    elapsed_time = current_time - time_initial

    # Obtenir dades dels dos motors
    position0, current0, voltage, intensity0, torque0 = get_motor0_data()
    position1, current1, _, intensity1, torque1 = get_motor1_data()

    # Actualitzar etiquetes
    position_label.config(text=f"Position Motor0: {position0:.2f}, Motor1: {position1:.2f} degrees")
    position2_label.config(text=f"Motor Current Motor0: {current0:.2f}, Motor1: {current1:.2f} A")
    intensity_label.config(text=f"Intensity Motor0: {intensity0:.2f}, Motor1: {intensity1:.2f}")
    voltage_label.config(text=f"Voltage: {voltage:.2f} V")
    torque_label.config(text=f"Torque Motor0: {torque0:.2f}, Motor1: {torque1:.2f} %")

    # Afegir dades a les llistes
    positions0.append(position0)
    positions1.append(position1)
    currents0.append(current0)
    currents1.append(current1)
    intensities0.append(intensity0)
    intensities1.append(intensity1)
    voltages.append(voltage)
    torques0.append(torque0)
    torques1.append(torque1)
    timestamps.append(elapsed_time)

    # Netejar eixos i dibuixar noves dades
    position_ax.clear()
    current_ax.clear()
    intensity_ax.clear()
    voltage_ax.clear()
    torque_ax.clear()

    position_ax.plot(timestamps,positions0, label='Position Motor0 (degrees)')
    position_ax.plot(timestamps,positions1, label='Position Motor1 (degrees)')
    current_ax.plot(timestamps,currents0, label='Motor Current Motor0 (A)')
    current_ax.plot(timestamps,currents1, label='Motor Current Motor1 (A)')
    intensity_ax.plot(timestamps,intensities0, label='Intensity Motor0')
    intensity_ax.plot(timestamps,intensities1, label='Intensity Motor1')
    voltage_ax.plot(timestamps,voltages, label='Voltage (V)')
    torque_ax.plot(timestamps,torques0, label='Torque Motor0 (%)')
    torque_ax.plot(timestamps,torques1, label='Torque Motor1 (%)')

    trigger_legend_added = False

    print("lista trigger = ",trigger_twistandtrac_list)
    for trigger_time in trigger_twistandtrac_list:
        print("min timestamps = {0}, max timestamps = {1} and trigger time = {2}".format(min(timestamps),max(timestamps),trigger_time-time_initial))
        if min(timestamps) <= trigger_time-time_initial <= max(timestamps):
            position_ax.axvline(x=trigger_time-time_initial, color='r', linestyle='--', label='Trigger' if not trigger_legend_added else "")
            trigger_legend_added = True  # Marcar que la leyenda del trigger ya se ha añadido

    # Afegir llegendes
    position_ax.legend()
    current_ax.legend()
    intensity_ax.legend()
    voltage_ax.legend()
    torque_ax.legend()

    # Redibuixar els canvas
    position_canvas.draw()
    current_canvas.draw()
    intensity_canvas.draw()
    voltage_canvas.draw()
    torque_canvas.draw()

    # Programar la propera actualització
    root.after(50, update_twistandtrac_plot, root, position_label, position2_label, intensity_label, 
               voltage_label, torque_label, positions0, positions1, currents0, currents1, intensities0, 
               intensities1, voltages, torques0, torques1, position_ax, current_ax, intensity_ax, 
               voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, 
               torque_canvas, timestamps)


def download_data(timestamps, positions0, positions1, currents0, currents1, 
                  intensities0, intensities1, voltages, torques0, torques1, 
                  filename = f"data/motor_twistandtrac_data_{now.strftime('%Y%m%d_%H%M%S')}.csv"):
    
    data = {
        "Timestamp": timestamps,
        "Position Motor0": positions0,
        "Position Motor1": positions1,
        "Motor Current Motor0": currents0,
        "Motor Current Motor1": currents1,
        "Intensity Motor0": intensities0,
        "Intensity Motor1": intensities1,
        "Voltage": voltages,
        "Torque Motor0": torques0,
        "Torque Motor1": torques1
    }
    
    df = pd.DataFrame(data)

    # Añadir columna para los triggers
    df['Trigger'] = False
    for trigger_time in trigger_twistandtrac_list:
        # Encontrar el índice más cercano en el DataFrame para el tiempo del trigger
        closest_time_index = (df['Timestamp'] - (trigger_time-time_initial)).abs().idxmin()
        df.at[closest_time_index, 'Trigger'] = True

    df.to_csv(filename, index=False)
    print(f"Datos guardados en {filename}")


def create_twistandtrac_plot_screen(root, window_geometry):
    window = tk.Toplevel(root)
    window.geometry(window_geometry)
    window.title('Motor twist Data Visualization')


    positions = []
    currents = []
    intensities = []
    voltages = []
    torques = []
    timestamps = []
    positions1 = []
    currents1 = []
    intensities1 = []
    voltages1 = []
    torques1 = []
    timestamps1 = []

    positions0 = []
    currents0 = []
    intensities0 = []
    voltages0 = []
    torques0 = []

    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    fig_size = (4, 3)  # Ajustar según sea necesario

    fig_position, position_ax = plt.subplots(figsize=fig_size)
    position_canvas = FigureCanvasTkAgg(fig_position, master=left_frame)
    position_canvas.get_tk_widget().pack()

    fig_current, current_ax = plt.subplots(figsize=fig_size)
    current_canvas = FigureCanvasTkAgg(fig_current, master=left_frame)
    current_canvas.get_tk_widget().pack()

    fig_intensity, intensity_ax = plt.subplots(figsize=fig_size)
    intensity_canvas = FigureCanvasTkAgg(fig_intensity, master=right_frame)
    intensity_canvas.get_tk_widget().pack()

    fig_torque, torque_ax = plt.subplots(figsize=fig_size)
    torque_canvas = FigureCanvasTkAgg(fig_torque, master=right_frame)
    torque_canvas.get_tk_widget().pack()

    fig_voltage, voltage_ax = plt.subplots(figsize=fig_size)
    voltage_canvas = FigureCanvasTkAgg(fig_voltage, master=right_frame)
    voltage_canvas.get_tk_widget().pack()

    position_label = tk.Label(window, text="Position: N/A")
    position_label.pack()
    position2_label = tk.Label(window, text="Motor Current: N/A")
    position2_label.pack()
    intensity_label = tk.Label(window, text="Intensity: N/A")
    intensity_label.pack()
    voltage_label = tk.Label(window, text="Voltage: N/A")
    voltage_label.pack()
    torque_label = tk.Label(window, text="Torque: N/A")
    torque_label.pack()

    download_button = tk.Button(window, text="Descargar Datos", command=lambda: download_data(timestamps, positions0, positions1, currents0, currents1, 
                intensities0, intensities1, voltages, torques0, torques1))
    download_button.pack()

    #update_twistandtrac_plot(window, position_label, position2_label, intensity_label, voltage_label, torque_label,positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas,timestamps)
    update_twistandtrac_plot(window, position_label, position2_label, intensity_label, 
               voltage_label, torque_label, positions0, positions1, currents0, currents1, intensities0, 
               intensities1, voltages, torques0, torques1, position_ax, current_ax, intensity_ax, 
               voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, 
               torque_canvas, timestamps)

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(root, window, positions0, positions1, currents0, currents1, intensities0, intensities1, voltages, torques0, torques1, timestamps))

    return window
