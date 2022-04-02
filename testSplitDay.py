#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  splitDayTest.py
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
# Standard library imports

import datetime
from sys import exit as sys_exit
from splitDay import class_splitDay


def main(args):
	myHour = 2
	myMinute = 0
	numLogsPerDay = 8
	logTime = datetime.datetime(2022, 3, 1,myHour,myMinute)
	stepTest = class_splitDay(logTime,numLogsPerDay)
	goFlag = True
	while goFlag:
		logTime = datetime.datetime(2022, 3, 1,myHour,myMinute)
		if stepTest.checkSplit(logTime):
			print(logTime.strftime('%H:%M'),"StepChange to",stepTest.stepNumber)
		else:
			print(logTime.strftime('%H:%M'))
		myMinute += 20
		if myMinute > 59 :
			myMinute = 0
			myHour += 1
		if myHour > 23:
			goFlag = False
			sys_exit()
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
