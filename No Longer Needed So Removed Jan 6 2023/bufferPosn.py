#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# title           :textBuffer.py
# description     :Rotating Buffer display and logging
# author          :David Torrens
# start date      :29 11 2019
# version         :25 12 2022
# python_version  :3

# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
from time import sleep as timeSleep
import os
import json

###
#Tasks
# sort out display anomolies
# incorporate esending to influx db
# add better top of page live data display

# Local application imports
from utility import pr,makeTimeText,sendByFtp,fileExists,prd
from bufferLogTest import class_buffer_log
import configTextBufferTest

class class_bufferPosn(object):
	# Rotating Buffer Posn Class
	def __init__(self,config):

		# Set up initial conditions for the buffer before any data has been added
		
		self.bufferMaxSize	= config.textBufferLength
		# where the most recent data will be after current update
		# this is also where the newset data will be
		self.mostRecentPosn = 0
		# where the oldest data will be after current update update
		self.oldestPosn = 0
		# The currect size of the buffer, always less than or equal to buffer length
		self.usedSize = 1

	def incrementPointer(self,pointer):
		# Move any pointer on one step in buffer allowing for nust go back to start if reaches the end
		if pointer < (self.bufferMaxSize - 1):
			pointer += 1
		else:
			pointer = 0
		return pointer

	def update(self,increment,count):
		if increment:
		# Make the changes needed for when current data to be retaine
			if self.usedSize < self.bufferMaxSize:
				# if buffer not full yet keep adding
				self.usedSize += 1
				self.mostRecentPosn += 1
				self.oldestPosn = 0
				print("size less than length and now",self.usedSize)
			else:
				# if buffer full move all pointers on new data will overwrite oldest
				self.mostRecentPosn = self.incrementPointer(self.mostRecentPosn)
				self.oldestPosn = self.incrementPointer(self.oldestPosn)
				print("maxed at ",self.usedSize)
		elif (count < 2) and (self.usedSize < self.bufferMaxSize):
			self.usedSize += 1
			self.mostRecentPosn += 1
			self.oldestPosn = 0



	def dataPosn(self,index):
		if self.usedSize == self.bufferMaxSize:
			# Buffer is full calculate based on position of start and end of current data
			dataPosition = self.mostRecentPosn - index
			if dataPosition < 0:
				# so item wanted is in top section
				dataPosition = self.usedSize + dataPosition
			return dataPosition
		else:
			# self.usedSize must be less than buffer size
			if index >  self.usedSize:
				print("Error in buffer index")
				Print("Size is : ",self.usedSize, " Index is : ",Index)
				sysExit()
			else:
				return self.usedSize - index - 1


# test routine run when script run direct
if __name__ == '__main__':
	from configTextBufferTest import class_config
	config = class_config("configTextBufferTest")
	config.scancount = 0
	bufferPosn =  class_bufferPosn(config)

	textBuffer = ["-"] * config.textBufferLength

	occ = 0
	twice = 0

	while (config.scanCount <= config.maxScans) or (config.maxScans == 0):
		if (config.scanCount < 3): 
			increment = True
			reason = "S"
		if (config.scanCount > 4) and occ < 5:
			occ += 1
		elif (config.scanCount > 4):
			increment = True
			reason = "C"
			occ = 0
		if twice < 6:
			twice += 1
		elif twice < 7:
			increment = True
			reason = "T1"
			twice += 1
		else:
			increment = True
			reason += "T2"
			twice = 0

		dataItem = str(config.scanCount) + reason

		print(config.scancount,increment,reason, "   dataItem ", dataItem)


		textBuffer[bufferPosn.mostRecentPosn] = dataItem


		printOut = ""
		for index in range(0,bufferPosn.usedSize):
			printOut = printOut + " " + str(index) + ":" + textBuffer[bufferPosn.dataPosn(index)]

		print("Buffer: ",textBuffer)
		print("Printout: ",printOut)



		bufferPosn.update(increment,config.scanCount)

		print("post update : ", bufferPosn.usedSize," bufferPosn.mostRecentPosn : ",bufferPosn.mostRecentPosn, ": ", dataItem ,"\n\n")



		config.scanCount += 1

		reason = ""
		increment = False

		timeSleep(config.scanDelay)	
		
		
		
		
		















