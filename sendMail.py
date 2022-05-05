#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sendMail.py
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
# Based on this Blog
#  https://www.justintodata.com/send-email-using-python-tutorial/#send-your-first-email-with-secure-smtp-server-connection

 
# Import modules 
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from cfgData import edit_cfgData , get_cfgData, password_decrypt
import os
import imghdr
from utility import fileexists,pr,make_time_text
from sys import exit as sys_exit

try:
	import json
except ImportError:
	try:
		import simplejson as json
	except ImportError:
		print("Error: import json module failed")
		sys.exit()
encoding = 'utf-8'


def password_key() :
	 global fernetKey
	 #Generate the password key based on the MachineID
	 #This is used both to encrypt and decrypt the Email send password 
	 keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
	 fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))

def attach_file_to_email(email_message, filename,ImageID = None):
	# Open the attachment file for reading in binary mode, and make it a MIMEApplication class
	with open(filename, "rb") as f:
		file_attachment = MIMEApplication(f.read())
	# Add header/name to the attachments	
	file_attachment.add_header("Content-Disposition",f"attachment; filename={os.path.basename(filename)}")
	
	# Set up the input extra_headers for img
	## Default is None: since for regular file attachments, it's not needed
	## When given a value: the following code will run
	### Used to set the cid for image
	if ImageID is not None:
		extra_headers = {'Content-ID': ImageID}
		print(extra_headers)
		for name, value in extra_headers.items():
			file_attachment.add_header(name, value)
	# Attach the file to the message
	email_message.attach(file_attachment)

def sendMail(cfgData,htmlintro,filenames,embedtype,loghtml):

		#Generate the Password Key based on the MachineID
# email_from	: a single email; address
# token 		: the encrypted password
# emailsTo		: a list of email addresses to send emails to (can be just one)
# mailSMTP		: the address of the server for sending email
# mailPort		: port number for sending email e.g. 465
# subject		: Text to put in the email subject

	for filename in filenames:
		if fileexists(filename) == False:
			print(filename," does not exist")
			sys_exit()
		#emailsTo  = cfgData["emailsTo"]
	for emailTo in cfgData["emailsTo"] :
		print("Sending to : ",emailTo)
			# Create a MIMEMultipart class, and set up the From, To, Subject fields
		email_message = MIMEMultipart()
		email_message['From'] = cfgData['emailFrom']
		email_message['To'] = emailTo
		email_message['Subject'] = cfgData["subject"] 

			# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
		html = htmlintro
		for rn in range(0,len(filenames)):
			try:
				#print(filenames[rn],imghdr.what(filenames[rn]))		 
				if imghdr.what(filenames[rn]) == embedtype:
					ImageID = 'myimageid' +  str(rn)
					#print(ImageID)
					html = f'''{html}<img src='cid:{ImageID}' width="700">
							'''
					#print(rn,filenames[0][rn],"  Will be embedded.")
				else:
					html = html
					#print("This file not image :" + filenames[rn])
			except:
				print("Error with Filenames to send")
				html = html + "@@@ Error in Send Mail lines 97 to 103 with Filenames to send @@@@"
				
		html = f'''{html} {loghtml}
			</body>
		</html>
		'''
		#print(html)
	
		email_message.attach(MIMEText(html, "html"))
			#Attach Files
		
		#print("\n sendmail line 124 filenames in email : ",filenames, "\n logfile is :", logFile)
		try:
			for rn in range(0,len(filenames)):
			   #print(filenames[0][rn],filenames[1][rn])
				if imghdr.what(filenames[rn]) == embedtype:
					attach_file_to_email(email_message,filenames[rn],ImageID)
				else:	
					attach_file_to_email(email_message,filenames[rn])
		except:
			print("error with filenames")
			# Convert it as a string
		email_string = email_message.as_string()

			# Connect to the Gmail SMTP server and Send Email
		context = ssl.create_default_context()
		try:
			with smtplib.SMTP_SSL(cfgData["mailSMTP"], cfgData["mailPort"],timeout = 1, context=context) as server:
				server.login(cfgData['emailFrom'], password_decrypt(cfgData['token']))
				server.sendmail(cfgData['emailFrom'], emailTo, email_string)
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print(message)

