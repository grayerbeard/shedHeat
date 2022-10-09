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
from time import sleep as time_sleep
from os import path
from datetime import datetime
from sys import exit as sys_exit
from subprocess import call
import numpy as np

# Third party imports
# None
# Local application imports
from configHp import class_config
from schedule import class_schedule
from text_buffer import class_text_buffer
from utility import fileexists,pr,make_time_text
# Note use of sensor_test possible on next line
from sensor import class_sensors
from tuyaCloud import class_tuyaCloud
#Set up Config file and read it in if present

config = class_config()
schedule = class_scehule(config)

sensor = class_sensors()

numberSwitches = 2
cloud = class_tuyaCloud(numberSwitches)

logTime= datetime.now()
logType = "log"
headings = ["Hour in Day","Room Temp","Per 10 Mins","Predicted Temp","Heaters Target Temp","HP Target Temp", \
			"HP Out","Outside","Heaters Status","HP Status","TotalHeaters","TotalHP","Reason","Message"]
logBuffer = class_text_buffer(headings,config,logType,logTime)


# Set The Initial Conditions
the_end_time = datetime.now()
loop_time = 0
correction = 7.5
# Ensure start right by inc buffer
buffer_increment_flag = False
if config.scan_delay > 9:
	refresh_time = config.scan_delay
else:
	refresh_time = 2*config.scan_delay

print("at Start up Turn heaters Off")


switchNumber = 0
id = config.switchId
code = "switch_1"
stateWanted = False
heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
if successfullResult:
	print("Heater Switch Working")
else:
	print("Heater Operation Fail")
if offLine:
	print("Switch is offLine")
	#id = "bf5723e4b65de4a64fteqz"
	#heatersOn, successfullResult = cloud.operateSwitch(id,"switch_1",False)
	#if successfullResult:
	#	print("Heater Switch Working")
	#else:
	#	print("Heater Operation Fail")
	sys_exit()

startHold = True
lastHoldMin = logTime.minute 
lastHoldSec = 0

programTemp = 0
increment = True
changeRate = 0
#lastTemp,tries = sensor.getTemp()
lastTemp = 0
lastDayInWeek = -1
getTheTempError = False
lastLogTime = logTime
predictedTemp = 0
overRun = False
overRunLogCount = 0
tries = 0  # NOT being set at the moment
sensor.errorCount = 0 # NOT being set at the moment

totalHeaterOnTime = 0
totalHpOnTime = 0

#tempMeasureErrorCount = 0
#maxTries = 0
#triesCount = 0
#getTheTempErrorCount = 0

message = ""
reason = ""


while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
	try:
		# Sort out Time in Day and Day in week etc
		logTime= datetime.now()
		dayInWeek = logTime.weekday()
		hourInDay = logTime.hour + (logTime.minute/60)
		shedStatus,desiredTemp,targetHp,targetHeaters = self.calcTargets(hourInDay)
		if dayInWeek != lastDayInWeek:
			totalHeaterOnTime = 0
			totalHpOnTime = 0

		if heatersOn:
			targetHeaters += config.hysteresis
		else:
			targetHeaters -= config.hysteresis

		if hpOn:
			targetHp += config.hysteresis
		else:
			targetHp -= config.hysteresis
		
		# Do Control
		temperatures = sensor.getTemp()
		temp = temperatures[config.sensorRoomTemp]
		if config.scan_count < 2:
			lastTemp = temp

		if temp < 0 : # No Sensor Connected
			print("no Sensor connected will turn heaters Off")
			switchNumber = config.switchNumberHeaters
			id = config.switchIdHeaters
			code = config.codeHeaters
			stateWanted = False
			heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
			if not(successfullResult):
				print("Heater Operation Fail while shutting down no sensors")
				message = message + " Htr Op Fail noo sensors"
				increment = True

			switchNumber = config.switchNumberHp
			id = config.switchIdHp
			code = config.codeHp
			stateWanted = False
			hpOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
			if not(successfullResult):
				print("Heat Pump Operation Fail while shutting down no sensors")
				message = message + " Htr Op Fail noo sensors"
				increment = True
			sys_exit()
		else:
			tempChange = (temp - lastTemp)*config.scan_delay/60 # degrees per minute
			changeRate = changeRate + (0.1 * (tempChange - changeRate))
			if abs(changeRate) * 3 > 2:
				changeRate = changeRate * 0.95
				message = message + " RR" + str(round(changeRate,3)) + ", "
				print("changeRate reduced : ",changeRate)
				increment = True
				reason = reason + "ChangeRateReduced"
				
			predictedTemp = temp + (3 * changeRate)
			lastTemp = temp
			
			if predictedTemp >= targetHeaters

				if heatersOn : # This is a change from ON to OFF
					heatersTurnOffTime = logTime
					heatersOnTime = (heatersTurnOffTime - heatersTurnOnTime).total_seconds() / 60.0
					totalHeatersOnTime += onTime
					increment = True
					reason = reason + "switchNumberHpheaters Off,"
					message = message + "htrs off after " + str(round(onTime)

				switchNumber = config.switchNumberHeaters
				id = config.switchIdHeaters
				code = config.codeHeaters
				stateWanted = False
				heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
				if not(successfullResult):
					increment = True
					reason = reason + " Heater turn off Fault, "
					print("Heater Operation Fail")
				if offLine:
					reason = reason + " Heater Switch Offline, "
			else:
				if not heatersOn : # This is a change from OFF to ON
					#print("Temp < Target so turn heaters ON")
					heatersTurnOnTime = logTime
					heatersOffTime = (heatersTurnOnTime - heatersTurnOffTime).total_seconds() / 60.0
					increment = True
					reason = reason + "heatersON"
					message = message + "htrs on after " + str(round(heatersOffTime)
				switchNumber = config.switchNumberHeaters
				id = config.switchIdHeaters
				code = config.codeHeaters
				stateWanted = True
				heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
				if not(successfullResult):
					increment = True
					reason = reason + " Heater turn on Fault, "
					print("Heater Operation Fail")
				if offLine:
					increment = True
					reason = reason + " Heater Switch Offline, "

		# Do Logging
		#" Room Temp","Target Temp","heaters Status","Message"]
		logBuffer.line_values["Hour in Day"]  =  round(hourInDay,2)
		logBuffer.line_values["RoomTemp"]  = round(temperatures[0],2)
		logBuffer.line_values["Per 10 Mins"] = round(changeRate*10*60/config.scan_delay,2)
		logBuffer.line_values["Predicted Temp"] = round(predictedTemp,2)
		logBuffer.line_values["Heaters Target Temp"]  = ########
		logBuffer.line_values["HP Target Temp"]  = ########
		logBuffer.line_values["HP Out"]  = round(temperatures[1],2)
		logBuffer.line_values["Outside"]  = round(temperatures[2],2)
		if heatersOn:
			logBuffer.line_values["Heaters Status"]  = "ON"
		else:
			logBuffer.line_values["heaters Status"]  = "OFF"
		if hpOn:
			logBuffer.line_values["HP Status"]  = "ON"
		else:
			logBuffer.line_values["HP Status"]  = "OFF"
		logBuffer.line_values["TotalHeaters"]  = round(offTime,2)
		logBuffer.line_values["TotalHP"]  = round(onTime,2)

#headings = ["Hour in Day"," Room Temp","Per 10 Mins","Predicted Temp","Heaters Target Temp","HP Target Temp", \
# "HP Out","Outside","Heaters Status","HP Status","TotalHeaters","TotalHP","Reason","Message"]

		#Ensure logs at least every config.mustLog minutes 
		timeSinceLog = (logTime - lastLogTime).total_seconds() / 60.0

		if timeSinceLog > config.mustLog - (config.scan_delay/120):
			lastLogTime = logTime
			
			increment = True
			reason = reason + " MustLog, "
			
		if (config.scan_count < 5): 
			increment = True
			reason = reason + "start,"

		logBuffer.line_values["Reason"]  = reason
		logBuffer.line_values["Message"]  = message

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
				time_sleep(sleep_time)
			except KeyboardInterrupt:
				print(".........Ctrl+C pressed... Output Off 288")
				print("Switching off heaters")
				switchNumber = 0
				id = config.switchId
				code = "switch_1"
				stateWanted = False
				heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
				if successfullResult:
					print("Heater Operation OK 292")
				if not(heatersOn):
					print("Heaters Off OK")
				else:
					print("Check Heaters")
				time_sleep(10)
				sys_exit()
			except ValueError:
				print("sleep_Time Error value is: ",sleep_time, "loop_time: ",
				      loop_time,"correction/1000 : ",correction/1000)
				print("Will do sleep using config.scan_delay and reset correction to 7.5msec")
				correction = 7.5
				time_sleep(config.scan_delay)
			except Exception:
				print("some other error with time_sleep try with config.scan_delay")
				time_sleep(config.scan_delay) 
		else:
			time_sleep(config.scan_delay)
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
		switchNumber = 0
		id = config.switchId
		code = "switch_1"
		stateWanted = False
		heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
		if successfullResult:
			print("Heater Operation OK 324")
		if not(heatersOn):
			print("Heaters Off OK")
		else:
			print("Check Heaters")
		time_sleep(10)
		sys_exit()

	
