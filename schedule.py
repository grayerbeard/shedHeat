#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of shedHeatHp
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

# title           :schedule.py
# description     :work out targets based on hour in day and confog.cfg parameters
# author          :David Torrens
# start date      :2022 10 09
# version         :0.1
# python_version  :3


import numpy as np

class class_schedule:
	def __init__(self,config):
		self.config = config

	def calcTargets(self,hourInDay,dayInWeek):
		shedStatus = "Closed"
		targetHeaters = 0
		targetHp =0
		desiredTemp = 0
		# for debug
		#print(f'hourInDay : {hourInDay}  dayInWeek : {dayInWeek}')
		if dayInWeek in self.config.shedDays:
			if self.config.shedOpens <= hourInDay < self.config.shedCloses:
				shedStatus = " Open "
				desiredTemp = self.config.desiredTemperature
				targetHp = self.config.desiredTemperature
				if hourInDay > (self.config.shedOpens - self.config.fanHeaterFollowTime):
					targetHeaters = round(self.config.desiredTemperature - self.config.fanHeaterFollowTemp,2)
				else:
					targetHeaters = round((self.config.desiredTemperature - self.config.fanHeaterFollowTemp) -  \
								(self.config.temperatureSlope*(self.config.fanHeaterFollowTime + self.config.shedOpens - hourInDay)),2)
			elif hourInDay < self.config.shedOpens:
				shedStatus = "Slope "
				desiredTemp = 0
				targetHeaters = round((self.config.desiredTemperature - self.config.fanHeaterFollowTemp) -  \
								(self.config.temperatureSlope*(self.config.fanHeaterFollowTime + self.config.shedOpens - hourInDay)),2)
				targetHp = round(self.config.desiredTemperature - (self.config.temperatureSlope*(self.config.shedOpens - hourInDay)),2)
		#for debug
		#print(f'shedStatus: {shedStatus} desiredTemp: {desiredTemp} targetHp: {targetHp} targetHeaters: {targetHeaters}')
		return shedStatus,desiredTemp,targetHp,targetHeaters


	def testPrint(self,start,end,step,dayInWeek):
		# set up an array of times to display
		hoursArray = np.arange(start,end,step)
		# print headings
		print("    Day    Time  Open/Closed  Desired   TargetHp  TargetHtrs") 
		for _, hourInDay in enumerate(hoursArray):
			# get targets etc for this time in day
			shedStatus,desiredTemp,targetHp,targetHeaters = self.calcTargets(hourInDay,dayInWeek)
			# print values
			print("    ",dayInWeek,"    ",hourInDay,"    ", shedStatus,"    ",  desiredTemp,"    ",targetHp,"    ",targetHeaters)

# test routine rin when script run direct
if __name__ == '__main__':
	from configHp import class_config
	from schedule import class_schedule
	config = class_config()
	schedule = class_schedule(config)
	print(config.shedDays)
	start = 10
	end = 24
	step = 0.25
	for dayInWeek in range(0,7):
		schedule.testPrint(start,end,step,dayInWeek)
		print("\n \n")
	
