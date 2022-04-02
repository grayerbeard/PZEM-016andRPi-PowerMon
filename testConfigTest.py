#!/usr/bin/env python3

from configTest import class_config

from utility import fileexists,pr,make_time_text
###

def main(args):
    
	logTime = datetime.datetime.now()
	config = class_config(logTime)
	#if fileexists(config.config_filename):	
	if fileexists("configTest.cfg")
		#print( "will try to read Config File : " ,config.config_filename)
		print( "will try to read Config File : " ,"configTest.cfg")
		config.read_file() # overwrites from file
	else : # no file so file needs to be writen
		config.write_file()
		print("New Config File Made with default values, you probably need to edit it")
		
	config.scan_count = 0
	
	allHeadings = ["Voltage","Amps","Power","Energy","Hz","PF", \
				"PZEMpeak","PZEMaverage","calcPower","calcPeak","calcAverage","Recent Power","Message"]
	pzemHeadings = ["Voltage","Amps","Power","Energy","Hz","PF"]
	#logBuffer = class_text_buffer(allHeadings,config,"log",logTime)
	#debugHeadings = ["Topic","Message","Value1","Value2"]
	#debugBuffer = class_text_buffer(debugHeadings,config,"debug",logTime)
	
	sensor = class_my_sensors(config,logTime)
	
	# Set The Initial Conditions
	the_end_time = logTime
	last_total = 0
	loop_time = 0
	correction = 7.5
	# Ensure start right by inc buffer
	#last_fan_state = True
	#buffer_increment_flag = False
	if config.scan_delay > 6 :
		refresh_time = config.scan_delay * 0.5 # How often to refresh the browser display#
	else:
		refresh_time = config.scan_delay

	
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
	filenames = ['/home/pi/powerMonitor/powerMonitor_log.html',
				 '/home/pi/powerMonitor/test.png']
	print(filenames)
	date_str = logTime.strftime('%Y-%m-%d %H:%M:%S')
	htmlintro = f'''
		<html>
			<body>
				<h1>WMIS Energy Report {date_str}</h1>
				<p>Hello, welcome to your report!</p>
				'''
	chanPorts = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
	chanAddrs = [0x01, 0x01]
	chan = 0

	initialReadings = readAcPZEM(chanPorts[chan], chanAddrs[chan],pzemHeadings)
	smoothedPower = round(initialReadings["Power"],3)

	#  Shed open times
	daysOpen = (2,3)
	openTime =  6
	closeTime = 17

	# List For Averages and Peaks
	#readingsListsLength = 70 #70
	#readingsListPower = [round(float(initialReadings["Power"]),2)] * readingsListsLength
	#initialReadings["calcPower"] = round(initialReadings["Voltage"] * initialReadings["Amps"] \
	#					* initialReadings["PF"],2)
	#readingsListCalcPower = [float(initialReadings["calcPower"])] * readingsListsLength
	#readingsListsIndex = 0
	
	#Limits and delays set up
	minAveragePowerToLog = 50 #  USUALLY 50
	

	limitSinceLogMINS = 10 # normally 10 (minutes)  must not log morte often than this
	limitSinceLogSecs = (limitSinceLogMINS * 60) - (0.5 * config.scan_delay)
	limitSinceEmailHOURS = 3  # normally 3
	limitSinceEmailSecs = (limitSinceEmailHOURS * 60 * 60) - (0.5 * config.scan_delay)
	
	# Set so can operate soon after program started to make testing
	timeLastLog = logTime - datetime.timedelta(seconds = 10)
	timeLastEmail = logTime - datetime.timedelta(seconds = 10)
	
	timeSinceLog = (logTime - timeLastLog).total_seconds
	timeSinceEmail = (logTime - timeLastEmail).total_seconds
	
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
			
	increment = False # flag crontrollein incrementing the text buffer
	
	debugIncrement = True
	debugBuffer.line_values["Topic"] = "Start"
	debugBuffer.line_values["Message"] = "Scan Limits For log and email"
	debugBuffer.line_values["Value1"] = timeSinceLog
	debugBuffer.line_values["Value2"] = timeSinceEmail
	#debugBuffer.pr(debugIncrement,0,logTime,refresh_time)
	
	debugIncrement = True
	debugBuffer.line_values["Topic"] = "Start"
	debugBuffer.line_values["Message"] = "Scan Limits For log and email"
	debugBuffer.line_values["Value1"] = timeSinceLog
	debugBuffer.line_values["Value2"] = timeSinceEmail
	#debugBuffer.pr(debugIncrement,0,logTime,refresh_time)
	
	
	powerAverageingTotal = 0
	calcPowerAverageingTotal = 0
	readingsCount = 0
	powerPeak = 0
	calcPowerPeak = 0
	startHold = True
	lastHoldMin = logTime.minute 

	
	
	while (config.scan_count <= config.max_scans) or (config.max_scans == 0):
		try:
			###
			#print("config.scan_count : ", config.scan_count, "  scansSinceLog : ",
				#scansSinceLog, "  scansSinceEmail : ",scansSinceEmail," slp: ",sleep_time)
			# Loop Management and Watchdog
			while startHold:
				holdMin = datetime.datetime.now().minute
				if holdMin != lastHoldMin:
					startHold = False
			logTime = datetime.datetime.now()
			timeSinceLog = (logTime - timeLastLog).total_seconds()
			timeSinceEmail = (logTime - timeLastEmail).total_seconds()
			
			if not((logTime.weekday() in daysOpen) and (openTime <= logTime.hour < closeTime)):
				message = "closed"
				shedClosed = True
			else:
				message = "open"
				shedClosed = False
			newLogStep = stepTest.checkSplit(logTime)
			temp = sensor.get_temp()
			pzemReading = readAcPZEM(chanPorts[chan], chanAddrs[chan],pzemHeadings)
			readingsCount += 1
			smoothedPower = round(smoothedPower + (0.05 * (pzemReading["Power"] - smoothedPower)),3)  
			message = message + " rdg:" + str(readingsCount) + " logStep:" + str(stepTest.stepNumber)
			#########################################
			# These must be done in the right Order #
			#########################################
			powerAverageingTotal +=  round(pzemReading["Power"],2)
			calcPower = round(float(pzemReading["Voltage"]) * \
					float(pzemReading["Amps"]) * float(pzemReading["PF"]),2)
			calcPowerAverageingTotal += calcPower
			if pzemReading["Power"] > powerPeak :
				powerPeak = round(pzemReading["Power"],2)
			pzemReading["PZEMpeak"] = powerPeak  # 1
			if calcPower > calcPowerPeak:
				calcPowerPeak = calcPower
			pzemReading["PZEMaverage"] = round(powerAverageingTotal/readingsCount,2)  # 2
			pzemReading["calcPower"] = calcPower # 3
			pzemReading["calcPeak"] = calcPowerPeak # 4
			pzemReading["calcAverage"] = round(calcPowerAverageingTotal/readingsCount,2) # 5
			pzemReading["Recent Power"] = smoothedPower
			pzemReading["Message"] = message # 6

			#if readingsListsIndex > readingsListsLength -2 :
			#	readingsListsIndex = 0
			#else:
			#	readingsListsIndex += 1

			logBuffer.line_values = pzemReading

			if ((timeSinceLog >= limitSinceLogSecs) and (smoothedPower > minAveragePowerToLog )) or  \
					(config.scan_count < 2) or newLogStep: 
				increment = True
				config.scan_count += 1
				#scansSinceLog = 0
				timeLastLog = logTime
				readingsCount = 0
				powerAverageingTotal = 0
				calcPowerAverageingTotal = 0
				powerPeak = 0
				calcPowerPeak = 0
				
				if (timeSinceEmail > limitSinceEmailSecs) and (smoothedPower > minAveragePowerToLog ) and shedClosed :
					sendMail(cfgData,htmlintro,filenames,logBuffer.logFile,embedtype,logBuffer.email_html)
					#scansSinceEmail = 0
					timeLastEmail = logTime
					
			else:	 
				increment = False
				
			debugIncrement = True
			debugBuffer.line_values["Topic"] = "Start"
			debugBuffer.line_values["Message"] = "Scan Limits For log and email"
			debugBuffer.line_values["Value1"] = timeSinceLog
			debugBuffer.line_values["Value2"] = timeSinceEmail
			#debugBuffer.pr(debugIncrement,0,logTime,refresh_time)
				
			logBuffer.pr(increment,0,logTime,refresh_time)	
	
			# Loop Managemntn^^^
			loop_end_time = datetime.datetime.now()
			loop_time = (loop_end_time - logTime).total_seconds()
			# Adjust the sleep time to aceive the target loop time and apply
			# with a slow acting correction added in to gradually improve accuracy
			if loop_time < (config.scan_delay - (correction/1000)):
				sleep_time = config.scan_delay - loop_time - (correction/1000)
				try:
					time_sleep(sleep_time)
				except KeyboardInterrupt:
					print("........Ctrl+C pressed... Output Off")
					time_sleep(3)
					sys_exit()
				except ValueError:
					print("sleep_Time Error value is: ",sleep_time, "loop_time: ",
					      loop_time,"correction/1000 : ",correction/1000)
					print("Will do sleep using config.scan_delay and reset correction to 7.5msec")
					correction = 7.5
					time_sleep(config.scan_delay)
				except Exception:
					print("some other error with time_sleep try with config.scan_delay")
					time_sleep(config.scan_delay) 
			else:
				time_sleep(config.scan_delay)
			last_end = the_end_time
			the_end_time = datetime.datetime.now()
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
			time_sleep(3) 
			sys_exit()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))	
