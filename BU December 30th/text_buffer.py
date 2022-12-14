#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# title           :text_buffer.py
# description     :Rotating Buffer display and logging
# author          :David Torrens
# start date      :29 11 2019
# version         :10 12 2022
# python_version  :3

# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
import os
import json

###
#Tasks
# sort out display anomolies
# incorporate esending to influx db
# add better top of page live data display

# Local application imports
from utility import pr,makeTimeText,sendByFtp,fileExists
from buffer_log import class_buffer_log

class class_text_buffer(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
#	def __init__(self,headings,config,logtype,logTime):
	def __init__(self,config,logtype,logTime):
		#initialization
		self.__config = config
		self.__config.logType = logtype
		print(" Buffer Init for : ",self.__config.prog_name," with a size of : ",self.__config.text_buffer_length, " and  width of : ", len(self.__config.headings) + 1, " including time stamp")
		if not os.path.exists('log'):
		    os.makedirs('log')

		self.__source_ref = 0 # a number used to control prevention repeat messages
		#len(self.__config.headings) = len(self.__config.headings) + 1
		###                     
		#self.lineValues = ["1"]*len(headings)
		
		self.lineValues = {}


		for heading in self.__config.headings:
			self.lineValues[heading]  =  heading[:3:]
		print(self.lineValues)
		self.email_html = "<p> No Log yet </p>"
		#self.__dta = [ [ None for di in range(len(self.__config.headings)) ] for dj in range(self.__config.text_buffer_length+1) ]
		self.__dta = [ [ ".." for di in range(len(self.__config.headings)) ] for dj in range(self.__config.text_buffer_length+1) ]
		self.__size = 0
		self.__posn = self.__config.text_buffer_length-1
		self.__headings = ["Time"]
		#for hdg_ind in range(0,self.__width-1):
		#	#print(hdg_ind,headings[hdg_ind])
		#	self.__headings.append(headings[hdg_ind])
		#print(self.__headings)
		#self.__pr_values = ["text"] * self.__width

		self.__html_filename = config.prog_name + "_" + self.__config.logType + ".html"
		self.__html_filename_save_as = config.prog_path + self.__html_filename
		self.__www_filename = config.local_dir_www + "/" + self.__html_filename
		print("self.__html_filename : ",self.__html_filename)
		print("self.__html_filename_save_as : ",self.__html_filename_save_as)
		print("self.__www_filename : ",self.__www_filename)

		try:
			self.__ftp_creds = config.ftp_creds_filename
		except:
			self.__ftp_creds = ""
		self.__send_html_count = 0
		self.logFile = ""
		if self.__config.log_buffer_flag:
			self.__send_log_count = 0
			self.__log = class_buffer_log(self.__config,logTime)
			
		#try:
		#	print("mqtt not installed")
			#self.__mqttc = mqtt.Client("python_pub")
			#self.__mqttc.connect(self.__config.broker_address, self.__config.broker_port) # use the ip of your rpi here
		#except:
			#print("mqtt cant connect")
			
	def size(self):
		return self.__config.text_buffer_length

#	def update_buffer(self,values,appnd,ref):
	def update_buffer(self,appnd,ref):
		#next for debug
		#print("104 self.__send_log_count : ",self.__send_log_count)
		#append a line of info at the current position plus 1 
		# print("Update Buffer appnd and ref are : ",appnd,ref)
		###
		#print("Growing Buffer?  : ",self.__size," >> ",self.__config.text_buffer_length)
		i = 0
		#for value in values:
		#	self.__dta[self.__posn][i] =val
		for heading in self.__config.headings:
			self.__dta[self.__posn][i] = str(self.lineValues[heading])
			#print(i,heading,self.lineValues[heading])
			i += 1
		#sys_exit()


		if appnd + (self.__source_ref != ref):
			#we adding message and incrementing posn
			if self.__size < self.__config.text_buffer_length-1 :
				self.__size += 1
			if self.__posn == self.__config.text_buffer_length-1:
				# last insert was at the end so go back to beginning@@
				self.__posn = 0
			else:
				# first increment insert position by one
				self.__posn += 1
				# then insert a line full of values
			self.__source_ref = ref
		else:
			self.__source_ref = ref		
		if len(self.lineValues) != len(self.__config.headings) :
			print("Width Error for :",self.__config.prog_name, "Values :",len(self.lineValues) , " Headings ", len(self.__config.headings))
			i = 0
			for heading in self.__config.headings:
				print(i,heading,self.lineValues[heading])
				i += 1
			print(self.lineValues)
			sys_exit()
		###
		#for i in range(0,len(values)):
		#	self.__dta[self.__posn][i] = values[i]

		
		# ##############################################################################
		#  Test WAS HERE
		#i = 0
		#for value in values:
		#	self.__dta[self.__posn][i] = value
		#	i += 1

		#print("Buffer updated and log buffer flag is : ",self.__config.log_buffer_flag)
		if self.__config.log_buffer_flag and appnd:
			self.__log.log_to_file(self.lineValues)
			#self.__log.log_to_file(self.__headings,values)
			#print("Data to text logging")
			#print(self.__headings)
			#print(values)
			
			
			
			if fileExists(self.__www_filename):
				try:
					self.__log.copy_log_to_www(False)
				except:
					print("Failed to copy log file to www because this not there: ",self.__www_filename)
			#send log file to website config every ten scans
			
			# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   NEXT    Needs to be time based @@@@@@@@@@@@@@@@@@@@@@@@@
			#next for debug
			#print("160 self.__send_log_count : ",self.__send_log_count)
			if self.__send_log_count > 10 and fileExists(self.__ftp_creds):
				self.__log.send_log_by_ftp(False,self.__config.log_directory,self.__config.ftp_timeout)
				self.__send_log_count = 0
			elif fileExists(self.__ftp_creds):
				self.__send_log_count += 1
			else:
				self.__send_log_count = 0
 
	def get_line_dta(self, key):
		#return stored element from position relative to current insert position in buffer
		line_dta = [" - "]*len(self.__config.headings)
		if (self.__posn-key) > -1:
			# ne to take values from arlogea before current insert position
			for i in range(len(self.__config.headings)):
				line_dta[i] = self.__dta[self.__posn-key][i]
			return(line_dta)
		else:
			# need to take values from after current insert position
			for i in range(len(self.__config.headings)):
				#following two lines used too debug the calc to get the lower part of status file
				#print("That Calc key,self.__size,self.__config.text_buffer_length, self.__posn-key,key sum",
				 #  key,self.__size,self.__config.text_buffer_length, self.__posn-key,(self.__posn-key),self.(self.__config.text_buffer_length + (self.__posn-key))
				line_dta[i] = self.__dta[self.__config.text_buffer_length + (self.__posn-key)][i]
			return(line_dta)	

	def get_dta(self):
		# get all the data inserted so far, or the whole buffer
		all_data = [ [ None for di in range(len(self.__config.headings)) ] for dj in range(self.__config.text_buffer_length+1) ]
		for ind in range(0,self.__size):
			line_dta = self.get_line_dta(ind)
			# Following line for debug data from Buffer
			# print("get_dta >>>",ind,line_dta)
			for i in range(len(line_dta)):    
				all_data[ind][i] = line_dta[i]
		return(all_data)

	def pr(self,appnd,ref,logTime,refresh_interval):
		here = "buffer.pr for " + self.__config.prog_name
		#make_values = [" -- "]*(self.__width+1)
		#prtime = logTime
		#forScreen = makeTimeText(logTime)
		# following alternative will show more resolution for fractions of a second
		# for_screen = log_time.strftime('%d/%m/%Y %H:%M:%S.%f')      
		#self.lineValues["Time"] = forScreen
		file_start = """<head>
<meta http-equiv="refresh" content="""
		file_start = file_start + str(refresh_interval)
		file_start = file_start + """ />
</head>
<caption>Rotating Buffer Display</caption>"""
		tbl_start = """ <p>
<table style="float: left;" border="1">
<tbody>"""
		tbl_start_line = """<tr>"""
		tbl_end_line = """</tr>"""
		tbl_start_col = """<td>"""
		tbl_end_col= """</td>"""
		tbl_end = """</tbody>
</table>"""
		file_end = """
</body>
</html>"""
		#try:
		i = 0
		#for i in range(0,self.__width -1):
		#for key in self.lineValues:
			#print(key, " : ",self.lineValues[key])
		#	make_values[i+1] = self.lineValues[key]
		#	for_screen = for_screen + " " + str(self.lineValues[key])
		#	i += 1
		forScreen = ""
		for heading in self.__config.headings:
			forScreen += " " + str(self.lineValues[heading])
		#except:
		#	print("Error in make values in ...buffer.pr for : ",self.__config.prog_name)
		#	print("i,values,len(self.line_value>s),self.__width",i,self.lineValues,len(self.lineValues),self.__width)
		#	sys_exit()
				
		# print to s}creen and to status log and update html file
		
		#if appnd:
		#	print(" a/" + self.__config.prog_name + "/" + for_screen)
		#else:
		#	print("na/" + self.__config.prog_name + "/" + for_screen)
		print(forScreen)

		self.update_buffer(appnd,ref)
		with open(self.__html_filename,'w') as htmlfile:
			htmlfile.write(file_start)
			if self.__config.log_buffer_flag:
				self.logFile = self.__config.log_directory + self.__log.log_filename
				htmlfile.write('<p>' + self.__html_filename + ' : ' + 
					makeTimeText(logTime)  + '      ' +
					'<a href= "' + self.logFile + 
					'" target="_blank"> View CSV Log File </a></p>\n<p>')
			else:
				htmlfile.write("<p>" + self.__html_filename + " : " + 
					makeTimeText(logTime)  + "</p>\n<p>")
			htmlfile.write(tbl_start + tbl_start_line)
			self.email_html = tbl_start + tbl_start_line
			for heading in self.__config.headings:
				htmlfile.write(tbl_start_col + heading + tbl_end_col)
				self.email_html = self.email_html + tbl_start_col + heading + tbl_end_col
			htmlfile.write(tbl_end_line)
			self.email_html = self.email_html + tbl_end_line
			buffer_dta = self.get_dta()
			for ind in range(self.__size):
				htmlfile.write(tbl_start_line)
				self.email_html = self.email_html + tbl_start_line
				for i in range(len(self.__config.headings)):
					htmlfile.write(tbl_start_col + str(buffer_dta[ind][i]) + tbl_end_col)
					self.email_html = self.email_html + tbl_start_col + str(buffer_dta[ind][i]) + tbl_end_col
				htmlfile.write(tbl_end_line)
				self.email_html = self.email_html + tbl_end_line
			htmlfile.write(tbl_end)
			self.email_html = self.email_html + tbl_end
			htmlfile.write(file_end)
			self.email_html = self.email_html + file_end
		
		try:
			#next for debug
			#print("Will try to copy : ",self.__html_filename," to ",self.__www_filename)
			if appnd != True:	
				copyfile(self.__html_filename, self.__www_filename)
		except:
			print("Not able to copy : ",self.__html_filename, " to ", self.__www_filename)
		
		#message =  self.lineValues[1]
		
		#try:
		#	print("no mqtt")
		#	#self.__mqttc.publish(self.__config.topic,message,retain=True)
		#	#self.__mqttc.loop(2) #timeout = 2s
		#except:
		#	print("Mqtt cant send")
				
		if fileExists(self.__ftp_creds):
			if self.__send_html_count >= 3:
				# To debug FTP change end of following line to " = True"   !!!!!!!!!!!! 
				FTP_dbug_flag = False
				ftp_result = sendByFtp(FTP_dbug_flag,self.__ftp_creds, self.__html_filename_save_as, self.__html_filename,"",self.__config.ftp_timeout)
				for pres_ind in range(0,len(ftp_result)):
					pr(FTP_dbug_flag,here, str(pres_ind) + " : ", ftp_result[pres_ind])
				self.__send_html_count = 0
			else:
				self.__send_html_count += 1
		return


# test routine run when script run direct
if __name__ == '__main__':
	# change this to suite number of switches.
	# one power switch and one heat pump
	# set up the class
	config = class_config()
	config.scan_count = 0
	logTime = datetime.now()
	headings = ["hdg01""hdg02","hdg03","hdg04"]
#	logBuffer = class_tuyaCloud(headings,config,logtype,logTime)

