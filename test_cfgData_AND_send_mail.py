#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_simple_mail_send.py
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
from send_mail import send_mail
from datetime import datetime
from cfgData import edit_cfgData , get_cfgData, password_decrypt
# test changed again

def main(args):
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
	cfgDataRequiredKeys = ["emailFrom","token","mailSMTP","mailPort","subject","emailTo"]
	### Following Three Lines for Debug Only
	#print("List of the required data Keys")
	#for ind in range(0,len(cfgDataRequiredKeys)):
	#	print(ind, " : ",cfgDataRequiredKeys[ind])
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
						"emailTo": ["first@nice.com"] }

	# Test the cfgData module

	print()
	print(" Here are the default Values")
	for ind in range(0,len(cfgDataRequiredKeys)):
		print(cfgDataRequiredKeys[ind]," : ",cfgDataDefaults[cfgDataRequiredKeys[ind]]," is Type: ",cfgDataType[ind])

	# Call The module to be tested.
	FileReadResult , cfgData = get_cfgData(cfgDataFileName,cfgDataRequiredKeys,cfgDataDefaults)
	
	#  Act on the resuly of trying to read in the file.
	if FileReadResult == 2 :
		print(cfgData)
		File_Read = True
		print("File read and all items present")
	elif FileReadResult == 1 :
		print("File read but not all items correctly present")
		File_Read = True
	else:
		File_Read =  False
		print("no file present so lets make", File_Read)
		keybrd_interupt,cfgData,File_Edit_result = edit_cfgData(cfgDataFileName,File_Read,cfgData,cfgDataType,cfgDataPrompt)
		File_Read = File_Full
	check = input("Press Y to edit again:   ")
	if check == "Y":
		while True:
			keybrd_interupt,cfgData,File_Edit_result = edit_cfgData(
				cfgDataFileName,File_Read,cfgData,cfgDataType,cfgDataPrompt)
			check = input("Press Y to edit again:   ")
			if check != "Y":
				break

#############################################################
#				 	Test send email							#
#############################################################

	filenames = ['/home/pi/energyMaster/energyMaster_logDetails_Light.csv',
				 '/home/pi/python3_test/simple_mail_send.txt',
				 '/home/pi/python3_test/test_simple_mail_send.txt',
				 '/home/pi/energyMaster/test.png']
	htmlintro = f'''
		<html>
			<body>
				<h1>WMIS Energy Report {date_str}</h1>
				<p>Hello, welcome to your report!</p>
				'''
	send_mail(cfgData,htmlintro,filenames,embedtype)
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
