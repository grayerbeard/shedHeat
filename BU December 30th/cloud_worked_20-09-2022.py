# Standard library imports
from time import sleep as time_sleep
from os import path
import datetime
from sys import exit as sys_exit
#from subprocess import callpython -m pip install tinytuya
		
import tinytuya

# Connect to Tuya Cloud
c = tinytuya.Cloud()  # uses tinytuya.json 

print("\n","@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@","\n")


# Display list of devicesapiKey
devices = c.getdevices()
print("Device List: %r" % devices)
print("\n""\n")
# Select a Device ID to Test
#
id = "bf5723e4b65de4a64fteqz"

# Display Properties of Device
result = c.getproperties(id)
print("Properties of Switch 1:\n", result)
print("\n""\n")
# Display Status of Device
result = c.getstatus(id)
print("Status of Switch 1:\n", result)
print("\n""\n")



id = "bf6f1291cc4b30aa8d1wsv" # Code for sensor
# Display Properties of Device
result = c.getproperties(id)
print("Properties of T & H Sensor:\n", result)
print("\n""\n")
# Display Status of Device
result = c.getstatus(id)
print("Status of T & H Sensor:\n", result)
print("\n""\n")

print("@@@@@@@@@@@@@@@@@")
for sub in result:
	print(sub)
print(result['result'][0]['value'])
print("@@@@@@@@@@@@@@@@@")      
    
id = "bf5723e4b65de4a64fteqz" # Code for switch

# Send Command - Turn on switch
commands = {
	'commands': [{
		'code': 'switch_1',
		'value': True
	}, {
		'code': 'countdown_1',
		'value': 0
	}]
}
print("Sending command...")
result = c.sendcommand(id,commands)
print("Results\n:", result)

time_sleep(10) 
#sys_exit()

# Send Command - Turn on switch
commands = {
	'commands': [{
		'code': 'switch_1',
		'value': False
	}, {
		'code': 'countdown_1',
		'value': 0
	}]
}
print("Sending command...")
result = c.sendcommand(id,commands)
print("Results\n:", result)
