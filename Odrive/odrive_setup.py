import odrive
from odrive.enums import *
import time
import threading


def setup_odrive():
    print("Finding an ODrive...")
    my_drive = odrive.find_any()

    print("Starting calibration...")
    my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while my_drive.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    my_drive.axis1.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
    my_drive.axis1.trap_traj.config.vel_limit = 50
    my_drive.axis1.trap_traj.config.accel_limit = 50
    my_drive.axis1.trap_traj.config.decel_limit = 50
    my_drive.axis1.motor.config.current_lim = 30
    my_drive.axis1.controller.config.vel_limit = 50

    my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    my_drive.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
    my_drive.axis0.trap_traj.config.vel_limit = 50
    my_drive.axis0.trap_traj.config.accel_limit = 50
    my_drive.axis0.trap_traj.config.decel_limit = 50
    my_drive.axis0.motor.config.current_lim = 30
    my_drive.axis0.controller.config.vel_limit = 50

    return my_drive

trigger_twistandtrac_list = []

def execute_movement_sequences(Dx, time_delays, N, Trigger = [-1]):
    my_drive = odrive.find_any()

    # Funció per comprovar l'estat i la posició del motor
    def check_motor_position(setpoint):
        current_state = "AXIS_STATE_CLOSED_LOOP_CONTROL" # Suposa que això és l'estat actual del motor
        position = setpoint  # Suposa que aquesta és la posició actual del motor
        if current_state == "AXIS_STATE_CLOSED_LOOP_CONTROL":
            if abs(position - setpoint) < 0.05:
                print("El motor ha llegado a la posición deseada.")
                return True
            else:
                pass
        else:
            print("El motor no está en control en bucle cerrado.")
        return False

    # Bucle per processar les llistes
    for i in range(len(Dx)):
        # Esperar segons el que indica time_delays
        time.sleep(float(time_delays[i]))

        # Enviar l'ordre al dispositiu
        my_drive.axis1.controller.input_pos = float(Dx[i])
        my_drive.axis0.controller.input_pos = float(N[i])

        # Esperar fins que el motor arribi a la posició desitjada
        setpoint = float(Dx[i])  # o el valor que sigui pertinent
        while not check_motor_position(setpoint):
            time.sleep(0.1)  # Esperar un curta estona abans de comprovar de nou

        # Comprovar el valor de Trigger
        if Trigger[i] != -1:
            trigger_time = abs(float(Trigger[i]))  # Usar el valor absolut per a temps de espera
            time.sleep(trigger_time)
            print("Trigger tirat")
            global trigger_twistandtrac_list
            trigger_twistandtrac_list.append(time.time()) 

trigger_twist_list = []

def execute_rotation_positions(data):
    my_drive = odrive.find_any()
    time_pause = float(data["Time pause:"])
    cycles = int(data["Cicles:"])
    trigger_duration = float(data["Trigger"])

    # Obtenir totes les claus de posicions
    position_keys = [key for key in data if key.startswith("Position")]

    for cycle in range(cycles):
        print(f"Iniciant el cicle {cycle + 1}/{cycles}")

        for key in position_keys:
            position = float(data[key])
            print(f"Enviant l'eix a la posició {position}")
            # Enviar la comanda al dispositiu
            my_drive.axis0.controller.input_pos = position

            # Esperar la meitat del temps de pausa
            time.sleep(time_pause / 2)

            # Executar el trigger aquí si és necessari
            print("Executant el trigger")
            global trigger_twist_list
            trigger_twist_list.append(time.time()) 
            # Suposem que executar el trigger és una funció que pots cridar
            # execute_trigger(trigger_duration)

            # Esperar la meitat restant del temps de pausa
            time.sleep(time_pause / 2)

        print(f"Cicle {cycle + 1}/{cycles} completat")


# Lista global para almacenar los tiempos de disparo de los triggers
trigger_times_list = []

def execute_trigger(trigger_time, trigger_name):
    time.sleep(trigger_time)
    global trigger_times_list
    trigger_times_list.append(time.time())  # Añade el tiempo actual a la lista
    print(f"Trigger {trigger_name} fired at {trigger_time} seconds")

def execute_traction_movement(data):
    my_drive = odrive.find_any()

    cycles = int(data["Cicles:"])

    # Obtenir les pauses i distàncies
    pauses = [int(data[key]) for key in data if key.startswith("Pause")]
    distances = [float(data[key]) for key in data if key.startswith("Distance")]

    # Obtenir els triggers i ordenar-los pel temps de trigger
    triggers = {int(data[key]): key for key in data if key.startswith("Trigger")}
    trigger_times = sorted(triggers.keys())

    # Iniciar els triggers com a fils d'execució independents
    for trigger_time in trigger_times:
        trigger_name = triggers[trigger_time]
        threading.Thread(target=execute_trigger, args=(trigger_time, trigger_name)).start()

    # Executar els cicles de moviment
    for cycle in range(cycles):
        print(f"Starting cycle {cycle + 1}")
        for pause, distance in zip(pauses, distances):
            print(f"Pausing for {pause} seconds")
            time.sleep(pause)  # Pause before moving
            print(f"Moving to distance {distance}")
            my_drive.axis1.controller.input_pos = distance  # Move to the specified distance

        print(f"Cycle {cycle + 1} completed")


def get_motor1_data():
    my_drive = odrive.find_any()
    # Reemplaza esta sección con tu código para obtener datos reales del motor/dispositivo
    position = my_drive.axis1.encoder.pos_estimate
    position2 = my_drive.axis1.motor.I_bus
    intensity = my_drive.axis1.motor.current_control.Iq_measured
    voltage = my_drive.vbus_voltage
    torque = ((8.27*my_drive.axis1.motor.current_control.Iq_setpoint/150) * 100)
    return position, position2,voltage, intensity, torque

def get_motor0_data():
    my_drive = odrive.find_any()
    # Reemplaza esta sección con tu código para obtener datos reales del motor/dispositivo
    position = my_drive.axis0.encoder.pos_estimate
    position2 = my_drive.axis0.motor.I_bus
    intensity = my_drive.axis0.motor.current_control.Iq_measured
    voltage = my_drive.vbus_voltage
    torque = ((8.27*my_drive.axis0.motor.current_control.Iq_setpoint/270) * 100)
    return position, position2,voltage, intensity, torque