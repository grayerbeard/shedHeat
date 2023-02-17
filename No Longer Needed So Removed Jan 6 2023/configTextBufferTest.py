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
#from utility import pr,make_time_text,send_by_ftp

class class_config:
	def __init__(self,configFileName):
		self.progPath = path.dirname(path.realpath(__file__)) + "/"
		self.progName = str(sys_argv[0][:-3])
		self.defaultConfigFileName = configFileName + "Default.cfg"
		self.configFileName = configFileName + ".cfg"
		self.logType = "log" # default log type
		
		if fileExists(self.configFileName):	
			print( "Will use : " ,self.configFileName)
			try:
				copyfile("old" + self.defaultConfigFileName,"older" + self.defaultConfigFileName)
				print("copied ","old" + self.defaultConfigFileName," to ","older" + self.defaultConfigFileName )
			except:
				print("noFilecalled: ","old" + self.defaultConfigFileName," to copy")
			try:
				copyfile(self.defaultConfigFileName,"old" + self.defaultConfigFileName)
				print("copied ",self.defaultConfigFileName," to ","old" + self.defaultConfigFileName )
			except:
				print("noFilecalled: ",self.defaultConfigFileName," to copy")
			try:
				copyfile(config_filename,self.defaultConfigFileName)
				print("copied ", config_filename," to ",self.defaultConfigFileName)
			except:
				print("noFilecalled: ",self.configFileName," to copy")
		elif fileexists(self.defaultConfigFileName): 
			print("Will copy ",self.defaultConfigFileName," to ",self.configFileName, " and use that")
			copyfile(self.defaultConfigFileName,self.configFileName)
		else:
			print("No Config File or defaultt filke must exit")
			sys_exit()

		configRead = RawConfigParser()
		configRead.read(self.configFileName)

		section = "Scan"
		self.scanDelay = float(configRead.get(section, 'scanDelay')) 
		self.maxScans = float(configRead.get(section, 'maxScans'))
		self.mustLog = float(configRead.get(section, 'mustLog'))
		self.scanCount = 0

		section = "Log"
		self.logDirectory = configRead.get(section, 'logDirectory')
		self.localDirWww = configRead.get(section, 'localDirWww')
		self.logBufferFlag = configRead.getboolean(section, 'logBufferFlag')
		self.textBufferLength  = configRead.getint(section, 'textBufferLength')
		self.headings = configRead.get(section, 'headings').split(",")
		print("self.headings :",self.headings)
		self.doTest = configRead.getboolean(section, 'doTest')
		self.debug = configRead.getboolean(section, 'debug')

		prd(self.debug,"Program Name is : ",self.progName)
		prd(self.debug,"config file is : ",self.configFileName)
		prd(self.debug,"Default config file is : ",self.defaultConfigFileName)
		return

