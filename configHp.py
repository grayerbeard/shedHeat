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


#from datetime import datetime
from shutil import copyfile
#from ftplib import FTP
#from sys import argv as sys_argv
from sys import exit as sys_exit
#import socket
from os import path
from sys import argv as sys_argv
from sys import exit as sys_exit

from utility import fileexists,pr,make_time_text

# Third party imports
#from w1thermsensor import W1ThermSensor

# Local application imports
#from utility import pr,make_time_text,send_by_ftp

class class_config:
	def __init__(self):
		self.prog_path = path.dirname(path.realpath(__file__)) + "/"
		self.prog_name = str(sys_argv[0][:-3])
		self.__config_filename = "configHp.cfg"
		self.__default_config_filename = "configHp_default.cfg"
		self.logType = "log" # default log type
		print("Program Name is : ",self.prog_name)
		print("config file is : ",self.__config_filename)
		print("Default config file is : ",self.__default_config_filename)
		
		if fileexists(self.__config_filename):		
			print( "Will use : " ,self.__config_filename)
		elif fileexists(self.__default_config_filename): 
			print( "Will copy ",self.__default_config_filename," to ",self.__config_filename, " and use that")
			copyfile(self.__html_filename, self.__www_filename)
		else:
			print("No Config File or defaultt filke must exit")
			sys_exit()

		config_read = RawConfigParser()
		config_read.read(self.__config_filename)

		section = "Scan"
		self.scan_delay = float(config_read.get(section, 'scan_delay')) 
		self.max_scans = float(config_read.get(section, 'max_scans'))
		self.mustLog = float(config_read.get(section, 'mustLog'))

		section = "Log"
		self.log_directory = config_read.get(section, 'log_directory')
		self.local_dir_www = config_read.get(section, 'local_dir_www')
		self.log_buffer_flag = config_read.getboolean(section, 'log_buffer_flag')
		self.text_buffer_length  = int(config_read.get(section, 'text_buffer_length'))		

		section = "Schedule"
		self.shedOpens = float(config_read.get(section, 'shedOpens'))
		self.shedCloses = float(config_read.get(section, 'shedCloses'))
		self.desiredTemperature = float(config_read.get(section, 'desiredTemperature'))
		self.temperatureSlope = float(config_read.get(section, 'temperatureSlope'))
		self.fanHeaterFollowTime = float(config_read.get(section, 'fanHeaterFollowTime'))
		self.fanHeaterFollowTemp = float(config_read.get(section, 'fanHeaterFollowTemp'))

		section = "MeasureAndControl"

		self.hysteresis =  float(config_read.get(section, 'hysteresis'))
		self.sensorTargetTemp =  int(config_read.get(section, 'sensorTargetTemp'))
		self.sensorHpOut = int(config_read.get(section, 'sensorHpOut'))
		self.sensorOutside = int(config_read.get(section, 'sensorOutside'))
		self.switchNumberHeaters = int(config_read.get(section, 'switchNumberHeaters'))
		self.switchIdHeaters = config_read.get(section, 'switchIdHeaters')
		self.codeHeaters = config_read.get(section, 'codeHeaters')
		self.switchNumberHp = int(config_read.get(section, 'switchNumberHp'))
		self.switchIdHeaters = config_read.get(section, 'switchIdHeaters')
		self.codeHp = config_read.get(section, 'codeHp')
		return
