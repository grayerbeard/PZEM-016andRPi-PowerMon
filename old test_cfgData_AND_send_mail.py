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
	# Format of cfgData Dictionary
#    key        :  variable used for 
# emailFrom	: a single email; address
# token 		: the encrypted password
# mailSMTP		: the address of the server for sending email
# mailPort		: port number for sending email e.g. 465
# subject		: Text to put in the email subject
# emailTo		: a list of email addresses to send emails to (can be just one)

	cfgDataFileName = "cfgData.json"
	cfgDataKeys = ["emailFrom","token","mailSMTP","mailPort","subject","emailTo"]
	#Types Are;
	#1 email
	#2 password
	#3 server
	#4 positive integer
	#5 text
	#6 list emails
	cfgDataType = [1,2,3,4,5,6]
	cfgDataPrompt = ["Enter email addres for sending Emails",
					"Enter Password for email sending",
					"Enter Email Send Server"
					"Enter Email server Port Number"
					"Enter Email Subject"
					"Enter email addresses to send to",
	cfgDataDefaults = {"emailFrom" : "from@sender.com",
						"token": "@@@@@@@@@",
						"mailSMTP" : "mail.server.com",
						"mailPort": "465",
						"subject": "Mail from Python",
						"emailTo": ["first@nice.com"] }
	# Test the cfgData module
	FileReadResult , cfgData = get_cfgData(cfgDataFileName,cfgDataKeys)
	
	if FileReadResult == 2 :
		print(cfgData)
		File_Read = True
		print("File read and all items present")
	elif FileReadResult == 1 :
		print("File read but not all items present")
		File_Read = True
	else:
		File_Read =  False
		print("no file present so lets make", File_Read)
		keybrd_interupt,cfgData,File_Edit_result = edit_cfgData(cfgDataFileName,File_Read,cfgData)
		File_Read = File_Full
	try:
		# This Keyboard Interupt Flag signals an interupt while editing 
		keybrd_interupt = False
		while not keybrd_interupt:
			# Repeatedly test editing cfgData,  Press Ctrl C to exit
			print()
			print("Repeatedly testing editing cfgData,  Press Ctrl C to exit")
			keybrd_interupt,cfgData,File_Full = edit_cfgData(cfgDataFileName,File_Read,cfgData)
			if File_Full:
				break
		print()
		print("Dropped back to Main Prog due to interupt whil editing")
		print()
	except KeyboardInterrupt:
		print()
		print("Interupt in main Program")
		print()
		File_Read , cfgData_filed = get_cfgData(cfgDataFileName)
		if cfgData_filed != cfgData:
			print("Edits may not have beeen saved to file")

		print
		print("Buffer Contents : ",cfgData)

		if File_Read :
			print("cfgData.json file contents : ",cfgData)
		else:
			print("No json file saved")

#############################################################
#				 	Test send email							#
#############################################################


	# TEMP STOP HERE ##################################################################
	return 0

	date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	mailSMTP = 'mail.smalle.uk'
	mailPort =  465
	embedtype = 'png'
	password = 'TU6v65niddy'
	email_from  = 'rpi_send@smalle.uk'
	emails_to = ['djgtorrens@gmail.com',
				'david.torrens@outlook.com',
				'djgtorrens@yahoo.co.uk']
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

	
	subject = f'WMIS Energy Report - {date_str}'
	send_mail(mailSMTP,mailPort,password,email_from,emails_to,subject,htmlintro,filenames,embedtype)
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
