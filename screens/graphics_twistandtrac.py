import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import threading

import sys
sys.path.append('../')  # Asegúrate de actualizar esta ruta
from Odrive.odrive_setup import get_motor0_data as get_motor0_data
from Odrive.odrive_setup import get_motor1_data as get_motor1_data

def update_twistandtrac_plot(root, position_label, position2_label, intensity_label, 
               voltage_label, torque_label, positions0, positions1, currents0, currents1, intensities0, 
               intensities1, voltages, torques0, torques1, position_ax, current_ax, intensity_ax, 
               voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, 
               torque_canvas, timestamps):

    current_time = time.time()

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
    timestamps.append(current_time)

    # Netejar eixos i dibuixar noves dades
    position_ax.clear()
    current_ax.clear()
    intensity_ax.clear()
    voltage_ax.clear()
    torque_ax.clear()

    position_ax.plot(positions0, label='Position Motor0 (degrees)')
    position_ax.plot(positions1, label='Position Motor1 (degrees)')
    current_ax.plot(currents0, label='Motor Current Motor0 (A)')
    current_ax.plot(currents1, label='Motor Current Motor1 (A)')
    intensity_ax.plot(intensities0, label='Intensity Motor0')
    intensity_ax.plot(intensities1, label='Intensity Motor1')
    voltage_ax.plot(voltages, label='Voltage (V)')
    torque_ax.plot(torques0, label='Torque Motor0 (%)')
    torque_ax.plot(torques1, label='Torque Motor1 (%)')

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
    root.after(500, update_twistandtrac_plot, root, position_label, position2_label, intensity_label, 
               voltage_label, torque_label, positions0, positions1, currents0, currents1, intensities0, 
               intensities1, voltages, torques0, torques1, position_ax, current_ax, intensity_ax, 
               voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, 
               torque_canvas, timestamps)


def download_data(timestamps, positions0, positions1, currents0, currents1, 
                  intensities0, intensities1, voltages, torques0, torques1, 
                  filename="data/motor_twistandtrac_data.csv"):
    
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
    #print(df.head(10))
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

    return window
