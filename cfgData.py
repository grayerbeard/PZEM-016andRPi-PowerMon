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

def checkinputtype(inputItem):
		# Determine the type of input
	inType = 99 
	try:
	# Try to Convert it into integer
		intval = int(inputItem)
		if intval > 0:
			inType = 1 # positive integer
			if intVal > 999999:
				inType = 10 # Large Positive Integer
		else:
			inType = -1 # negative integer
			if intVal < 999999:
				inType = -10 # Large Integer
	except ValueError:
		try:
			# Convert it into float
			floatval = float(inputItem)
			if floatval > 0:
				inType = 2 # positive float
				if intVal > 999999:
					inType = 20 # Large Positive Integer
			else:
				inType = 3 # negative float
				if intVal < 999999:
					inType = -20 # Large Positive Integer
		except ValueError:
			print("failed convert to float")
			if len(inputItem) > 5 :
				print("string longer than 5")
				inType = 5 # its a string of at least 6 characters
			else:
				print("string shorter than 5")
				inType = 4 # its a string
	print("Intype is : ",inType)
	return inType



def check(inputItem,itemType):
	encoding = 'utf-8'
	# Data types to be tested are
	#0 or >  4 are email
	#1 password
	#2 server
	#3 positive integer
	#4 text
		# Regular expression for validating email and server
	if itemType in (0,5):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	elif itemType == 2:
		regex = r'\b[A-Za-z0-9._%+-]+\.[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	else:
		regex = ""
	print("regex is : ",regex)

	inType = checkinputtype(inputItem)

			# Check the input is the required type
	result = False
	if itemType in (1,4):  # should just be 6 characters or more
		if inType in (5,20):
			result = True
	elif itemType in (0,2,5): # should be an email or server
		if(re.fullmatch(regex, inputItem)):
			result = True
	elif itemType == 3: # server port
		if inType == (1,10):
			result = True
	else:
		print("Error in Input test")
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
		# There is no file so return a flag and the Default values.
		FileReadResult = 0
		print("No file found returned defaults")
		print("Finished getCfgData, No File")
		print()
		return  FileReadResult,cfgDataDefaults

def edit_cfgData(cfgDataFileName,File_Read,cfgData,cfgDataType,cfgDataPrompt):	

	# Data tpes in the cfgData could be these where <5 are single values and
	# =>5 are lists.
	#Types Are;
	#0 email
	#1 password
	#2 server
	#3 positive integer
	#4 text
	#5 list emails

	try:
		indexEdit = -1
		for key in cfgData:
			indexEdit += 1 # So will start at zero
			indexList = 0
			cfgDataItem = cfgData[key]
			while True:
				if cfgDataType[indexEdit] > 4 : # Its a list 
					print("Editing a List: d delete item, f finish with list")
					print("Existing Value: ",cfgDataItem[indexList])
					print(cfgDataPrompt[indexEdit])
					if indexList < len(cfgDataItem):
						input_value = input() or cfgDataItem[indexList]
					else:
						input_value = input() 
					if input_value == "d":
						del cfgDataItem[indexList]
						print("Deleting old value")
					elif (input_value == "f") and (indexList > 0):
						print("Finished editing Send to Emails")
						cfgData[key] = cfgDataItem
						break
					elif (input_value == "f"):
						print("Must enter at least one send email address")
					else:
						if check(input_value,cfgDataType[indexEdit]):
							cfgDataItem[indexList] = input_value
							indexList += 1
						else:
							print()
							print("Not a valid email try again")
							print()
				else: # So Not a list
					print("Existing Value: ",cfgDataItem)
					print(cfgDataPrompt[indexEdit])
					input_value = input() or cfgDataItem
					if check(input_value,cfgDataType[indexEdit]):
						cfgData[key] = input_value
						indexList += 1
						break
					else:
						print("Entry no valid try again")

#               All done editing

#               Put data into json file

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

#                          O R I G I N A L
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
