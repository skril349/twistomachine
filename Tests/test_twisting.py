import odrive
from odrive.enums import *
import time
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
import Odrive.odrive_setup
from Odrive.odrive_setup import setup_odrive as setup_odrive
from Odrive.odrive_setup import execute_rotation_positions as execute_rotation_positions

# Dades d'entrada
data = {
    "Time pause:": "10",
    "Cicles:": "3",
    "Trigger": "5.0",
    "Position 1": "2",
    "Position 2": "8",
    "Position 3": "10",
    "Position 4": "8"
}
setup_odrive()
execute_rotation_positions(data)