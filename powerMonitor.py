#!/usr/bin/env python3
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

# title           :powerMonitor.py
# description     :plogging of shed power use
# author          :David Torrens
# start date      :2022 03 07
# version         :0.1 March 2022
# python_version  :3

# Standard library imports
from time import sleep as time_sleep
from os import path
from datetime import datetime
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

#Set up Config file and read it in if present
config = class_config()
if fileexists(config.config_filename):		
	print( "will try to read Config File : " ,config.config_filename)
	config.read_file() # overwrites from file
else : # no file so file needs to be writen
	config.write_file()
	print("New Config File Made with default values, you probably need to edit it")
	
config.scan_count = 0

headings = ["Count","Voltage","Amps","Power","Energy","Hz","PF","Alarm","Message"]
log_buffer = class_text_buffer(headings,config)

sensor = class_my_sensors(config)

# Set The Initial Conditions
the_end_time = datetime.now()
last_total = 0
loop_time = 0
correction = 7.5
# Ensure start right by inc buffer
#last_fan_state = True
#buffer_increment_flag = False
refresh_time = 2 * config.scan_delay # How often to refresh the browser display#

chanPorts = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
chanAddrs = [0x01, 0x01]
chan = 0

lastLoggedReadings = readAcPZEM(chanPorts[chan], chanAddrs[chan],headings)
scansSinceLog = 0
scansSinceEmail = 0

#  Shed open times
daysOpen = (3,4)
openTime =  7
closeTime = 17



#                 cfgData File for Email

# Format of cfgData Dictionary of configurationn data
#    key        :  variable used for 
# emailFrom		: a single email; address
# token 		: the encrypted password
# mailSMTP		: the address of the server for sending email
# mailPort		: port number for sending email e.g. 465
# subject		: Text to put in the email subject
# emailTo		: a list of email addresses to send emails to (can be just one)

# Define file name
cfgDataFileName = "cfgData.json"

#  Define a list of the keys required in the dictionary
cfgDataRequiredKeys = ["emailFrom","token","mailSMTP","mailPort","subject","emailsTo"]

#Types Are;
#0 email
#1 password
#2 server
#3 positive integer
#4 text
#5 list emails

# The test types to apply when the data is read i
cfgDataType = ["email","pwd","server","port","subj","emails"]

# Prompts to the user when he enters values to put in the dictionary
cfgDataPrompt = ["Enter email address for sending Emails",
				"Enter Password for email sending",
				"Enter Email Send Server",
				"Enter Email server Port Number",
				"Enter Email Subject",
				"Enter email addresses to send to"]
				
# default values to use
cfgDataDefaults = {"emailFrom" : "from@sender.com",
					"token": "@@@@@@@@@",
					"mailSMTP" : "mail.server.com",
					"mailPort": "465",
					"subject": "Mail from Python",
					"emailsTo": ["first@nice.com"] }
# parameters for sending email
embedtype = 'png' # This type gets enmbedde in the message
filenames = ['/home/pi/power-monitor/powerMonitor_log.html',
			 '/home/pi/power-monitor/test.png']
print(filenames)
date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
htmlintro = f'''
	<html>
		<body>
			<h1>WMIS Energy Report {date_str}</h1>
			<p>Hello, welcome to your report!</p>
			'''
			
minPowerToLog = 60
minEnergyChangeToLog = 5
LimitScansSinceLog  =  10
LimitScansSinceEmail = 20
LimitScansMustLog = 58  #  USUALLY 58     5 minutes diided by 5 -2
sleep_time = config.scan_delay
 
FileReadResult , cfgData = get_cfgData(cfgDataFileName,cfgDataRequiredKeys,cfgDataDefaults)
	#  Act on the resuly of trying to read in the file.

if FileReadResult == 2 :
	print(cfgData)
	File_Read = True
	print("cfgData File read and all items present")
else:
	File_Read = False
	keybrd_interupt,cfgData,File_Edit_result = \
		edit_cfgData(cfgDataFileName,File_Read,cfgData,cfgDataType,cfgDataPrompt)

while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
	try:
		print("config.scan_count : ", config.scan_count, "  scansSinceLog : ",
		  scansSinceLog, "  scansSinceEmail : ",scansSinceEmail," slp: ",sleep_time)
		# Loop Management and Watchdog
		lst = datetime.now()
		if not((lst.weekday() in daysOpen) and (openTime <= lst.hour < closeTime)):
			message = "shed closed"
			shedClosed = True
		else:
			message = "shed open"
			shedClosed = False
		temp = sensor.get_temp()
		pzem_reading = readAcPZEM(chanPorts[chan], chanAddrs[chan],headings)
		# Logging
		
		pzem_reading[headings[0]] = str(round(config.scan_count,3))
		pzem_reading[headings[len(headings)-1]]= message
		
		powerBeingUsed = False
		
		if ((float(pzem_reading[headings[3]]) > minPowerToLog )  and \
			(float(pzem_reading[headings[4]]) - float(lastLoggedReadings[headings[4]])) \
			> minEnergyChangeToLog) :
			powerBeingUsed = True
		if ((scansSinceLog > LimitScansSinceLog) and powerBeingUsed) or  (config.scan_count < 2) \
				or (scansSinceLog > LimitScansMustLog): 
			log_buffer.line_values = pzem_reading
			log_buffer.pr(True,0,lst,refresh_time)
			last8LoggedReadings = pzem_reading
			if shedClosed and powerBeingUsed and (scansSinceEmail > LimitScansSinceEmail):
				sendMail(cfgData,htmlintro,filenames,log_buffer.logFile,embedtype,log_buffer.email_html)
				scansSinceEmail = 0
			config.scan_count += 1
			scansSinceLog = -1
			
		scansSinceLog += 1
		scansSinceEmail += 1

		# Loop Managemntn^^^
		loop_end_time = datetime.now()
		loop_time = (loop_end_time - lst).total_seconds()
		# Adjust the sleep time to aceive the target loop time and apply
		# with a slow acting correction added in to gradually improve accuracy
		if loop_time < (config.scan_delay - (correction/1000)):
			sleep_time = config.scan_delay - loop_time - (correction/1000)
			try:
				time_sleep(sleep_time)
			except KeyboardInterrupt:
				print("........Ctrl+C pressed... Output Off")
				time_sleep(10)
				sys_exit()
			except ValueError:
				print("sleep_Time Error value is: ",sleep_time, "loop_time: ",
				      loop_time,"correction/1000 : ",correction/1000)
				print("Will do sleep using config.scan_delay and reset correction to 7.5msec")
				cor66rection = 7.5
				time_sleep(config.scan_delay)
			except Exception:
				print("some other error with time_sleep try with config.scan_delay")
				time_sleep(config.scan_delay) 
		else:
			time_sleep(config.scan_delay)
		last_end = the_end_time
		the_end_time = datetime.now()
		last_total = (the_end_time - last_end).total_seconds()
		error = 1000*(last_total - config.scan_delay)
		if error > 250*(config.scan_delay):
			print("Large Error ignored it was : ",error)
		else:
			correction = correction + (0.15*error)
			# Following for looking at error correctoion
			# print("Error correcting OK, Error : ",error,"  Correction : ", correction)
	except KeyboardInterrupt:
		print(".........Ctrl+C pressed... Output Off")
		time_sleep(10) 
		sys_exit()

	
