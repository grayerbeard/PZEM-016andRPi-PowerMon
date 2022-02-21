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
import cfgData

def main(args):
	# Test the cfgData module
	existing , cfgData = get_cfgData()
	
	if existing :
		print(cfgData)
	else:
		print("no file present so lets make")
		edit_cfgData(existing,cfgData)
		existing = True
	try:
		while(True):
			# Repeatedly test editing cfgData,  Press Ctrl C to exit
			print("Repeatedly test editing cfgData,  Press Ctrl C to exit")
			edit_cfgData(existing,cfgData)
    except KeyboardInterrupt
		print("Exiting...")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
