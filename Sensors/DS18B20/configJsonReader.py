import json

with open('sensor-config.json') as config_file:
    data = json.load(config_file)

for sensor in data['sensorGroup']:
    print(sensor['deviceId'])


# width = data['prop']
# other = data['arrayProp']
# other2 = data['arrayProp2']

# print(width)
# print(other[0])
# print(other2)
