#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  splitDayTest.py
#  
#  Copyright 2022  <pi@RPi4Shed>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# Standard library imports
from time import sleep as time_sleep
from os import path
import datetime
from sys import exit as sys_exit
from subprocess import call

# Third party imports
# None
# Local application imports
from config import class_config
from text_buffer import class_text_buffer
# Note use of pwm_test possible on next line
###
#from pwm import class_pwm
from utility import fileexists,pr,make_time_text
###
#from algorithm import class_control
# Note use of sensor_test possible on next line
from sensor import class_my_sensors
from pzemdt import readAcPZEM 

from sendMail import sendMail
from cfgData import edit_cfgData , get_cfgData, password_decrypt

def main(args):

	goFlag = True
	myHour = 0
	myMinute = 0
	numLogsPerDay =36
	logTime = datetime.datetime(2022, 3, 1,myHour,myMinute)
	logPeriod = round(60 * 24/numLogsPerDay,0)/60
	lastLogStep = round((logTime.hour + (logTime.minute/60))/logPeriod,0)
	daysOpen = (2,3)
	openTime =  6
	closeTime = 17
	print("perday,period,stepNumber ",numLogsPerDay,logPeriod,round((logTime.hour + \
		(logTime.minute/60))/logPeriod,0),lastLogStep)
	while goFlag:
		logTime = datetime.datetime(2022, 3, 1,myHour,myMinute)
		#logStep = round((logTime.hour + (logTime.minute/60))/logPeriod,0)
		logTimeHourMin = logTime.hour + (logTime.minute/60)
		logStep = int(logTimeHourMin / logPeriod)
		#if logStep!= lastLogStep:
		#	newLogStep = True
		#	print("New LogStep!",lastLogStep, " >> ",logStep)
		#	lastLogStep = logStep
		#else:
		#	newLogStep = False
		#print(logTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],logStep,newLogStep)
		print(logTime.strftime('%H:%M'),logTimeHourMin,logStep)
		myMinute += 20
		if myMinute > 59 :
			myMinute = 0
			myHour += 1
		if myHour > 23:
			goFlag = False
	
	sys_exit()
	
	logTime = datetime.datetime.now()
	numLogsPerDay = 4
	logPeriod = round(60 * 24/numLogsPerDay,0)/60
	lastLogStep = round((logTime.hour + (logTime.minute/60))/logPeriod,0)
	daysOpen = (2,3)
	openTime =  6
	closeTime = 17
	timeLastLog = logTime - datetime.timedelta(seconds = 10)
	timeLastEmail = logTime - datetime.timedelta(seconds = 10)
	
	timeSinceLog = (logTime - timeLastLog).total_seconds
	timeSinceEmail = (logTime - timeLastEmail).total_seconds
	print("perday,period,stepNumber ",numLogsPerDay,logPeriod,round((logTime.hour + \
		(logTime.minute/60))/logPeriod,0),lastLogStep)
	logStep = round((logTime.hour + (logTime.minute/60))/logPeriod,0)
	if logStep!= lastLogStep:
		newLogStep = True
		print("New LogStep!",lastLogStep, " >> ",logStep)
		lastLogStep = logStep
	else:
		newLogStep = False
	if not((logTime.weekday() in daysOpen) and (openTime <= logTime.hour < closeTime)):
		message = "closed"
		shedClosed = True
	else:
		message = "open"
		shedClosed = False
	message = message + " rdg:" + str(readingsCount) + " of: " + \
			str((limitMustLogMINS * 60)/config.scan_delay) + " 6:" + str(logStep) + "-" + str(lastLogStep)
	if newLogStep: 
		print("new step")

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
