
import sys
sys.path.append('../')  # Canvia aquesta ruta amb la ubicació real

from Functions.structuring_json import processar_json as processar_json
# Exemple d'ús de la funció amb el teu JSON
json_input = {
    "N_inputs": [
        {
            "time": "5",
            "Dx": "10",
            "N": "10"
        },
        {
            "time": "2",
            "Dx": "0",
            "N": "5"
        },
        {
            "time": "2",
            "Dx": "0",
            "N": "0"
        }
    ],
    "Triggers": [
        {
            "Pos": "1",
            "Trigger": "1"
        }
    ]
}

Dx, time, N, Trigger = processar_json(json_input)

print("Dx:", Dx)
print("time:", time)
print("N:", N)
print("Trigger:", Trigger)
