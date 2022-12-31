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

# title           :myTuya.py
# description     :interfaces for Tuya Devices
# author          :David Torrens
# start date      :2022 09 01
# version         :0.1
# python_version  :3

# Standard library imports
from configparser import RawConfigParser
from csv import DictReader as csv_DictReader
from csv import DictWriter as csv_DictWriter
#from datetime import datetime
#from shutil import copyfile
#from ftplib import FTP
#from sys import argv as sys_argv
from sys import exit as sys_exit
#import socket
from os import path
from sys import argv as sys_argv

# Third party imports
#from w1thermsensor import W1ThermSensor

# Local application imports
from utility import pr,make_time_text,send_by_ftp

class class_myTuya:
	def __init__(self,devicesFilename,tinytuyaFilename):
		
		self.kjhkjhkjh = "Set for Your Location"
		self.jkkjhgjkhg = 30		# delay in seconds between each scan (not incl sensor responce times)


	def getID(self,):
		here = "config.read_file"
		config_read = RawConfigParser()
		config_read.read(self.config_filename)
		section = "Scan"
		self.location =  str(config_read.get(section, 'location'))
		self.scan_delay = float(config_read.get(section, 'scan_delay')) 
		self.max_scans = float(config_read.get(section, 'max_scans'))
		section = "Log"
		self.log_directory = config_read.get(section, 'log_directory')
		self.log_directory_www = config_read.get(section, 'log_directory_www')
		self.local_dir_www = config_read.get(section, 'local_dir_www')
		self.log_buffer_flag = config_read.getboolean(section, 'log_buffer_flag')
		self.text_buffer_length  = int(config_read.get(section, 'text_buffer_length'))		
		section = "powerMonitor"
		self.numLogsPerDay =  float(config_read.get(section, 'numLogsPerDay'))
		self.daysOpen =  config_read.get(section, 'daysOpen').split(",")
		print("daysopen  ",self.daysOpen)
		self.openTime =  float(config_read.get(section, 'openTime'))
		self.closeTime =  float(config_read.get(section, 'closeTime'))
		self.minAveragePowerToLog =  float(config_read.get(section, 'minAveragePowerToLog'))
		self.limitSinceLogMINS =  float(config_read.get(section, 'limitSinceLogMINS'))
		self.limitSinceEmailHOURS =  float(config_read.get(section, 'limitSinceEmailHOURS'))
		self.spare =  int(config_read.get(section, 'spare'))
		return

	def write_file(self):
		here = "config.write_file"
		config_write = RawConfigParser()
		section = "Scan"
		config_write.add_section(section)
		config_write.set(section, 'location',self.location)
		config_write.set(section, 'scan_delay',self.scan_delay)
		config_write.set(section, 'max_scans',self.max_scans)
		section = "Log"
		config_write.add_section(section)
		config_write.set(section, 'log_directory',self.log_directory)
		config_write.set(section, 'log_directory_www',self.log_directory_www)
		config_write.set(section, 'local_dir_www',self.local_dir_www)
		config_write.set(section, 'log_buffer_flag',self.log_buffer_flag)
		config_write.set(section, 'text_buffer_length',self.text_buffer_length)	
		section = "powerMonitor"	
		config_write.add_section(section)	
		config_write.set(section, 'numLogsPerDay',self.numLogsPerDay)
		daysOpenAsString  =",".join(map(str,self.daysOpen))
		config_write.set(section, 'daysOpen',daysOpenAsString)
		config_write.set(section, 'openTime',self.openTime)
		config_write.set(section, 'closeTime',self.closeTime)		
		config_write.set(section, 'minAveragePowerToLog',self.minAveragePowerToLog)
		config_write.set(section, 'limitSinceLogMINS',self.limitSinceLogMINS)
		config_write.set(section, 'limitSinceEmailHOURS',self.limitSinceEmailHOURS)
		config_write.set(section, 'spare',self.spare)
		# Writing our configuration file to 'self.config_filename'
		print("Will write new config file with default values: " , self.config_filename)
		with open(self.config_filename, 'w+') as configfile:
			config_write.write(configfile)
		return 0

