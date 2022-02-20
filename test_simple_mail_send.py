#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_simple_mail_send.py
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
import simple_mail_send as send_mail
from datetime import datetime
# test change

def main(args):
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mailSMTP = 'mail.smalle.uk'
    mailPort =  465
    embedtype = 'png'
    password = 'TU6v65niddy'
    email_from  = 'rpi_send@smalle.uk'
    emails_to = ['djgtorrens@gmail.com',
                'david.torrens@outlook.com',
                'djgtorrens@yahoo.co.uk']
    filenames = ['/home/pi/energyMaster/energyMaster_logDetails_Light.csv',
                 '/home/pi/python3_test/simple_mail_send.txt',
                 '/home/pi/python3_test/test_simple_mail_send.txt',
                 '/home/pi/energyMaster/test.png']
    htmlintro = f'''
        <html>
            <body>
                <h1>WMIS Energy Report {date_str}</h1>
                <p>Hello, welcome to your report!</p>
                '''

    
    subject = f'WMIS Energy Report - {date_str}'
    send_mail.send_mail(mailSMTP,mailPort,password,email_from,emails_to,subject,htmlintro,filenames,embedtype)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
