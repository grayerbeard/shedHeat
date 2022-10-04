#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of pwm_fanshim.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
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

# title           :sensor.py
# description     :get temperature of the temp sensor
# author          :David Torrens
# start date      :2019 12 12
# version         :0.1
# python_version  :3

# Standard library imports
# None

# Third party imports
from w1thermsensor import W1ThermSensor, Sensor
# Local application imports
from utility import fileexists
from sensorConfig import class_sensorConfig
from time import sleep as time_sleep
from datetime import datetime

class class_sensors:
	def __init__(self):
		# Get Sensor codes from sensorConfig.cfg or set up empty variable and default values
		self.sensorConfig = class_sensorConfig()
		self.lastTemperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)
		self.temperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)
	def get_temp(self):
		sensorID = []
		tempsFromSensors = []
		self.temperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)
		sensors = W1ThermSensor.get_available_sensors()
		for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
			#get data
			sensor.id, sensor.get_temperature()
			sensorGet = W1ThermSensor(Sensor.DS18B20, sensor.id)
			temp = sensorGet.get_temperature()
			tempsFromSensors.append(temp)
			sensorID.append(sensor.id)

		#scan the ids expected against those found
		for code in self.sensorConfig.cfgIds:
			foundIndex = sensorID.index(code) # position of cfg file code in list of found codes
			if code in sensorID:
				#we found a code in cfg amongst read in values
				#find this codes position in our cfg list
				cfgIndex = self.sensorConfig.cfgIds.index(code)
				temp = tempsFromSensors[foundIndex]	# the temperature of that sensor
				self.temperatures[foundIndex] = temp # store in output list
				self.lastTemperatures[foundIndex] = temp # store in last values list
			else:
				#The cfg held code was NOT found in connected codes
				cfgIndex = self.sensorConfig.cfgIds.index(code)
				print(cfgIndex,code, "  not found this time")
				if self.lastTemperatures[cfgIndex] == self.sensorConfig.failsDefault:
					print(cfgIndex,code, "  never found")
					self.temperatures[cfgIndex] = self.lastTemperatures[cfgIndex]
				else:
					# it was found during this session, 
					self.temperatures[cfgIndex],self.lastTemperatures[cfgIndex] = \
						round(self.lastTemperatures[cfgIndex]) + 0.12345
		for code in sensorID:
			foundIndex = sensorID.index(code)
			if code in self.sensorConfig.cfgIds:
				cfgIdsIndex = self.sensorConfig.cfgIds.index(code)
				print("This existing code : ",cfgIdsIndex,code,"  was found")
				# no additional action needed we have already stoored the temperature in "temperatures" list.
			else:
				#this is a new code and must be added to the list
				cfgIndex = len(self.sensorConfig.cfgIds) + 1 # one more than was there before
				self.sensorConfig.newConfigFileNeeded = True
				self.sensorConfig.cfgIds.append(code)
				self.temperatures.append(tempsFromSensors[foundIndex])
				self.lastTemperatures.append(tempsFromSensors[foundIndex])
		if self.sensorConfig.newConfigFileNeeded:
			self.sensorConfig.write_file()
		return self.temperatures

if __name__ == '__main__':

	#from config import class_config

	#Set up Config file and read it in if present
	#config = class_config()
	#if fileexists(config.config_filename):		
	#	print( "will try to read Config File : " ,config.config_filename)
	#	config.read_file() # overwrites from file
	#else : # no file so file needs to be writen
	#	config.write_file()
	#	print("New Config File Made with default values, you probably need to edit it")
	sensor = class_sensors()
	print("Sensor Class set up")
	print("\n")
	lastTime = datetime.now()
	limit = 0
	count = 0
	while (count<limit) or (limit == 0):
		temperatures = sensor.get_temp()
		thisTime = datetime.now()
		cycleTime = round((thisTime - lastTime).total_seconds(),2)
		lastTime = thisTime
		for index in range(len(sensor.sensorConfig.cfgIds)):
			print(count,cycleTime,index+1,sensor.sensorConfig.cfgIds[index],temperatures[index])
		print ("\n")
		count+=1

