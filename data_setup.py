import ujson as json

led_state = False # inintialize led_state as 0
jsonData = {"stateKey": led_state} # Initialize a JSON literal

try:
    with open('savedata.json', 'w') as f:
        json.dump(jsonData, f)
except:
        print("Error! Could not save")