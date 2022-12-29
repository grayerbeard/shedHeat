#!/usr/bin/env python3
# This is for controlling Room Temperature
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the OnTimeGNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :shedHeat.py based on tankTemp.py
# description     :For controlling Room Temperature so as to minimise heating costs
# author          :David Torrens
# start date      :2022 10 04
# version         :0.1 October 2022
# python_version  :3

# Standard library imports
from time import sleep as timeSleep
from os import path
from datetime import datetime
from sys import exit as sys_exit
from subprocess import call
import numpy as np
import json

# Third party imports
# None
# Local application imports
from configHp import class_config
from schedule import class_schedule
from text_buffer import class_text_buffer
from utility import prd as debugPrint
from utility import makeTimeText
# Note use of sensor_test possible on next line
from sensor import class_sensors
from tuyaCloud import class_tuyaCloud
#Set up Config file and read it in if present



config = class_config("configHp.cfg")
dHp = config.deviceNumberHp
dHtrs = config.deviceNumberHeaters
dTempTH = []
dTempTH.append(config.deviceNumberTemp1)
dTempTH.append(config.deviceNumberTemp2)
dTempTH.append(config.deviceNumberTemp3)
dTempTH.append(config.deviceNumberTemp4)

debug = config.debug

config.scan_count = 0
baseHeat = 5
schedule = class_schedule(config,baseHeat)

sensor = class_sensors()
cloud = class_tuyaCloud(config)

logTime= datetime.now()
heatersTurnOnTime = logTime
heatersTurnOffTime = logTime
hpTurnOnTime  = logTime
hpTurnOffTime = logTime
logType = "log"
logBuffer = class_text_buffer(config,logType,logTime)


# Set The Initial Conditions
the_end_time = datetime.now()
loop_time = 0
correction = 7.5
# Ensure start right by inc buffer

if config.scan_delay > 9:
	refresh_time = config.scan_delay
else:
	refresh_time = 2*config.scan_delay

# Check Heaters Switch

#print( "\n\n","Status at start : ",json.dumps(cloud.devicesStatus[dHtrs]), "\n\n")

if config.doTest:
	print(json.dumps(cloud.devicesStatus,indent = 4))
	print("Heater: ",cloud.devicesStatus[dHtrs]["switch_1"])
	if cloud.amendCommands(dHtrs,"switch_1",'True'): # Check if worked
		success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
		if success:
			print("Heaters should be on for five seconds")
		else:
			print( success,stSuccess,failReason)
	else: # Print failed and stop
		print ("amend command failed 95")
		sys_exit()
	
	stSuccess,failReason,devicesStatus,excRep = cloud.getStatus()
	if len(excRep) > 0:
		print(excRep)
		reason += str(excRep[0])

	if stSuccess:
		print( "\n\n","Status at after switch on : ",json.dumps(cloud.devicesStatus), "\n\n")
	else:
		print(stSuccess,reason)

	print("Heaters should be on for ten Seconds")
	print("Heater: ",cloud.devicesStatus[dHtrs]["switch_1"])

	timeSleep(2)
	
	if cloud.amendCommands(dHtrs,"switch_1",'False'): # Check if worked

		success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
		#print( success,stSuccess,failReason)
		if success:
			print("Now heaters should be off")
		else:
			print( success,stSuccess,failReason)
	else: # Print failed and stop
		print ("amend command failed 101")
		sys_exit()


	stSuccess,failReason,devicesStatus,excRep = cloud.getStatus()
	if len(excRep) > 0:
		print(excRep)
		reason += str(excRep[0])
	if stSuccess:
		print( "\n\n","AfterdHtr Switch Off : ",json.dumps(cloud.devicesStatus), "\n\n")
	else:
		print(stSuccess,failReason)

	print("Heater: ",cloud.devicesStatus[dHtrs]["switch_1"])

	#sys_exit()

	
	# Check operation of Heat Pump Switch
	
	if cloud.amendCommands(dHp,"switch",'True'):
		success,stSuccess,failReason = cloud.upDateDevice(dHp)
		if success:
			print( "Heat Pump should be on for 10 seconds")
		else:
			print( success,stSuccess,failReason)
	else: # Print failed and stop
		print ("amend command failed 113")
		sys_exit()

	stSuccess,failReason,devicesStatus,excRep = cloud.getStatus()
	if len(excRep) > 0:
		print(excRep)
		reason += str(excRep[0])
	if stSuccess:
		print( "\n\n","After dHp Switch On : ",json.dumps(cloud.devicesStatus), "\n\n")
	else:
		print(stSuccess,failReason)

	timeSleep(10)
	
	
	if cloud.amendCommands(dHp,"switch", 'False'):
		success,stSuccess,failReason = cloud.upDateDevice(dHp)
		#
		if success:
			print( "Now Heat Pump should be off")
		else:
			print( success,stSuccess,failReason)
	else: # Print failed and stop
		print ("amend command failed 113")
		sys_exit()

	stSuccess,failReason,devicesStatus,excRep = cloud.getStatus()
	if len(excRep) > 0:
		print(excRep)
		reason += str(excRep[0])
	if stSuccess:
		print( "\n\n","After dHp Switch Off : ",json.dumps(cloud.devicesStatus), "\n\n")
	else:
		print(stSuccess,failReason)
		sys_exit()

if config.doTest:
	print("Test Completed, will stop")	
	sys_exit()

programTemp = 0
increment = True
changeRate = 0
#lastTemp,tries = sensor.getTemp()
lastTemp = 0
lastDayInWeek = -1
getTheTempError = False
lastLogTime = logTime
hpTurnOffTime = logTime
heatersTurnOffTime = logTime
predictedTemp = 0
overRun = False
overRunLogCount = 0
tries = 0  # NOT being set at the moment
sensor.errorCount = 0 # NOT being set at the moment



#tempMeasureErrorCount = 0
#maxTries = 0
#triesCount = 0
#getTheTempErrorCount = 0

message = ""
reason = ""
tempFailCount = 0

while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
	try:
		# Sort out Time in Day and Day in week etc
		logTime= datetime.now()
		dayInWeek = logTime.weekday()
		hourInDay = logTime.hour + (logTime.minute/60)
		shedStatus,desiredTemp,targetHp,targetHeaters = schedule.calcTargets(hourInDay,dayInWeek)
		message += shedStatus
		if dayInWeek != lastDayInWeek:
			totalHeatersOnTime = 0
			totalHpOnTime = 0

		if targetHeaters != 0:
			if cloud.devicesStatus[dHtrs]["switch_1"]:
				targetHeaters += config.hysteresis
			else:
				targetHeaters -= config.hysteresis

		if targetHp != 0:	
			if cloud.devicesStatus[dHp]["switch"]:
				targetHp += config.hysteresis
			else:
				targetHp -= config.hysteresis
		#reason + ????
		# Do Control
		startGetTemp = datetime.now()
		temperatures,excRep,numberFound = sensor.getTemp()
		if len(excRep) > 0:
			reason += str(excRep[0])
			print(excRep)
		if debug:
			print("temperatures :",temperatures)
		stSuccess,failReason,devicesStatus,excRep = cloud.getStatus()
		if len(excRep) > 0:
			print("excRep: ",excRep)
			reason += str(excRep[0])
			print("failReason: ",failReason)
			increment = True
		for deviceFailReason in failReason:
			reason += deviceFailReason
			if len(deviceFailReason) > 1:
				increment = True
		tempTH = []
		humidityTH = []
		batteryTH = []
		for indTH in range(0,len(dTempTH)):
			if stSuccess[dTempTH[indTH]]:
				tempTH.append(devicesStatus[dTempTH[indTH]]["va_temperature"]/10)
				humidityTH.append(devicesStatus[dTempTH[indTH]]["va_humidity"])
				batteryTH.append(devicesStatus[dTempTH[indTH]]["battery_state"])
				if debug:
					print(indTH,dTempTH[indTH],tempTH[indTH],humidityTH[indTH],batteryTH[indTH])
			else:
				tempTH.append(-99)
				humidityTH.append(-99)
				batteryTH.append(-99)
		#print(tempTH,humidityTH,batteryTH)
		batteries = ""
		for battery in batteryTH:
			if type(battery)  != type("cat"):
				batteries += " " + str(battery) + "TYPE ERROR"
			else:
				batteries += " " + battery 

		otherTemp = tempTH

		temp = temperatures[config.sensorRoomTemp]

		if config.scan_count < 2:
			lastTemp = temp


		if type(temp) != type(1.1):
			temp = -1
			print("Temperature reading not a float")

		if temp < 0 : # No Sensor Connected
			tempFailCount += 1
		if (temp < 0) and (tempFailCount > 5):

			print("no Sensor connected will turn heaters Off")

			if cloud.amendCommands(dHtrs,"switch_1",'False'):
				success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
				#print( success,stSuccess,failReason)
				if not(success):
					print("Reason : ",failReason)
				print("Now heaters should be off")
			else:
				print("amend command fault")
	
			if cloud.amendCommands(dHp,"switch",'False'):
				success,stSuccess,failReason = cloud.upDateDevice(dHp)
				#print( success,stSuccess,failReason)
				if not(success):
					print("Reason : ",failReason)
				print("Now HP should be off")
			else:
				print("amend command fault")
			sys_exit()
		else:
			tempFailCount = 0
			tempChange = (temp - lastTemp)*config.scan_delay/60 # degrees per minute
			changeRate = changeRate + (0.1 * (tempChange - changeRate))
			if abs(changeRate) * 3 > 2:
				changeRate = changeRate * 0.95
				message += " RR" + str(round(changeRate,3)) + ", "
				#print( "changeRate reduced : ",changeRate)
				increment = True
				reason += "01ChangeRateReduced"
				print("Reason: ",reason)
				
			predictedTemp = temp + (3 * changeRate)
			lastTemp = temp

			if predictedTemp >= targetHeaters:
				#print("Heater Status: ",cloud.devicesStatus[dHtrs]["switch_1"])
				#print("Heaters predictedTemp and targetHeaters heater OFF? : ",predictedTemp,targetHeaters)

				if cloud.devicesStatus[dHtrs]["switch_1"] : # This is a change from ON to OFF
					heatersTurnOffTime = logTime
					heatersOnTime = (heatersTurnOffTime - heatersTurnOnTime).total_seconds() / 60.0
					totalHeatersOnTime += heatersOnTime
					increment = True
					reason += "02deviceNumberHpheaters Off,"
					print("Reason: ",reason)
					message += "htrs off after " + str(round(heatersOnTime,2))

				if cloud.amendCommands(dHtrs,"switch_1",'False'):
					success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
					if not(success and stSuccess):
						increment = True
						reason += failReason + " ##6 "
						print("Reason: ",reason)
				else:
					print("amend command fault")
			else:
				print("Heater Status: ",cloud.devicesStatus[dHtrs]["switch_1"])
				print("Heaters predictedTemp and targetHeaters heater Off? : ",predictedTemp,targetHeaters)
				if not cloud.devicesStatus[dHtrs]["switch_1"]  : # This is a change from OFF to ON
					#print("Temp < Target so turn heaters ON")
					heatersTurnOnTime = logTime
					heatersOffTime = (heatersTurnOnTime - heatersTurnOffTime).total_seconds() / 60.0
					increment = True
					reason += "03heatersON"
					print("Reason: ",reason)
					message += "htrs on after " + str(round(heatersOffTime,2))

				if cloud.amendCommands(dHtrs,"switch_1",'True'):
					success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
					if not(success and stSuccess):
						increment = True
						reason += failReason + " ##7 "
						print("Reason: ",reason)
				else:
					print("amend command fault")

			if predictedTemp >= targetHp:

				if cloud.devicesStatus[dHp]["switch"] : # This is a change from ON to OFF
					hpTurnOffTime = logTime
					hpOnTime = (hpTurnOffTime - hpTurnOnTime).total_seconds() / 60.0
					totalHpOnTime += hpOnTime
					increment = True
					reason += "04deviceNumberHphp Off,"
					print("Reason: ",reason)
					message += "05HP off after " + str(round(hpOnTime,2))

				if cloud.amendCommands(dHp,"switch",'False'):
					success,stSuccess,failReason = cloud.upDateDevice(dHp)
					if not(success and stSuccess):
						increment = True
						reason += failReason + " ##8 "
						print("Reason : ",reason)
				else:
					print("amend command fault")
			else:
				if not cloud.devicesStatus[dHp]["switch"] : # This is a change from OFF to ON
					#print("Temp < Target so turn hp ON")
					hpTurnOnTime = logTime
					hpOffTime = (hpTurnOnTime - hpTurnOffTime).total_seconds() / 60.0
					increment = True
					reason += "hpON"
					print("Reason: ",reason)
					message += "htrs on after " + str(round(hpOffTime,2))
				if cloud.amendCommands(dHp,"switch",'True'):
					success,stSuccess,failReason = cloud.upDateDevice(dHp)
					if not(success and stSuccess):
						increment = True
						reason += failReason  + " ##9 "
						print("Reason: ",reason)
				else:
					print("amend command fault")

#Time, Hour in Day,Room Temp,Battery,Per 10 Mins,Predicted Temp,Heaters Target Temp,HP Target Temp,
# HP In,HP Out,Lower Work,High Clock,Outside,Heaters Status,HP Status,Total Heaters,Total HP,Reason,Message
		# Do Logging
		#" Room Temp","Target Temp","heaters Status","Message"]
		logBuffer.lineValues["Time"] =makeTimeText(logTime)
		logBuffer.lineValues["Hour in Day"] =  round(hourInDay,2)
		logBuffer.lineValues["Room Temp"] = round(temperatures[config.sensorRoomTemp],2)
		logBuffer.lineValues["Battery"] = batteries
		logBuffer.lineValues["Per 10 Mins"] = round(changeRate*10*60/config.scan_delay,2)
		logBuffer.lineValues["Predicted Temp"] = round(predictedTemp,2)
		logBuffer.lineValues["Heaters Target Temp"] = round(targetHeaters,2)
		logBuffer.lineValues["HP Target Temp"] = round(targetHp,2)
		logBuffer.lineValues["HP In"] =  round(tempTH[2],2)
		logBuffer.lineValues["HP Out"] = round(tempTH[3],2)
		logBuffer.lineValues["Lower Work"] = round(tempTH[0],2)
		logBuffer.lineValues["High Clock"] = round(tempTH[1],2)
		logBuffer.lineValues["Outside"] = round(temperatures[config.sensorOutside],2)
		
		if cloud.devicesStatus[dHtrs]["switch_1"]:
			logBuffer.lineValues["Heaters Status"] = "ON"
		else:
			logBuffer.lineValues["Heaters Status"] = "OFF"
		#print("Heaters Status: ",logBuffer.lineValues["Heaters Status"],"\n",cloud.devicesStatus[dHtrs],"\n")
		if cloud.devicesStatus[dHp]["switch"]:
			logBuffer.lineValues["HP Status"] = "ON"
		else:
			logBuffer.lineValues["HP Status"] = "OFF"
		#print("Heaters status :",logBuffer.lineValues["HP Status"],"\n",cloud.devicesStatus[dHp],"\n")
		logBuffer.lineValues["Total Heaters"] = round(totalHeatersOnTime,2)
		logBuffer.lineValues["Total HP"] = round(totalHpOnTime,2)

		#Ensure logs at least every config.mustLog minutes 
		timeSinceLog = (logTime - lastLogTime).total_seconds() / 60.0

		if timeSinceLog > config.mustLog - (config.scan_delay/120):
			lastLogTime = logTime
			
			increment = True
			reason += " MustLog, "
			print(reason)
			
		if (config.scan_count < 5): 
			increment = True
			reason += "start "
			debugPrint(debug,"Reason: ",reason)


		logBuffer.lineValues["Reason"] = reason
		logBuffer.lineValues["Message"] = message

		#next for debug
		#print("count : ",config.scan_count," Increment : ",increment)

		logBuffer.pr(increment,0,logTime,refresh_time)
		increment = False
		reason = ""
		message = ""

		# Loop Managemnt
		loop_end_time = datetime.now()
		loop_time = (loop_end_time - logTime).total_seconds()
		config.scan_count += 1
		
		# Adjust the sleep time to aceive the target loop time and apply
		# with a slow acting correction added in to gradually improve accuracy
		if loop_time < (config.scan_delay - (correction/1000)):
			sleep_time = config.scan_delay - loop_time - (correction/1000)
			try:
				timeSleep(sleep_time)
			except KeyboardInterrupt:
				print(".........Ctrl+C pressed... Output Off 288")
				print("Switching off heaters")

				commands = {"commands": {"code": "switch_1", "value": false}}

				if cloud.amendCommands(dHtrs,"switch_1",'False'):
					success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
					if not(success and stSuccess):
						reason += failReason + " ##10 "
						print("Reason : ",reason)
					print("Now heaters should be off")
				else:
					print("amend command fault")
	
				if cloud.amendCommands(dHp,"switch",'False'):
					success,stSuccess,failReason = cloud.upDateDevice(dHp)
					if not(success and stSuccess):
						reason += failReason + " ##11 "
						print("Reason : ",reason)
					print("Now Heat Pump should be off")
				else:
					print("amend command fault")

				timeSleep(10)
				sys_exit()

			except ValueError:
				print("sleep_Time Error value is: ",sleep_time, "loop_time: ",
				      loop_time,"correction/1000 : ",correction/1000)
				print("Will do sleep using config.scan_delay and reset correction to 7.5msec")
				correction = 7.5
				timeSleep(config.scan_delay)
			except Exception:
				print("some other error with timeSleep try with config.scan_delay")
				timeSleep(config.scan_delay) 
		else:
			timeSleep(config.scan_delay)
		last_end = the_end_time
		the_end_time = datetime.now()
		last_total = (the_end_time - last_end).total_seconds()
		error = 1000*(last_total - config.scan_delay)
		if error > 250*(config.scan_delay):
			print("Large Error ignored it was : ",error)
		else:
			correction = correction + (0.15*error)
			# Following for looking at error correctoion
			# print("Error correcting OK, Error : ",error,"  Correction : ", correction)

	except KeyboardInterrupt:

		print(".........Ctrl+C pressed... Output Off321") 

		if cloud.amendCommands(dHtrs,"switch_1",'False'):
			success,stSuccess,failReason = cloud.upDateDevice(dHtrs)
			if not(success and stSuccess):
				print("Reason : ",failReason)
			
			print("Now heaters should be off")
		else:
			print("amend command fault")

		if cloud.amendCommands(dHp,"switch",'False'):
			success,stSuccess,failReason = cloud.upDateDevice(dHp)
			if not(success and stSuccess):
				print("Reason : ",failReason)
			print("Now Heat Pump should be off")
		else:
			print("amend command fault")

		timeSleep(10)

		sys_exit()

	
