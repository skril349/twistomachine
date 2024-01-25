import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
import Odrive.odrive_setup
from Odrive.odrive_setup import get_motor_data as get_motor_data

# Esta función se llama repetidamente para actualizar los gráficos
def update_plot(root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas):
    # datos en tiempo real
    position, position2, intensity, voltage, torque = get_motor_data()
    # Actualizar etiquetas
    position_label.config(text=f"Position: {position:.2f} degrees")
    position2_label.config(text=f"Motor Current: {position2:.2f} A")
    intensity_label.config(text=f"Intensity: {intensity:.2f}")
    voltage_label.config(text=f"Voltage: {voltage:.2f} V")
    torque_label.config(text=f"Torque: {torque:.2f} %")

    # Agregar datos a las listas
    positions.append(position)
    currents.append(position2)
    intensities.append(intensity)
    voltages.append(voltage)
    torques.append(torque)

    # Limpiar y dibujar gráficos
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

    # Programar la próxima actualización
    root.after(500, update_plot, root, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas)

def create_plot_screen(root, window_geometry):
    window = tk.Toplevel(root)
    window.geometry(window_geometry)
    window.title('Motor Data Visualization')

    # Listas para almacenar datos
    positions = []
    currents = []
    intensities = []
    voltages = []
    torques = []

    # Crear los gráficos
    fig_position, position_ax = plt.subplots()
    position_canvas = FigureCanvasTkAgg(fig_position, master=window)
    position_canvas.get_tk_widget().pack()

    fig_current, current_ax = plt.subplots()
    current_canvas = FigureCanvasTkAgg(fig_current, master=window)
    current_canvas.get_tk_widget().pack()

    fig_intensity, intensity_ax = plt.subplots()
    intensity_canvas = FigureCanvasTkAgg(fig_intensity, master=window)
    intensity_canvas.get_tk_widget().pack()

    fig_voltage, voltage_ax = plt.subplots()
    voltage_canvas = FigureCanvasTkAgg(fig_voltage, master=window)
    voltage_canvas.get_tk_widget().pack()

    fig_torque, torque_ax = plt.subplots()
    torque_canvas = FigureCanvasTkAgg(fig_torque, master=window)
    torque_canvas.get_tk_widget().pack()

    # Crear etiquetas para mostrar datos
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

    # Iniciar la actualización de gráficos
    update_plot(window, position_label, position2_label, intensity_label, voltage_label, torque_label, positions, currents, intensities, voltages, torques, position_ax, current_ax, intensity_ax, voltage_ax, torque_ax, position_canvas, current_canvas, intensity_canvas, voltage_canvas, torque_canvas)

    return window
