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

# Third party imports
# None
# Local application imports
from config import class_config
from text_buffer import class_text_buffer
from utility import fileexists,pr,make_time_text
# Note use of sensor_test possible on next line
from sensor import class_sensors
from tuyaCloud import class_tuyaCloud

#Set up Config file and read it in if present
config = class_config()
if fileexists(config.config_filename):		
	print( "will try to read Config File : " ,config.config_filename)
	config.read_file() # overwrites from file
else : # no file so file needs to be writen
	config.write_file()
	print("New Config File Made with default values, you probably need to edit it")
	
print ("0",config.program0)
print ("1",config.program1)
print ("2",config.program2)
print ("3",config.program3)
print ("4",config.program4)
print ("5",config.program5)
print ("6",config.program6)


program = [[0] for i in range(7)]

for item in config.program0:
	program[0].append(float(item))
for item in config.program1:
	program[1].append(float(item))
for item in config.program2:
	program[2].append(float(item))
for item in config.program3:
	program[3].append(float(item))
for item in config.program4:
	program[4].append(float(item))
for item in config.program5:
	program[5].append(float(item))
for item in config.program6:
	program[6].append(float(item))	
print (program)
		
	
config.scan_count = 0
logTime= datetime.now()
heatersTurnOffTime = logTime
heatersTurnOnTime = logTime
overRunStartTime = logTime
onTime = 0
offTime = 0

logType = "log"
headings = ["Hour in Day"," Room Temp","Per 10 Mins","Predicted Temp","Target Temp","Heat Pmp Out","OutDoor","heaters Status",\
	"offTime","onTime","Reason","Message"]
logBuffer = class_text_buffer(headings,config,logType,logTime)

sensor = class_sensors()

numberSwitches = 2
cloud = class_tuyaCloud(numberSwitches)

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
targetTemp = 0
programTemp = 0
increment = True
changeRate = 0
#lastTemp,tries = sensor.getTemp()
lastTemp = 0
getTheTempError = False
lastLogTime = logTime
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


while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
	try:
		while startHold:
		#while False:
			logTime = datetime.now()
			holdMin = logTime.minute
			holdSec = logTime.second
			if holdMin != lastHoldMin:
				startHold = False
				break
			if holdSec > (lastHoldSec + 5):
				print("Waiting for next Minute : ",(60 - holdSec))
				lastHoldSec = holdSec
		# Sort out Time in Day and Day in week etc
		logTime= datetime.now()
		dayInWeek = logTime.weekday()
		hourInDay = logTime.hour + (logTime.minute/60)
#		dayTime = config.day_start <= hourInDay <= config.night_start
		
		numValues = len(program[dayInWeek])
		ind = 0
		while ind<(numValues):
			progHour = program[dayInWeek][ind]
			if (ind + 2) < numValues:
				nextProgHour = program[dayInWeek][ind + 2]
			else:
				nextProgHour = 24
			progTemp = program[dayInWeek][ind + 1]
			if progHour < hourInDay < nextProgHour:
				targetTemp = progTemp
				print("targetTemp is: ",targetTemp,"from : ",progHour," to : ",nextProgHour)
			ind +=2
		message = "day: " + str(dayInWeek) + " hour: " + str(round(hourInDay,2)) + " TargTemp: " + str(targetTemp)

		if heatersOn:
			targetTemp += config.hysteresis
		else:
			targetTemp -= config.hysteresis
		
		# Do Control
		temperatures = sensor.getTemp()
		temp = temperatures[config.sensor4readings]
		if config.scan_count < 2:
			lastTemp = temp

		if temp < 0 : # Nor Sensor Connected
			print("no Sensor connected will turn heaters Off")
			switchNumber = 0
			id = config.switchId
			code = "switch_1"
			stateWanted = False
			heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
			if not(successfullResult):
				print("Heater Operation Fail while shutting down no sensors")
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
			
			if predictedTemp >= targetTemp:

				if heatersOn : # This is a change from ON to OFF
					#print("Temp NOW > Target so turn heaters off")
					heatersTurnOffTime = logTime
					increment = True
					reason = reason + "heaters Off,"
					message = message + " heaters Turned OFF"

				switchNumber = 0
				id = config.switchId
				code = "switch_1"
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
					onTime = (heatersTurnOnTime - heatersTurnOffTime).total_seconds() / 60.0
					increment = True
					reason = reason + "heatersON"
					message = message + "heaters Turned"
				switchNumber = 0
				id = config.switchId
				code = "switch_1"
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
		logBuffer.line_values["RoomTemp"]  = temp
		logBuffer.line_values["Per 10 Mins"] = round(changeRate*10*60/config.scan_delay,2)
		logBuffer.line_values["Predicted Temp"] = round(predictedTemp,2)
		logBuffer.line_values["Target Temp"]  = targetTemp
		logBuffer.line_values["Other Temp1"]  = temperatures[1]
		logBuffer.line_values["Other Temp2"]  = temperatures[2]
		if heatersOn:
			logBuffer.line_values["heaters Status"]  = "ON"
		else:
			logBuffer.line_values["heaters Status"]  = "OFF"
		logBuffer.line_values["offTime"]  = round(offTime,2)
		logBuffer.line_values["onTime"]  = round(onTime,2)

#headings = ["Hour in Day"," Room Temp","Per 10 Mins","Predicted Temp","Target Temp","Other Temp1","OtherTemp2","heaters Status",\
#	"offTime","onTime","Reason","Message"]

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

		print("count : ",config.scan_count," Increment : ",increment)

		logBuffer.pr(increment,0,logTime,refresh_time)
		print("\n")
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

	
