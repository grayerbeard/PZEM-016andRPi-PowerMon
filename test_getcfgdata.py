#!/usr/bin/env python

# test the subroutine that gets the contents of cfgData.json

from cfgData import edit_cfgData , get_cfgData, password_decrypt

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
	cfgDataRequiredKeys = ["emailFrom","token","mailSMTP","mailPort","subject","emailTo"]
	###
	for ind in range(0,len(cfgDataRequiredKeys)):
		print(ind, " : ",cfgDataRequiredKeys[ind])
	#Types Are;
	#0 email
	#1 password
	#2 server
	#3 positive integer
	#4 text
	#5 list emails
	cfgDataType = [0,1,2,3,4,5]
	cfgDataPrompt = ["Enter email addres for sending Emails",
					"Enter Password for email sending",
					"Enter Email Send Server"
					"Enter Email server Port Number"
					"Enter Email Subject"
					"Enter email addresses to send to"]
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

	FileReadResult , cfgData = get_cfgData(cfgDataFileName,cfgDataRequiredKeys,cfgDataDefaults)
	
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

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
