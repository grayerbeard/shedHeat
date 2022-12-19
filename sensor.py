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
from inspect import currentframe as cf
from inspect import getframeinfo as gf

class class_sensors:
	def __init__(self):
		# Get Sensor codes from sensorConfig.cfg or set up empty variable and default values
		self.sensorConfig = class_sensorConfig()
		self.lastTemperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)
		self.temperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)
		# for debug
		#self.testBias = -3
	def getTemp(self):

		#set up an empt list for error reporting
		excRep = []

		#set up an empty list for sensor IDs
		sensorID = []

		#set up and empty list for readings found
		tempsFromSensors = []

		# Put default values incase not able to get a new value 
		self.temperatures = [self.sensorConfig.failDefault]*len(self.sensorConfig.cfgIds)

		# set up to read in sensors
		# this could be in any order
		# this could miss expeccted sensors
		# this could include unexpected new sensors
		# code below allows for all these possibilities
		sensors = W1ThermSensor.get_available_sensors()

		numberFound = 0
		try:
			finfo = gf(cf())
			# scan through sensors available and read into the list "tempsFromSensors"	
			for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
				#get data
				finfo = gf(cf())
				sensor.id, sensor.get_temperature()
				sensorGet = W1ThermSensor(Sensor.DS18B20, sensor.id)
				temp = sensorGet.get_temperature()
				tempsFromSensors.append(temp)
				sensorID.append(sensor.id)

			#scan the ids expected against those found
			finfo = gf(cf())
			for code in self.sensorConfig.cfgIds:
				found = False
				if code != '0315a80584ff':				
					foundIndex = sensorID.index(code) # position of cfg file code in list of found codes
					found = True
				else:
					found = False
				if (code in sensorID) and found:
					#we found a code in cfg amongst read in values
					#find this codes position in our cfg list
					cfgIndex = self.sensorConfig.cfgIds.index(code)
					temp = tempsFromSensors[foundIndex]	# the temperature of that sensor
					temp = tempsFromSensors[foundIndex]	# the temperature of that sensor
					self.temperatures[foundIndex] = temp # store in output list
					self.lastTemperatures[foundIndex] = temp # store in last values list
					numberFound += 1
				else:
					#The code from sensors.cfg was NOT found in connected codes
					cfgIndex = self.sensorConfig.cfgIds.index(code)
					#print(cfgIndex,code, "  not found this time")
					if self.lastTemperatures[cfgIndex] == self.sensorConfig.failDefault:
						#print(cfgIndex,code, "  never found")
						self.temperatures[cfgIndex] = self.lastTemperatures[cfgIndex]
					else:
						print("############## Doing rounding #############")
						# it was found during this session, 
						self.temperatures[cfgIndex] = round(self.lastTemperatures[cfgIndex]) + 0.12345
						self.lastTemperatures[cfgIndex] = round(self.lastTemperatures[cfgIndex]) + 0.1111
						print("Last was : ", self.lastTemperatures[cfgIndex],"  This is : ",self.temperatures[cfgIndex])
		except Exception as err:
			exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err))
			if not(exc in excRep):
				excRep.append(exc)

		try:
			finfo = gf(cf())
			for code in sensorID:
				foundIndex = sensorID.index(code)
				if code in self.sensorConfig.cfgIds:
					cfgIdsIndex = self.sensorConfig.cfgIds.index(code)
					#print("This existing code : ",cfgIdsIndex,code,"  was found")
					# no additional action needed we have already stoored the temperature in "temperatures" list.
				else:
					#this is a new code and must be added to the list
					cfgIndex = len(self.sensorConfig.cfgIds) + 1 # one more than was there before
					self.sensorConfig.newConfigFileNeeded = True
					self.sensorConfig.cfgIds.append(code)
					self.temperatures.append(tempsFromSensors[foundIndex])
					self.lastTemperatures.append(tempsFromSensors[foundIndex])
					numberFound += 1
			if self.sensorConfig.newConfigFileNeeded:
				self.sensorConfig.write_file()
		except Exception as err:
			exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err))
			if not(exc in excRep):
				excRep.append(exc)
		return self.temperatures,excRep,numberFound

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
	lastTime = datetime.now()
	limit = 10000
	count = 0
	pat = 1
	startTime = datetime.now()
	reason = ""
	while (count<limit) or (limit == 0):
		temperatures,excRep,numberFound = sensor.getTemp()
		if len(excRep) > 0:
			reason = str(excRep)
			print("Error: ",excRep,"\n","Temperatures: ",temperatures)
		elif numberFound != 2:
			print("numberFound: ",numberFound, temperatures)
#		thisTime = datetime.now()
#		cycleTime = round((thisTime - lastTime).total_seconds(),2)
#		lastTime = thisTime
#		for index in range(len(sensor.sensorConfig.cfgIds)):
#			print(count,cycleTime,index+1,sensor.sensorConfig.cfgIds[index],temperatures[index])
#		print ("\n")count/pat
		#print("\n",count)
		#print(int(round((count/pat),0)),count/pat)
		count+=1
		if int(round((count/pat),0)) == count/pat:
			print("Done: ",count, " of ", limit," After: ", \
			round(((datetime.now() - startTime).total_seconds())/60,2)," minutes.  ",temperatures)
		if reason != "":
			print("reason: ",reason)
		reason = ""



