# Standard library imports
from time import sleep as time_sleep
from os import path
from datetime import datetime
from sys import exit as sys_exit
from operator import itemgetter
import json
from configHp import class_config
#from subprocess import callpython -m pip install tinytuya
		
import tinytuya
class class_tuyaCloud:
	def __init__(self,names,ids): #,codes):
		self.cloud = tinytuya.Cloud()  # uses tinytuya.json
		self.lastSwitchOn = [False]*len(names)
		self.ids = ids
		#self.codes = codes
		self.names = names

	def sendCommands(self,device,commandPairs,start,end):    # Set to start up values

		# Assume online until get bad result and offline confirmed
		printMessage =  ""
		reason = ""
		success = [False]*(end-start+1)
		opFail = [True]*(end-start+1)
		stSuccess = [False]*(end-start+1)
		stOpFail = [True]*(end-start+1)
		for ind in range(start,end+1):
			commands = { 'commands' : commandPairs[ind]}
			dump = json.dumps(commands)
			print("Command : ",ind,"\n",dump)
			try:
				status = self.cloud.sendcommand(self.ids[device],commands)
				print("Status after Command Send : ","\n",status)
				success[ind] = status['success']
				if status.get('msg','device is online') == 'device is offline':
					opFail[ind] = True
					reason += self.names[device] + "is offLine"
				if not(success[ind]):
					opFail[ind] = True
			except:	
				printMessage += "Send Command fail"
				reason += "Send Command Failed"
				opFail = True
	
			try:
				id = self.ids[device]
				status = self.cloud.getstatus(id)
				dump = json.dumps(status)
				print("STATUS : ","\n",dump)
				stSuccess[ind] = status['success']
				if status.get('msg','device is online') == 'device is offline':
					stOpFail[ind] = True
					reason += self.names[device] + " is offLine"
				if not(stSuccess[ind]):
					stOpFail[ind] = True
			except:	
				printMessage += "Get Status fail"
				reason += "Get Status Fail"
				stOpFail = True
		return success,stSuccess,opFail,stOpFail,printMessage,reason


	def listDevices(self):
		# Display list of devicesapiKey
		devices = self.cloud.getdevices()
		print("Device List: %r" % devices)
		print("\n""\n")

	def deviceProperties(self,id):
		# Display Properties of Device
		properties = self.cloud.getproperties(id)
		print("Properties of Device:\n", properties)
		print("\n""\n")
		return properties

	def deviceStatus(self,id):
		# Display Status of DeviceStauts
		status = self.cloud.getstatus(id)
		#print("Status of Device:\n", status)
		#print("\n""\n")
		return status

	def getTH(self,id):
		status = self.cloud.getstatus(id)
		#print(status)
		temp = float(status['result'][0]['value'])/10
		humidity = float(status['result'][1]['value'])
		battery = status['result'][2]['value']
		#print("Temperaturs : ", temp, " Humidity : ",humidity, "  Battery : ",battery)
		return temp,humidity,battery

	def getHP(self,id):
		status = self.cloud.getstatus(id)
		if status["success"] == True:
			values = []
			codes = []
			for ind in range(len(status['result'])):
				values.append(status['result'][ind]['value'])
				codes.append(status['result'][ind]['code'])
			print("RValues : ",values,"  Codes : ",codes)
			switch = status['result'][0]['value']
			temp_set = int(status['result'][1]['value'])
			temp_current = int(status['result'][2]['value'])
			mode = status['result'][3]['value']
			windspeed = int(status['result'][4]['value'])
			c_f	= status['result'][5]['value']
			print("Switch : ", switch,"temp_set : ", temp_set, " temp_current : ",temp_current, "  mode : ",mode, "  windspeed : ",windspeed, "  c_f : ",c_f)
		else:
			print("Get Status Fail with message : ",status.get("msg","No message"))
			switch,temp_set,temp_current,mode,windspeed,c_f = "","","","","",""
		return switch,temp_set,temp_current,mode,windspeed,c_f

	#def operateSwitch(self,switchNumber,stateWanted):    # Send Command - Turn on switch

		# Assume online until get bad result and offline confirmed
		printMessage =  ""
		reason = ""
		opFail = False

		commands = {
			'commands': 	[
								{
								'code': self.codes[switchNumber],
								'value': stateWanted
								}, 
								{
								'code': 'countdown_1',
								'value': 0
								}
							]
					}
		successfullResult = False
		try:
			status = self.cloud.sendcommand(self.ids[switchNumber],commands)
			#print(status, "  :  ",status.get('msg','device is online'))
			success = status['success']
			if status.get('msg','device is online') == 'device is offline':
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
		print(status)
		return switchOn,opFail,printMessage,reason

#if __name__ == '__main__':
#    import sys
#    sys.exit(main(sys.argv)

# test routine rin when script run direct
if __name__ == '__main__':
	# change this to suite number of switches.
	# one power switch and one heat pump
	# set up the class
	config = class_config()
	config.scan_count = 0	
	cloud = class_tuyaCloud(config.names,config.ids)
	device = 1
	stateWanted = True
	temperatureWanted = 25
	codes = []	
	values = []
	commandPairs = []
	codes.append(config.codes0)
	codes.append(config.codes1)
	values.append(config.values0)
	values.append(config.values1)
	for device in range(0,2):
		commandPairs.append([])
		for ind  in range(len(codes[device])):
			commandPairs[device].append(dict(code = codes[device][ind],value = values[device][ind]))
		print(json.dumps(commandPairs[device],indent = 4))

	sys_exit()

	start = 1
	end = 3
	HPcommandPairs[0]["value"] = False
	HPcommandPairs[4]["value"] = 25

	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(device,HPcommandPairs,start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)

	start = 0
	end = 0	
	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(device,HPcommandPairs,start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)

	start = 4
	end = 4
	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(device,HPcommandPairs,start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)
	sys_exit()


	# uncomment line below to get list of devices
	#cloud.listDevices()
	
	# uncomment three lines below and set id to check a particular device 
	#cloud.deviceProperties(ids[1])
	#cloud.deviceStatus(id)

	# uncomment three lines below and set id to check a particular device 
	#id = 'bf6f1291cc4b30aa8d1wsv'
	#properties = cloud.deviceProperties(id)

	#switchOn,opFail,printMessage,reason = cloud.operateSwitch(1,False)
	 
	#properties = cloud.deviceProperties(id)
	
	#print("\n \n ")
	#print(status)
	#print("\n \n")
	
	#print(online)


	count = 0

	while count < 5  :
		#status = cloud.deviceStatus(id)
	# print("Properties:"	, propertiecommandPairss)
	# print("Status:",status)
		temp, humidity, battery = cloud.getTH(id)
		print(temp,humidity,battery)
		print(datetime.now())
		count += 1
		#time_sleep(10 * 60)
		print(count)

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
