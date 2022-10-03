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


class class_my_sensors:
	def __init__(self,idsToUse):
		sensorConfig = class_sensorConfig()
		#Set up Config file and read it in if present
		sensorConfig = class_sensorConfig(logTime)
	if fileexists(config.config_filename):		
		print( "will try to read Config File : " ,config.config_filename)
		config.read_file() # overwrites from file
	else : # no file so file needs to be writen
		config.write_file()
		print("New Config File Made with default values, you probably need to edit it")
		self.sensorConfig = 
		self.failDefault = -100
		self.lastReading = [self.failDefault]*len(idsToUse)
		self.idsToUse = idsToUse
	def get_temp(self):
		tempsFromSensors = []
		sensorID = []
		fails = []
		newCode = []
		readings = [-1]*len(self.idsToUse)
		# gets the temperature of the sensor for readings	
		sensors = W1ThermSensor.get_available_sensors()
		#print("Found Sensors : ",setemps.append(temp)nsors)
		for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
			#get data
			try:
				sensor.id, sensor.get_temperature()
				sensorGet = W1ThermSensor(Sensor.DS18B20, sensor.id)
				temp = sensorGet.get_temperature()
				tempsFromSensors.append(temp)
				sensorID.append(sensor.id)
			except:
				fails.append(sensor.id)
			found = len(sensorID)
			#print(found)
			#print(sensorID[found-1])
			if found > 0:
				print("sensor : ",found,"   SensorID : ",sensorID[found-1]," Temp : ",tempsFromSensors[found-1])
		for code in self.idsToUse:
			if code in sensorID:
				index = sensorID.index(code)
				temp = tempsFromSensors[index]	
				print("found : ",code, " at ", index," with value : ",temp)
				readings[index] = temp
				self.lastReading[index] = temp
			elif self.lastReading(index) ==  self.failDefault :
				print(code, " never found")
			else:
				print(code, "  not found this time")
				readings[index] = round(self.lastReading[index]) + 0.12345
		for code in sensorID:
			if code in self.idsToUse:
				print("This code : ",code,"  was found")
			else:
				newCode.append(code)
		return fails,found,sensorID, tempsFromSensors

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
	idsToUse=('0316062c0fff', '0316064402ff', '0315a80584ff')
	sensor = class_my_sensors(idsToUse)
	print("Sensor Class set up")
	print("\n")
	
	limit = 0	
	count = 0
	while (count<limit) or (limit == 0):
		fails,found,sensorID, tempsFromSensors = sensor.get_temp()
		for ind in range(found):
			print(ind+1,sensorID[ind],tempsFromSensors[ind])
		print (sensorID)
		print (tempsFromSensors)
		count+=1

