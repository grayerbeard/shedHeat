# Standard library imports
from time import sleep as time_sleep
from os import path
import datetime
from sys import exit as sys_exit
from operator import itemgetter
#from subprocess import callpython -m pip install tinytuya
		
import tinytuya

class class_tuyaCloud:
	def __init__(self,numberSwitches,names,ids,codes):
		self.cloud = tinytuya.Cloud()  # uses tinytuya.json
		self.lastSwitchOn = [False]*numberSwitches
		self.ids = ids
		self.codes = codes
		self.names = names

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

	def operateSwitch(self,switchNumber,stateWanted):    # Send Command - Turn on switch

		# Assume online until get bad result and offline confirmed
		printMessage =  ""
		reason = ""
		opFail = False

		commands = {
			'commands': [{
				'code': self.codes[switchNumber],
				'value': stateWanted
			}, {
				'code': 'countdown_1',
				'value': 0
			}]
		}
		successfullResult = False
		try:
			checkResult = self.cloud.sendcommand(self.ids[switchNumber],commands)
			successfullResult = checkResult['success']
			if checkResult.get('msg','device is online') == 'device is offline':
				opFail = True
				reason += names[switchNumber] + " is offLine"
		except:	
			printMessage += "Cloud Send Command Fail"
			reason += "Cloud Send Command Fail"
			opFail = True

		if successfullResult:
			switchOn = stateWanted
			self.lastSwitchOn[switchNumber] = switchOn
			if stateWanted:
				printMessage += " Switch on OK " + self.names[switchNumber]
			else:
				printMessage += " Switch off OK "+ self.names[switchNumber]
		else:
			# not successful so return last known state and error flag
			switchOn = self.lastSwitchOn[switchNumber]
		return switchOn,opFail,printMessage,reason

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))














# test routine rin when script run direct
if __name__ == '__main__':
	# change this to suite number of switches.
	numberSwitches = 2 # one power switch and one heat pump

	# set up the class	
	cloud = class_tuyaCloud(numberSwitches)

	# uncomment line below to get list of devices
	#cloud.listDevices()

	# uncomment three lines below and set id to check a particular device 
	#id = "bf5723e4b65de4a64fteqz"  
	#cloud.deviceProperties(id)
	#cloud.deviceStatus(id)

	# uncomment three lines below and set id to check a particular device 
	#id = "01303121a4e57cb7ca0c"  
	#cloud.deviceProperties(id)
	#cloud.deviceStatus(id)	


	# test power switch that has a switch code of "switch_1"
	# Using id found from print out doing above
	# note we use switchNumber 0

	print("Test power switch")

	switchNumber = 0
	id = "bf5723e4b65de4a64fteqz"
	code = "switch_1"

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")
	time_sleep(5)

	stateWanted = True
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")
	time_sleep(5)

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")	
		if offLine:
			print("Device is Offline")

	# test power on off of heat pump that has power switch code of "switch"
	# Using id found from print out doing above
	# note we use switchNumber 1

	print("Test power switch on/off of Heat Pump")

	switchNumber = 1
	id = "01303121a4e57cb7ca0c"
	code = "switch"
	stateWanted = False

	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")

	time_sleep(5)

	stateWanted = True
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")

		if offLine:
			print("Device is Offline")

	time_sleep(20)

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")	
		if offLine:
			print("Device is Offline")
