import odrive
from odrive.enums import *
import time
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
import Odrive.odrive_setup
from Odrive.odrive_setup import setup_odrive as setup_odrive
from Odrive.odrive_setup import execute_movement_sequences as execute_movement_sequences

setup_odrive()
# Les teves llistes d'entrades
Dx = ['10', '0', '0']
time_delays = ['5', '2', '2']
N = ['10', '5', '0']
Trigger = ['1', '-1', '-1']

# Execució de la seqüència de moviments
execute_movement_sequences(Dx, time_delays, N, Trigger)