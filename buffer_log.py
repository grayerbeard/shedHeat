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

# title           :buffer_log.py
# description     :pwm control for R Pi Cooling Fan
# author          :David Torrens
# start date      :2019 11 20
# version         :0.1
# python_version  :3

# Standard library imports
#from configparser import RawConfigParser
from csv import DictReader as csv_DictReader
from csv import DictWriter as csv_DictWriter
from datetime import datetime
from shutil import copyfile
from ftplib import FTP
from sys import argv as sys_argv
from sys import exit as sys_exit

import socket

# Third party importstemp_log
# none
 
# Local application imports
from utility import pr,makeTimeText,sendByFtp

class class_buffer_log:
	def __init__(self,config,logTime):
		self.dbug = False
		self.__send_plain_count = 5
		self.__no_heading_yet = True
		self.__config = config
		timestamp = makeTimeText(logTime)
		self.log_filename = timestamp + "_" + self.__config.prog_name + "_" + self.__config.logType + ".csv"
		self.__log_filename_save_as = self.__config.prog_path + self.__config.log_directory + self.log_filename
		self.__local_www_log_filename = self.__config.local_dir_www + "/" + self.__config.log_directory + self.log_filename
		print("self.log_filename : ",self.log_filename)
		print("self.__log_filename_save_as : ",self.__log_filename_save_as)
		print("self.__local_www_log_filename : ",self.__local_www_log_filename)

#	def log_to_file(self,log_headings,log_values):
	def log_to_file(self,log_values):
		here = 	"log_cpu_data_to_file"
		#write the time at the start of the line in logging file
	
		if self.__no_heading_yet:
			self.__no_heading_yet = False
			self.__log_file = open(self.__log_filename_save_as,'w')
			#for hdg_ind in range(0,len(log_headings)):
			#	self.__log_file.write(log_headings[hdg_ind] + ",")
			
			for heading  in self.__config.headings:
				
				self.__log_file.write(heading + ",")
			self.__log_file.write("\n")
		#print("string made by Buffer Log")
		madeString = ""
		#for z in range(0,len(log_values),1):
		#	self.__log_file.write(str(log_values[z]) + ",")
		#	madeString += str(log_values[z]) + ","
		#filedRecord = {}
		for heading in self.__config.headings:
			#filedRecord[heading] = str(log_values[heading]) + ","
			self.__log_file.write(str(log_values[heading]) + ",")
		#print("Logged as :",filedRecord)
		self.__log_file.write("\n")
		self.__log_file.flush()
		
		return
		
	def send_log_by_ftp(self,FTP_dbug_flag,remote_log_dir,ftp_timeout):
		ftp_result = send_by_ftp(FTP_dbug_flag,self.__config.ftp_creds_filename, self.__log_filename_save_as, \
			self.log_filename,remote_log_dir,ftp_timeout)
		for pres_ind in range(0,len(ftp_result)):
			pr(FTP_dbug_flag,here, str(pres_ind) + " : ", ftp_result[pres_ind])
		if self.__send_plain_count < 0 :
			ftp_result = send_by_ftp(FTP_dbug_flag,self.__config.ftp_creds_filename, self.__log_filename_save_as, \
				"log.csv",remote_log_dir,ftp_timeout)
			for pres_ind in range(0,len(ftp_result)):
				pr(FTP_dbug_flag,here, str(pres_ind) + " : ", ftp_result[pres_ind])
			self.__send_plain_count = 10
		else:
			self.__send_plain_count -= 1
			#print("Send plain count : ",self.__send_plain_count)
		return
					
	def copy_log_to_www(self,dbug_flag):
		try:
			# send the same html file to the local web site
			copyfile(self.__log_filename_save_as, self.__local_www_log_filename)
			#next for debug
			#print( "Sent : " + self.__log_filename_save_as + " to : ", self.__local_www_log_filename)
		except:
			print("Fail with copy " + self.__log_filename_save_as + " to : ", self.__local_www_log_filename)


