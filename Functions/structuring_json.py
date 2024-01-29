import json

def processar_json(json_input):
    Dx_list = []
    time_list = []
    N_list = []
    Trigger_list = []

    for input_data in json_input.get("N_inputs", []):
        Dx_list.append(input_data.get("Dx"))
        time_list.append(input_data.get("time"))
        N_list.append(input_data.get("N"))

    triggers = json_input.get("Triggers", [])
    if triggers:
        trigger_values = [-1] * len(Dx_list)
        for trigger in triggers:
            pos = int(trigger.get("Pos", 0)) - 1
            if 0 <= pos < len(trigger_values):
                trigger_values[pos] = trigger.get("Trigger")
        Trigger_list = trigger_values
    else:
        Trigger_list = [-1] * len(Dx_list)
    return Dx_list, time_list, N_list, Trigger_list
