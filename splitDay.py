#!/usr/bin/env python3

import datetime

class class_splitDay(object):
	# Tests for Current time to 
	# enable easy divide of day into equal length
	# slots
	def __init__(self,timeNow,numberOfSplits):
		self.__splitLength = round(60 * 24/numberOfSplits,0)/60
		self.__dayTimeHourMin = timeNow.hour + (timeNow.minute/60)
		self.__lastStepNumber = int(self.__dayTimeHourMin / self.__splitLength)
		self.stepNumber = self.__lastStepNumber
		
	def checkSplit(self,timeNow):
		self.__dayTimeHourMin = timeNow.hour + (timeNow.minute/60)
		self.stepNumber = int(self.__dayTimeHourMin / self.__splitLength)
		if self.stepNumber != self.__lastStepNumber:
			self.__lastStepNumber = self.stepNumber
			return True
		else:
			return False
