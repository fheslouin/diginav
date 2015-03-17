#!/usr/bin/python
# -*- coding: utf-8 -*-

# code Python obtenu avec l'IDE Pyduino - www.mon-club-elec.fr 

#from pyduino_pcduino import * # importe les fonctions Arduino pour Python


import BMP085 as BMP085
import os, threading
from LatLon import LatLon
from bottle import route, run, template, static_file # importe classes utile du module Bottle
from gps import *
from time import *
from serial import *
from threading import Thread
from templateHtml import *
from javaScriptCode import *

gpsd = None #seting the global variable
ampd = None
dataAmp = '0'
dataPressure = '0'
dataTemperature = '0'
FileDataAmp = '/home/olimex/diginav/data/dataAmp.txt'
FileDataPressure = '/home/olimex/diginav/data/dataPressure.txt'

#----GPS data
class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd #bring it in scope
		gpsd = gps(mode=1) #starting the stream of info
		self.current_value = None
		self.running = True #setting the thread running to true

	def run(self):
		global gpsd
		while gpsp.running:
			gpsd.next()

#----Get data from amp sensor
def receivingDataAmp(ser):
	global dataAmp
	buffer = ''

	try:
		while True:
			buffer += ser.read(1024)
			if '\n' in buffer:
				dataAmp, buffer = buffer.split('\n')[-2:]
	except:
		dataAmp = '0'
		ser.close()
		
def dataLoggerAmp():
	global dataAmp

	fileAmp = open(FileDataAmp,'a')
	
	try:
		fileAmp.write(str(time.strftime('%H:%M',time.localtime()))+',')
		fileAmp.write(str('{0}'.format(dataAmp)))
		fileAmp.write('\n')
		
		threading.Timer(300, dataLoggerAmp).start()
		
	except:
		print "Le fichier", FileDataAmp, "est introuvable"
	finally:
		fileAmp.close
	
	return 0

#----Get data from pressure sensor
def receivingDataPressure(sensor):
	global dataPressure
	global dataTemperature

	try:
		while True:
			dataPressure = sensor.read_sealevel_pressure() / 100
			dataTemperature = sensor.read_temperature()
	except:
		dataPressure = '0'
		dataTemperature = '0'
	
def dataLoggerPressure():
	global dataPressure
	global dataTemperature

	filePressure = open(FileDataPressure,'a')
	
	try:		
		filePressure.write(str(time.strftime('%H:%M',time.localtime()))+',')
		filePressure.write(str(dataTemperature)+',')
		filePressure.write(str(dataPressure))
		filePressure.write('\n')

		threading.Timer(300, dataLoggerPressure).start()
		
	except:
		print "Le fichier", FileDataPressure, "est introuvable"
	finally:
		filePressure.close
	
	return 0

# dependances : 
# sudo apt-get install python-bottle
# sudo apt-get install python-cherrypy3 (pour serveur multithread)

# entete declarative
noLoop=True # bloque loop
affichage = ""

#ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
#ipLocale="127.0.0.1"


port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

#---- les routes doivent etre definies avant lancement bottle

#--- gestion requetes HTML --- 
@route('/')
def bottleHtmlInitial():
	return pageInitialeHTMLJS("accueil")
	
#--- gestion requetes HTML --- 
@route('/afficheur')
def bottleHtmlInitial():
	return pageInitialeHTMLJS("afficheur")
	
@route('/graphPressure')
def bottleHtmlInitial():
	return pageInitialeHTMLJS("graphPressure")
	
@route('/graphAmp')
def bottleHtmlInitial():
	return pageInitialeHTMLJS("graphAmp")

@route('/ajax/') # la meme chaine a mettre dans code JS initial requete AJAX
def bottleReponseAjax():
	return reponseAJAX()

#-- route pour gestion fichier statique pour libairie js locale 
@route('/static/<filename:path>')
def send_static(filename):
	return static_file(filename, root='/home/olimex/diginav/static/') # utilisation chemin relatif
	# le rep /static doit exister dans rép app *.py--
	#return static_file(filename, root=currentdir()+'static/') # si utilisation chemin absolu
	
@route('/data/<filename:path>')
def send_static(filename):
	return static_file(filename, root='/home/olimex/diginav/data/') # utilisation chemin relatif

#--- setup ---
def setup():
	
	global gpsp
	
	try:
		ser = Serial(
			port='/dev/ttyACM0',
			baudrate=9600,
			bytesize=EIGHTBITS,
			parity=PARITY_NONE,
			stopbits=STOPBITS_ONE,
			timeout=0.1,
			xonxoff=0,
			rtscts=0,
			interCharTimeout=None
		)
		
		Thread(target=receivingDataAmp, args=(ser,)).start()
		time.sleep (2)
		dataLoggerAmp()
	except:
		global dataAmp
		dataAmp = '0'
	
	try:
		sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
		
		Thread(target=receivingDataPressure, args=(sensor,)).start()
		time.sleep (2)
		dataLoggerPressure()
	except (ValueError, TypeError, IOError, UnboundLocalError):
		global dataPressure
		dataPressure = '0'
		
		
	
	gpsp = GpsPoller() # create the thread
	gpsp.start() # start it up
	
	run(host='0.0.0.0',port=port, server='cherrypy') # bottle lance automatiquement le wsgiserver de cherrypy (multithread)
	
#--- fin setup

# -- loop --
def loop():
	return
# -- fin loop --

#--- fonction fournissant la page HTML ---
def pageInitialeHTMLJS(affichage):

	pageHTML=( # debut page HTML
	"""
	<!DOCTYPE HTML> 
	<html>
		<head> 
			<meta charset="utf-8" />
			<title>DigiNav</title>
			"""
			+includeJS(affichage)+
			"""
			<script language="javascript" type="text/javascript"> 
			"""
			+codeJS(affichage)+
			"""
			</script> 
		</head> 

		<body>
			"""
			+bodyHTML(affichage)+
			"""
		</body> 
	</html> 
	"""
	)  # fin page HTML

	return pageHTML # la fonction renvoie la page HTML

#------ fonction retournant le body de la page HTML ---- 
def bodyHTML(affichage):
		
	if affichage == "afficheur":
		return htmlAfficheur
		
	elif affichage == "graphPressure":
		return htmlGraphPressure
					
	elif affichage == "graphAmp":
		return htmlGraphAmp
		
	else:
		return htmlMainPage
	
#------ fonction fournissant les fichiers JS a inclure -----
def includeJS(affichage):
	
	if affichage == "afficheur":
		return jsIncDisplay
	else:
		return jsIncMain
		 
#------ fonction fournissant le code Javascript / jQuery de la page HTML----
def codeJS(affichage):
	
	if affichage == "afficheur":
		return jsCodeDisplay
		
	elif affichage == "graphPressure":		
		return jsCodePressure
		
	elif affichage == "graphAmp":		
		return jsCodeAmp
		
	else:
		return jsCodeMain

#--- fin du code Javascript / jQuery  ---



#===================== Envoi Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX

#def reponseAJAX(paramIn):
def reponseAJAX():
	
	global gpsd
	global dataAmp
	global dataPressure
	global dataTemperature
	cogFix = '0'

	if dataPressure == "0":
		pressure = "No Data"
		temperature = "No Data"
	else:
		pressure = '{0:0.1f} hPa'.format(dataPressure)
		temperature = '{0:0.1f} °C'.format(dataTemperature)
		
	try:
		gps = LatLon(gpsd.fix.latitude, gpsd.fix.longitude)
		degMin = gps.to_string('d% %m%')
		sec = gps.to_string('%S%')
		hemis = gps.to_string('%H')		
		latdegMin = degMin[0].strip("-(')")
		londegMin = degMin[1].strip("-(')")	
		latSec = '{0:0.3f}'.format(float(sec[0].strip("(')")))
		lonSec = '{0:0.3f}'.format(float(sec[1].strip("(')")))
		lathemis = hemis[0].strip("(')")
		lonhemis = hemis[1].strip("(')")
		
		latitude = latdegMin+" "+latSec+" "+lathemis
		longitude = londegMin+" "+lonSec+" "+lonhemis
		
		cog = '{0:0.1f}°'.format(gpsd.fix.track)
		sog = '{0:0.1f} Kts'.format(gpsd.fix.speed * 1.852)

	except (ValueError, TypeError, IOError, UnboundLocalError):
		sog = "No Data"
		latitude = "No Data"
		longitude = "No Data"
		cog = "No Data"
		
	if dataAmp == "0":
		amp = "No Data"
	else:
		amp = '{0} Ah'.format(dataAmp)
		
	reponseAjax=(
	str(temperature)+","
	+str(pressure)+","
	+str(sog)+","
	+str(latitude)+","
	+str(longitude)+","
	+str(cog)+","
	+str(amp)
	)  
	return reponseAjax

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
