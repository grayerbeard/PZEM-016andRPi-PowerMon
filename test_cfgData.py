#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tesst_cfgData.py
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
from cfgData import edit_cfgData , get_cfgData, password_decrypt

def main(args):
	cfgDataFileName = "cfgData.json"
	# Test the cfgData module
	File_Read , cfgData = get_cfgData(cfgDataFileName)
	
	if File_Read :
		print(cfgData)
	else:
		
		print("no file present so lets make", File_Read)
		keybrd_interupt,cfgData,File_Full = edit_cfgData(cfgDataFileName,File_Read,cfgData)
		File_Read = File_Full
	try:
		# This Keyboard Interupt Flag signals an interupt while editing 
		keybrd_interupt = False
		while not keybrd_interupt:
			# Repeatedly test editing cfgData,  Press Ctrl C to exit
			print()
			print("Repeatedly testing editing cfgData,  Press Ctrl C to exit")
			keybrd_interupt,cfgData,File_Full = edit_cfgData(cfgDataFileName,File_Read,cfgData)
		print()
		print("Dropped back to Main Prog due to interupt whil editing")
		print()
	except KeyboardInterrupt:
		print()
		print("Interupt in main Program")
		print()
		File_Read , cfgData_filed = get_cfgData(cfgDataFileName)
		if cfgData_filed != cfgData:
			print("Edits may not have beeen saved to file")

		print
		print("Buffer Contents : ",cfgData)

		if File_Read :
			print("cfgData.json file contents : ",cfgData)
		else:
			print("No json file saved")
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
