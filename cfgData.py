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

def checkInputType(inputItem):
		# Determine the type of input
	inType = 99 
	try:
	# Try to Convert it into integer
		intVal = int(inputItem)
		if intVal > 0:
			inType = "int" # positive integer
			if intVal > 999999:
				inType = "lint" # Large Positive Integer
		else:
			inType = "nint" # negative integer
			if intVal < -999999:
				inType = "lnint" # Large Integer
	except ValueError:
		try:
			# Convert it into float
			floatVal = float(inputItem)
			if floatVal > 0:
				inType = "float" # Positive float
				if floatVal > 999999:
					inType = "lfloat" # Large Positive Float
			else:
				inType = -2 # negative float
				if floatVal < -999999:
					inType = "lnfloat" # Large Negative Float
		except ValueError:
			if len(inputItem) > 5 :
				inType = "lstring" # its a string of at least 6 characters
			else:
				inType = "string" # its a string
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
	if itemType in ("email","emails"):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	elif itemType == "server":
		regex = r'\b[A-Za-z0-9._%+-]+\.[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	else:
		regex = ""

	inType = checkInputType(inputItem)

			# Check the input is the required type
	result = False
	if itemType in ("pwd","subj"):  # should just be 6 characters or more
		if inType in ("lstring","lint"):
			result = True
	elif itemType in ("email","server","emails"): # should be an email or server or list of email
		if inType == "lstring":
			print("checking pattern")
			if(re.fullmatch(regex, inputItem)):
				result = True
	elif itemType == "port": # server port
		if inType in ("int"):
			result = True
	else:
		print("Error in Input test item has no type")
	if not result:
		print("itemType  " ,itemType) 
		print("inType  ", inType)
	return result

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
			try:
				cfgData_file_data = json.load(cfgDataFile)
			except:
				print("Cannot read in file line 164")
				FileReadResult = 0
				exit
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
				if cfgDataType[indexEdit] == "emails" : # Its a list 
					print("Editing List item: ",indexList, " d delete item, f finish with list")
					print(cfgDataPrompt[indexEdit])
					if indexList < len(cfgDataItem):
						print("Existing Value: ",cfgDataItem[indexList])
						inputValue = input() or cfgDataItem[indexList]
					else:
						print("No Existing Value")
						inputValue = input() 
					if inputValue == "d":
						del cfgDataItem[indexList]
						print("Deleting old value")
					elif (inputValue == "f") and (indexList > 0):
						print("Finished editing Send to Emails")
						print("Old Value of List : ",cfgData[key])
						print("New Value of List : ",cfgDataItem)
						cfgData[key] = cfgDataItem
						break
					elif (inputValue == "f"):
						print("Must enter at least one send email address")
					else:
						if check(inputValue,cfgDataType[indexEdit]):
							if indexList < len(cfgDataItem):
								cfgDataItem[indexList] = inputValue
								print("replacing")
							else:
								cfgDataItem.append(inputValue)
								print("appending")
							indexList += 1
						else:
							print("\n Not a valid email try again \n")
				else: # So Not a list
					print("\n",key,indexEdit,cfgDataPrompt[indexEdit])
					if cfgDataType[indexEdit] == "pwd":
						inputValue = input() or password_decrypt(cfgDataItem)
						if check(inputValue,cfgDataType[indexEdit]):
							cfgData[key] = password_encrypt(inputValue)
							break
						else:
							print("\n Entry not valid try again \n")	
					else:
						print("Existing Value: ",cfgDataItem)
						inputValue = input() or cfgDataItem
						if check(inputValue,cfgDataType[indexEdit]):
							cfgData[key] = inputValue
							break
						else:
							print("\n Entry not valid try again \n")

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
if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
