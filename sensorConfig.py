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

# title           :config.py
# description     :pwm control for powerMonitor Electric Heater Control
# author          :David Torrens
# start date      :2019 12 12
# version         :0.1
# python_version  :3

# Standard library imports
from configparser import RawConfigParser

# Third party imports
#from w1thermsensor import W1ThermSensor

# Local application imports
from utility import pr,make_time_text,send_by_ftp

class class_sensorConfig:
	def __init__(self):
		self.sensorConfig_filename = "sensorConfig.cfg"
		self.idsToUse = []
		#Set up Config file and read it in if present
		if fileexists(self.sensorConfig_filename):		
			print( "will try to read sensorConfig File : " ,self.sensorConfig_filename)
			config_read = RawConfigParser()
			config_read.read(self.sensorConfig_filename)
			self.sensorConfigFileExists = True
			section = "Codes"
			self.idsToUse =  config_read.get(section, 'tempSensorCodes').split(",")

	def write_file(self):
		config_write = RawConfigParser()
		section = "Codes"
		idsToUseAsString  =",".join(map(str,self.idsToUse))
		config_write.set(section, 'tempSensorCodes',idsToUseAsString)
		# Writing our configuration file to 'self.config_filename'
		with open(self.sensorConfig_filename, 'w+') as configfile:
			config_write.write(configfile)
		return 0

