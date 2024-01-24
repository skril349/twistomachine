import odrive
from odrive.enums import *
import time
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real

from Odrive.odrive_setup import setup_odrive as setup_odrive

# Les teves llistes d'entrades
Dx = ['10', '0', '0']
time_delays = ['5', '10', '10']
N = ['3', '5', '0']
Trigger = ['5', '-1', '-1']

setup_odrive()
my_drive = odrive.find_any()
# La funció per comprovar l'estat i la posició del motor
def check_motor_position(setpoint):
    # Aquí hauries de substituir aquesta part pel codi que obté l'estat real i la posició del motor
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
    my_drive.axis1.controller.input_pos = (float(Dx[i]))
    my_drive.axis0.controller.input_pos = (float(N[i]))

    # Esperar fins que el motor arribi a la posició desitjada
    setpoint = float(Dx[i])  # o el valor que sigui pertinent
    while not check_motor_position(setpoint):
        time.sleep(0.1)  # Esperar un curta estona abans de comprovar de nou

    # Comprovar el valor de Trigger
    if Trigger[i] != '-1':
        trigger_time = abs(float(Trigger[i]))  # Usar el valor absolut per a temps de espera
        time.sleep(trigger_time)
        print("Trigger tirat")