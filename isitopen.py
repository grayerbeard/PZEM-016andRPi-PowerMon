#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

daysOpen = (3,4)
openTime =  7
closeTime = 17

x = datetime.now()
print(daysOpen,openTime,closeTime)

for count in range(1,(24*7)):
	if not((lst.weekday() in daysOpen) and (openTime <= lst.hour < closeTime)):
		message = "shed closed"
	else:
		message = "shed open"
	lst += timedelta(hours=1)
	



