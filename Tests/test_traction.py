
import odrive
from odrive.enums import *
import time
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real
import Odrive.odrive_setup
from Odrive.odrive_setup import setup_odrive as setup_odrive
from Odrive.odrive_setup import execute_traction_movement as execute_traction_movement

# Dades d'entrada
data = {
    "Pause 1:": "2",
    "Distance 1:": "6",
    "Pause2:": "2",
    "Distance 2:": "0",
    "Cicles:": "3",
    "Trigger 1": "2",
    "Trigger 2": "5",
    "Trigger 3": "8"
}
setup_odrive()
execute_traction_movement(data)