# Standard library imports
from time import sleep as time_sleep
from os import path
import datetime
from sys import exit as sys_exit
from operator import itemgetter
#from subprocess import callpython -m pip install tinytuya
		
import tinytuya

class class_tuyaCloud:
	def __init__(self):
		self.cloud = tinytuya.Cloud()  # uses tinytuya.json
		#self. = 

	def listDevices(self):
		# Display list of devicesapiKey
		devices = self.cloud.getdevices()
		print("Device List: %r" % devices)
		print("\n""\n")

	def deviceProperties(self,id):
		# Display Properties of Device
		result = self.cloud.getproperties(id)
		print("Properties of Device:\n", result)
		print("\n""\n")

	def deviceStatus(self,id):
		# Display Status of DeviceStauts
		result = self.cloud.getstatus(id)
		print("Status of Device:\n", result)
		print("\n""\n")

	def operateSwitch(self,id,code,on):    # Send Command - Turn on switch
		commands = {
			'commands': [{
				'code': code,
				'value': on
			}, {
				'code': 'countdown_1',
				'value': 0
			}]
		}
		checkResult = self.cloud.sendcommand(id,commands)
		successfulResult = result['success']
		if on and successfulResult:
			heaterOn = True

		return heaterOn, successfulResult
		#status = self.cloud.getstatus(id)
		#print("Results\n:", result)
		#if result['success']:
		#	print("Worked")
		#else:
		#	print("Failed")
		#print("Status\n", status)
		#print("status['result'] : ",status['result'])
		#values = list(map(itemgetter('value'), status['result']))
		#codes = list(map(itemgetter('code'), status['result']))
		#print("\n")
		#for index in range(len(codes)):
		#	print(code[index] ," is ",values[index])


# test routine rin when script run direct
if __name__ == '__main__':
	cloud = class_tuyaCloud()
	#cloud.listDevices()
	id = "bf5723e4b65de4a64fteqz"  
	#cloud.deviceProperties(id)
	#cloud.deviceStatus(id)
	#cloud.operateSwitch(id,"switch_1",True)
	#time_sleep(20)
	if cloud.operateSwitch(id,"switch_1",False):
		print("worked ok")
	else:
		Print("failed")
