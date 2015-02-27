#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015 root <root@a20-olimex>
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
import BMP085 as BMP085
import time

dataDigiNav = "/home/olimex/diginav/data/dataDigiNav.txt"

def main():
	fileData = open(dataDigiNav,'a')
	
	try:
		sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
		pressure = (sensor.read_sealevel_pressure() / 100)
		
		fileData.write(str(time.strftime('%H:%M',time.localtime()))+',')
		fileData.write(str(sensor.read_temperature())+',')
		fileData.write(str('{0:0.1f}'.format(pressure)))
		fileData.write('\n')
	except:
		print "Le fichier", dataDigiNav, "est introuvable"
	finally:
		fileData.close
	
	return 0

if __name__ == '__main__':
	main()

