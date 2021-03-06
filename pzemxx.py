#!/usr/bin/python
import logging, minimalmodbus
#from apscheduler.scheduler import Scheduler #Advanced Python Scheduler v2.12
from time import sleep

pz = minimalmodbus.Instrument("/dev/ttyUSB0", 1)
pz.serial.timeout = 0.1 # had to bump this up from the default of 0.05
pz.serial.baudrate = 9600
logging.basicConfig()
#sched = Scheduler()
#sched.start()

def read_meter():
	VOLT = pz.read_register(0, 0, 4)
	AMPS = pz.read_register(1, 0, 4)
	WATT = pz.read_register(3, 0, 4)
	WHRS = pz.read_register(5, 0, 4)
	FREQ = pz.read_register(7, 0, 4)
	PWRF = pz.read_register(8, 0, 4)
	print(VOLT * 0.1)
	print(AMPS * 0.001)
	print(WATT * 0.1)
	print(WHRS)
	print(FREQ * 0.1)
	print(PWRF * 0.01)
	print()

def main():
	while True:
		sleep(2)	#sched.add_cron_job(read_meter, second='*/1')
		read_meter()


if __name__ == "__main__":
	main()
