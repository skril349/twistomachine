import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import sys
from datetime import datetime
sys.path.append('../')  # Asegúrate de actualizar esta ruta
from Odrive.odrive_setup import get_motor1_data, trigger_times_list

# Restablece time_initial a None
global time_initial
time_initial = None
now = datetime.now()


def close_window(root, window, positions, currents, intensities, voltages, torques, timestamps):
    # Limpia todos los arrays
    positions.clear()
    currents.clear()
    intensities.clear()
    voltages.clear()
    torques.clear()
    timestamps.clear()
    
    # Restablece time_initial a None
    global time_initial
    time_initial = None
    
    window.destroy()


def update_plot(root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas, timestamps):
    global time_initial
    current_time = time.time()

    if time_initial is None:
        time_initial = current_time
    
    elapsed_time = current_time - time_initial


    position, position2, intensity, voltage, torque = get_motor1_data()

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
    timestamps.append(elapsed_time)

    # Limpiar los ejes antes de dibujar
    position_ax.clear()
    current_ax.clear()
    intensity_ax.clear()
    voltage_ax.clear()
    torque_ax.clear()

    # Dibujar los datos
    position_ax.plot(timestamps, positions, label='Position (degrees)')
    current_ax.plot(timestamps, currents, label='Motor Current (A)')
    intensity_ax.plot(timestamps, intensities, label='Intensity')
    voltage_ax.plot(timestamps, voltages, label='Voltage (V)')
    torque_ax.plot(timestamps, torques, label='Torque (%)')

    # Dibujar líneas verticales para cada trigger
    for trigger_time in trigger_times_list:
        print("trigger time = ",trigger_time)
        print("timestamps = ",timestamps[-1])
        print("trigger time - elapsed = ",trigger_time-time_initial)

        if min(timestamps) <= trigger_time-time_initial <= max(timestamps):
            position_ax.axvline(x=trigger_time-time_initial, color='r', linestyle='--', label='Trigger')

    # Añadir leyendas a los gráficos
    position_ax.legend()
    current_ax.legend()
    intensity_ax.legend()
    voltage_ax.legend()
    torque_ax.legend()

    # Actualizar los canvas
    position_canvas.draw()
    current_canvas.draw()
    intensity_canvas.draw()
    voltage_canvas.draw()
    torque_canvas.draw()

    # Programar la próxima actualización
    root.after(50, update_plot, root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas, timestamps)

def download_data(timestamps, positions, currents, intensities, voltages, torques,filename = f"data/motor_data_{now.strftime('%Y%m%d_%H%M%S')}.csv"):
    data = {
        "Timestamp": timestamps,
        "Position": positions,
        "Motor Current": currents,
        "Intensity": intensities,
        "Voltage": voltages,
        "Torque": torques
    }
    df = pd.DataFrame(data)

    # Añadir columna para los triggers
    df['Trigger'] = False
    for trigger_time in trigger_times_list:
        # Encontrar el índice más cercano en el DataFrame para el tiempo del trigger
        closest_time_index = (df['Timestamp'] - (trigger_time-time_initial)).abs().idxmin()
        df.at[closest_time_index, 'Trigger'] = True

    df.to_csv(filename, index=False)
    print(f"Datos guardados en {filename}")

def create_plot_screen(root, window_geometry):
    time_initial = None
    window = tk.Toplevel(root)
    window.geometry(window_geometry)
    window.title('Motor Data Visualization')

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

    update_plot(window, position_label, position2_label, intensity_label, voltage_label, torque_label,positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas,timestamps)
    
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(root, window, positions, currents, intensities, voltages, torques, timestamps))

    return window
