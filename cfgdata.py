#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cfgdata.py
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

def password_encrypt(phrase):
	#Generate the token for securely storong password from the password
	keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
	fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))
	token = fernetKey.encrypt(bytes(phrase,encoding))
	return token.decode(encoding)

def password_decrypt(token):
	#generate the password from the token
	keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
	fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))
	phrase = fernetKey.decrypt(bytes(token,encoding))
	return phrase.decode(encoding)

def get_cfgData()
	cfgDataFileName = "cfgData.json"
	cfgData = dict()

	# Tries to get cfgData from file
	# If successful returns True
	# if not returns False (so new file needed

	try:
		with open(cfgDataFileName, 'r') as cfgDataFile:
			cfgData_file_data = json.load(cfgDataFile)
			# If file loaded, replace default values in cfgData with values from file
			print("Values in Config File")
			for key in cfgData_file_data:   
				print( key, ": = ",cfgData_file_data[key])
				cfgData[key] = cfgData_file_data[key]
			return = True

	except IOError:  
		return  = False

	
	while True:
		if existing:
			print("Existing Value for Senders Email :",cfgData['email_from'])
			print("Enter new or Press enter to leave unchanged")
		else:
			cfgData['email_from'] = ""
			print("Enter email SENDER's email address")   

		cfgData['email_from'] = input() or cfgData['email_from']
		if check(cfgData['email_from']):
			break
		else:
			print("Not a valid email try again")
		
	print("Send Email Address set to: ",cfgData['email_from'])

	while True:
		if existing:
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
			print("Password required")
	
	print("Password now :  ",password_decrypt(cfgData['token']))



	
	print(cfgData)
	
	
	if existing:
		emailto = cfgData["emails_to"]
	else:
		emailto = [""]
	count = 0
	while True :
		if count < len(emailto) and existing:

			print("Number : ",count + 1, " Email address :",emailto[count])
			print("Either enter replacement Or d to delete or enter to leave as is")

			input_value = input() or emailto[count]
 
			if input_value == "d":
				del emailto[count]
				print("Deleting old value")
			elif input_value == "f":
				print("finished")
				break
			else:
				if check(input_value):
					emailto[count] = input_value
					count += 1
				else:
					print("Not a valid email try again")
		else:	
			print("Enter a new recipient's email",count)
			print("when filished just enter f")
			print("Enter a new value")
			input_value = input()
			if input_value == "f":
				print("finished")
				break
			else:
				if check(input_value):
					emailto.append(input_value)
					count += 1
				else:
					print("Not a valid email try again")
						
	cfgData['emails_to'] = emailto
	for key in cfgData:   
		print( key, ": = ",cfgData[key])

	with open(cfgDataFileName, 'w') as cfgDataFile:
		json.dump(cfgData, cfgDataFile)

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
