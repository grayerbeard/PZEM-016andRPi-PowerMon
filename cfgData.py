     #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cfgData.py
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
#  ##################################################################
#  #																#  
#  #	Module for retrieving, editing and saving cfg.json file		#
#  #																#
#  ##################################################################
import subprocess
import time
import smtplib
from cryptography.fernet import Fernet
import base64
import re

try:
	import json
except ImportError:
	try:
		import simplejson as json
	except ImportError:
		print("Error: import json module failed")
		sys.exit()



encoding = 'utf-8'
# Regular expression for validating email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
	if(re.fullmatch(regex, email)):
		return True
	else:
		return False
		
def compareKeys(requiredkeys,datasetkeys):
	if len(requiredkeys) != len(datasetkeys):
		return False
	for ind in range(0,len(requiredkeys)):
		if requiredkeys[ind] != datasetkeys[ind]:
			return False
	return True

def password_encrypt(phrase):
	#Generate the token for securely storong password from the password
	#uses key based on machineID
	keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
	fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))
	token = fernetKey.encrypt(bytes(phrase,encoding))
	return token.decode(encoding)

def password_decrypt(token):
	#generate the password from the token
	#uses key based on machineID
	keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
	fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))
	phrase = fernetKey.decrypt(bytes(token,encoding))
	return phrase.decode(encoding)
	
def print_cfg_data(cfgData):
	print()
	for key in cfgData:
		print( key, ": = " ,cfgData[key])
	print()

def get_cfgData(cfgDataFileName,cfgDataRequiredKeys,cfgDataDefaults):
	cfgData = dict()
	# Tries to get cfgData from file
	# If fully successful returns FileReadRusult = 3
	# If file read but keys 
	# if not returns False (so new file needed
	# Returns Current File Contents if file exists
	# If no file then returns an empty cfgData variable
	
	try:
		with open(cfgDataFileName, 'r') as cfgDataFile:
			cfgData_file_data = json.load(cfgDataFile)
			print()
			print("Here is the data read from the file") 
			for key in cfgData_file_data: 
				cfgData[key] = cfgData_file_data[key]
				# Debug
				print(key," : ",cfgData[key])
			print()
			#Reference for list of keys see 
			#https://www.delftstack.com/howto/python/python-dictionary-index/
			File_cfgDataKeys = list(cfgData.keys())
			if compareKeys(cfgDataRequiredKeys,File_cfgDataKeys):
				FileReadResult = 2
				print("File read and Keys correct")
				
				
			else:
				print("File Read but not all items there")
				print("Required : ",cfgDataKeys)
				print("From File: ",cfgData.keys())
				FileReadResult = 1
			print("Finished getCfgData, read file")
			print()
			return FileReadResult, cfgData

	except IOError:
		FileReadResult = 0
		print("No file found returned defaults")
		print("Finished getCfgData, No File")
		print()
		return  FileReadResult,cfgDataDefaults

def edit_cfgData(cfgDataFileName,File_Read,cfgData):	
	try:
#                            Get emailFrom
		while True:
			if File_Read:
				print("existing Value for Senders Email :",cfgData['emailFrom'])
				print("Enter new or Press enter to leave unchanged")
			else:
				cfgData['emailFrom'] = ""
				print("Enter email SENDER's email address")   
	
			cfgData['emailFrom'] = input() or cfgData['emailFrom']
			if check(cfgData['emailFrom']):
				break
			else:
				print("Not a valid email try again")
			
		print("Send Email Address set to: ",cfgData['emailFrom'])
	
#                            Get Password and encrpt token
		while True:
			if File_Read:
				print("There is an existing email send password set")
				print("Enter new or press enter to leave as is")
			else:
				print("No existing pwd")
				cfgData['token'] = ""
				print("Enter email send PASSWORD")
			cfgData['token'] = password_encrypt(input() or password_decrypt(cfgData['token']))
			if len(cfgData['token']) > 4:
				break
			else:
				print("Password required surely must be more than 4 characters")
		print()
		print("Password now :  ",password_decrypt(cfgData['token']))

#                            Get email_to
		if File_Read:
			emailto = cfgData["emailTo"]
			print()
			print("Email to send to set to: ",cfgData["emailTo"])
			print()
		else:
			emailto = []
			# Zero count so that we start scanning through at first email
		email_to_count = 0
		while True :
			#  Check if we are still editing entered emails or entering new ones
			if email_to_count < len(emailto) and File_Read:
				print("Number : ",email_to_count + 1, " Email address :",emailto[email_to_count])
				print("Either enter replacement Or d to delete or enter to leave as is")
	
				input_value = input() or emailto[email_to_count]
	 
				if input_value == "d":
					del emailto[email_to_count]
					print("Deleting old value")
				elif input_value == "f":
					print("Finished editing Send to Emails")
					break
				else:
					if check(input_value):
						emailto[email_to_count] = input_value
						email_to_count += 1
					else:
						print()
						print("Not a valid email try again")
						print()
			else:	
				print()
				print("Enter a new recipient's email for send email number: ",email_to_count +1)
				print("when filished just enter f")
				print("Enter a new value")
				input_value = input()
				if (input_value == "f") and email_to_count > 0:
					print("Finished editing send emails")
					break
				elif input_value == "f":
					print()
					print("Must enter at least one send email")
					print()
				else:
					if check(input_value):
						emailto.append(input_value)
						print("Debug print emailto : ",len(emailto), emailto)
						email_to_count += 1
					else:
						print("Not a valid email try again")
		cfgData['emailTo'] = emailto

				
#							Get mailSMTP

#							Get mailPort
		while True:
			try:
				if File_Read:
					print("There is an existing port number set at :", cfgData['mailPort'])
					print("Enter new or press enter to leave as is")
				else:
					print("No existing port set so enter new Port Number")
					cfgData['mailPort'] = "0"
				mailPort = int(input("Enter Port Number")) or int(cfgData['mailPort'])
				if 1 < mailPort < 9999:
					cfgData['mailPort'] = str(mailPort)
					break
				else:
					print("Enter correct port number between 1 and 9999")
			except ValueError:
					print("Enter a number")
					print()
		print()
		print("email send SMTP Port now set to ",cfgData['mailPort'])

#							Get subject
		while True:
			try:
				if File_Read:
					print("There is an existing subject :", cfgData['subject'])
					print("Enter new or press enter to leave as is")
				else:
					print("No subject set so entersubject")
					cfgData['mailPort'] = "0"
				subject = input("Enter subject") or cfgData['subject']
				if len(subject) > 4:
					break
				else:
					print("Enter some subject text")
			except ValueError:
					print("Enter text")
		print()
		print("Subject now set to ",cfgData['subject'])

#               All done editing

#               Put data into filjson file
		with open(cfgDataFileName, 'w') as cfgDataFile:
			json.dump(cfgData, cfgDataFile)
		keybrd_interupt = False
		File_Full = True
		return keybrd_interupt,cfgData,File_Full			
	except KeyboardInterrupt:
		print()
		print("Interupt while in edit_cfgData")
		print()
		# Interupt while editing so return current data and save it to file.
		# Flag will be used in main prog to continue
		with open(cfgDataFileName, 'w') as cfgDataFile:
			json.dump(cfgData, cfgDataFile)
		keybrd_interupt = True
		# Signal if interupted when editing not finished
		File_Full = File_read or (email_to_count >  0)
		return keybrd_interupt,cfgData,File_Full

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
