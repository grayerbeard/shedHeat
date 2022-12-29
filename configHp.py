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

# title           :confighP.py
# description     :pwm control for Sauna Electric Heater Control
# author          :David Torrens
# start date      :2019 12 12
# version         :0.1
# python_version  :3

# Standard library imports
from configparser import RawConfigParser
from csv import DictReader as csv_DictReader
from csv import DictWriter as csv_DictWriter
from shutil import copyfile
from sys import exit as sys_exit
from os import path
from sys import argv as sys_argv
from sys import exit as sys_exit
from utility import fileExists,pr,prd,makeTimeText,makeBoolean

# Third party imports
#from w1thermsensor import W1ThermSensor

# Local application imports
#from utility import pr,makeTimeText,send_by_ftp

class class_config:
	def __init__(self,config_filename):
		self.prog_path = path.dirname(path.realpath(__file__)) + "/"
		self.prog_name = str(sys_argv[0][:-3])
		self.__default_config_filename = "configHp_default.cfg"
		self.logType = "log" # default log type
		defaultConfig = "default_" + config_filename
		
		if fileExists(config_filename):		
			print( "Will use : " ,config_filename)
			try:
				copyfile("old" + defaultConfig,"older" + defaultConfig)
				print("copied ","old" + defaultConfig," to ","older" + defaultConfig )
			except:
				print("noFilecalled: ","old" + defaultConfig," to copy")
			try:
				copyfile(defaultConfig,"old" + defaultConfig)
				print("copied ",defaultConfig," to ","old" + defaultConfig )
			except:
				print("noFilecalled: ",defaultConfig," to copy")
			try:
				copyfile(config_filename,defaultConfig)
				print("copied ", config_filename," to ",defaultConfig)
			except:
				print("noFilecalled: ",config_filename," to copy")
		elif fileExists(defaultConfig): 
			print("Will copy ",defaultConfig," to ",config_filename, " and use that")
			copyfile(defaultConfig,config_filename)
		else:
			print(debug,"No Config File or defaultt filke must exit")
			sys_exit()

		config_read = RawConfigParser()
		config_read.read(config_filename)

		section = "Scan"
		self.scan_delay = float(config_read.get(section, 'scan_delay')) 
		self.max_scans = float(config_read.get(section, 'max_scans'))
		self.mustLog = float(config_read.get(section, 'mustLog'))

		section = "Log"
		self.log_directory = config_read.get(section, 'log_directory')
		self.local_dir_www = config_read.get(section, 'local_dir_www')
		self.log_buffer_flag = config_read.getboolean(section, 'log_buffer_flag')
		self.text_buffer_length  = config_read.getint(section, 'text_buffer_length')		

		section = "Schedule"
		shedDays = config_read.get(section, 'shedDays').split(",")
		self.shedDays = []
		for shedDay in shedDays:
			self.shedDays.append(float(shedDay))
		self.shedOpens = config_read.getfloat(section, 'shedOpens')
		self.shedCloses = config_read.getfloat(section, 'shedCloses')
		self.desiredTemperature = config_read.getfloat(section, 'desiredTemperature')
		self.temperatureSlope = config_read.getfloat(section, 'temperatureSlope')
		self.fanHeaterFollowTime = config_read.getfloat(section, 'fanHeaterFollowTime')
		self.fanHeaterFollowTemp = config_read.getfloat(section, 'fanHeaterFollowTemp')

		section = "MeasureAndControl"

		self.hysteresis =  config_read.getfloat(section, 'hysteresis')
		self.headings = config_read.get(section, 'headings').split(",")
		self.sensorRoomTemp =  config_read.getint(section, 'sensorRoomTemp')
		self.sensorOther = config_read.getint(section, 'sensorOther')
		self.sensorOutside = config_read.getint(section, 'sensorOutside')
		self.names = config_read.get(section, 'names').split(",")
		self.ids   = config_read.get(section, 'ids').split(",")
		self.codes0 = config_read.get(section, 'codes0').split(",")
		self.values0 = config_read.get(section, 'values0').split(",")
		self.values0Types = config_read.get(section, 'values0Types').split(",")
		self.codes1 = config_read.get(section, 'codes1').split(",")
		self.values1 = config_read.get(section, 'values1').split(",")
		self.values1Types = config_read.get(section, 'values1Types').split(",")
		self.deviceNumberHeaters = config_read.getint(section, 'deviceNumberHeaters')
		self.deviceNumberHp = config_read.getint(section, 'deviceNumberHp')
		self.deviceNumberTemp1 = config_read.getint(section, 'deviceNumberTemp1')
		self.deviceNumberTemp2 = config_read.getint(section, 'deviceNumberTemp2')
		self.deviceNumberTemp3 = config_read.getint(section, 'deviceNumberTemp3')
		self.deviceNumberTemp4 = config_read.getint(section, 'deviceNumberTemp4')
		self.numberCommandSets = config_read.getint(section, 'numberCommandSets')
		self.doTest = config_read.getboolean(section, 'doTest')
		self.debug = config_read.getboolean(section, 'debug')
#		New method
		#self.tuyaTempSensorDeviceNumbers = config_read.getint(section, 'tuyaTempSensorDeviceNumbers')
		#self.tuyaTempSensorNames = config_read.get(section, 'tuyaTempSensorNames').split(",")
		#self.gotCodes = config_read.get(section,'codes').split("#")
		#prd(debug,"self.gotCodes  ",self.gotCodes)
		#sys_exit()
		#self.codes = [{}]*self.numberDevices
		#self.codes  = []
		#for ind in self.gotCodes:
		#	self.codes.append(setCodes)
		#self.gotValues = config_read.get(section, 'values').split("#")
		#self.values  = []
		#for setValues in self.gotValues:
		#	self.values.append(setValues)
		#self.gotValuesTypes = config_read.get(section, 'valuesTypes').split("#")
		#self.valuesTypes  = []
		#for setValuesTypes in self.gotValuesTypes:
		#	self.valuesTypes.append(setValuesTypes)

		prd(self.debug,"Program Name is : ",self.prog_name)
		prd(self.debug,"config file is : ",config_filename)
		prd(self.debug,"Default config file is : ",defaultConfig)
		return

