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

def update_twist_plot(root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas,timestamps):
    current_time = time.time()
    position, position2, intensity, voltage, torque = get_motor0_data()

    position_label.config(text=f"Position: {position:.2f} degrees")
    position2_label.config(text=f"Motor Current: {position2:.2f} A")
    intensity_label.config(text=f"Intensity: {intensity:.2f}")
    voltage_label.config(text=f"Voltage: {voltage:.2f} V")
    torque_label.config(text=f"Torque: {torque:.2f} %")

    positions.append(position)
    currents.append(position2)
    intensities.append(intensity)
    voltages.append(voltage)
    torques.append(torque)
    timestamps.append(current_time)

    position_ax.clear()
    current_ax.clear()
    intensity_ax.clear()
    voltage_ax.clear()
    torque_ax.clear()

    position_ax.plot(positions, label='Position (degrees)')
    current_ax.plot(currents, label='Motor Current (A)')
    intensity_ax.plot(intensities, label='Intensity')
    voltage_ax.plot(voltages, label='Voltage (V)')
    torque_ax.plot(torques, label='Torque (%)')

    position_ax.legend()
    current_ax.legend()
    intensity_ax.legend()
    voltage_ax.legend()
    torque_ax.legend()

    position_canvas.draw()
    current_canvas.draw()
    intensity_canvas.draw()
    voltage_canvas.draw()
    torque_canvas.draw()

    root.after(500, update_twist_plot, root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas,timestamps)

def download_data(timestamps,positions, currents, intensities,voltages, torques, filename="data/motor_twist_data.csv"):
    data = {
        "Timestamp": timestamps,
        "Position": positions,
        "Motor Current": currents,
        "Intensity": intensities,
        "Voltage": voltages,
        "Torque": torques
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Datos guardados en {filename}")

def create_twist_plot_screen(root, window_geometry):
    window = tk.Toplevel(root)
    window.geometry(window_geometry)
    window.title('Motor twist Data Visualization')

    positions = []
    currents = []
    intensities = []
    voltages = []
    torques = []
    timestamps = []

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

    download_button = tk.Button(window, text="Descargar Datos", command=lambda: download_data(timestamps,positions, currents, intensities, voltages, torques))
    download_button.pack()

    update_twist_plot(window, position_label, position2_label, intensity_label, voltage_label, torque_label,positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas,timestamps)

    return window
