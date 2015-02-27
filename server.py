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

gpsd = None #seting the global variable
ampd = None
last_received = ''
dataDigiNav = '/home/olimex/diginav/data/dataAmp.txt'

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

def receiving(ser):
	global last_received
	buffer = ''

	try:
		while True:
			buffer += ser.read(1024)
			if '\n' in buffer:
				last_received, buffer = buffer.split('\n')[-2:]
	except:
		last_received = '0'
		ser.close()
		
def dataLogger():
	fileData = open(dataDigiNav,'a')
	
	try:
		global last_received
			
		fileData.write(str(time.strftime('%H:%M:%S',time.localtime()))+',')
		fileData.write(str('{0}'.format(last_received)))
		fileData.write('\n')
		
		threading.Timer(300, dataLogger).start()
		
	except:
		print "Le fichier", dataDigiNav, "est introuvable"
	finally:
		fileData.close
	
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

#--- gestion requetes AJAX --- 
"""
@route('/ajax/<param>') # la meme chaine a mettre dans code JS initial requete AJAX
def bottleReponseAjax(param):
	return reponseAJAX(param)
"""

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
	
	#print "dir="+os.getcwd()+"/"+'static/' # debug
	#print "dir="+currentdir()+'static/' # debug
	
	global gpsp
	
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
	
	Thread(target=receiving, args=(ser,)).start()
	
	gpsp = GpsPoller() # create the thread
	gpsp.start() # start it up
	
	dataLogger()

	
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
		
		includeJS="""<script type="text/javascript" src="static/jquery-1.11.1.min.js"></script>"""	
		
	else:
		
		includeJS="""
		<link rel="stylesheet" href="static/jqx.base.css" type="text/css" />
		<link rel="stylesheet" href="static/opennav.css" type="text/css" />
		<link rel="stylesheet" href="static/bootstrap.min.css" type="text/css" />
		<script type="text/javascript" src="static/jquery-1.11.1.min.js"></script>
		<script type="text/javascript" src="static/bootstrap.min.js"></script>
		<script type="text/javascript" src="static/jqxcore.js"></script>
		<script type="text/javascript" src="static/jqxchart.js"></script>
		<script type="text/javascript" src="static/jqxgauge.js"></script>
		<script type="text/javascript" src="static/jqxdata.js"></script>
		<script type="text/javascript" src="static/jqxdraw.js"></script>
		<script type="text/javascript" src="static/jqxchart.core.js"></script>
		"""
		
	return includeJS

	
#------ fonction fournissant le code Javascript / jQuery de la page HTML----
def codeJS(affichage):
	
	if affichage == "afficheur":
		
		codeJS=(
		"""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500); // fixe délai actualisation

		}); // fin function + fin ready + fin $ 

		function refreshValues(){
			
			$.get("ajax/", manageReponseAjaxServeur); // envoi d'une requete AJAX
			
		} // fin refresh value
		"""
		+
		manageReponseAjaxServeur()
		+
		"""
		""")
		
	elif affichage == "graphPressure":		
		codeJS=(
		"""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500); // fixe délai actualisation
		
			$('#myModal').on('shown.bs.modal', function () {
				$('#myInput').focus()
			})

			// Graph for pressure
			var source =
            {
                datatype: "csv",
                datafields: [
                    { name: 'Date' },
                    { name: 'Temp' },
                    { name: 'Pressure' }
                    ],
                url: 'data/dataDigiNav.txt'
            };
            
			var dataAdapter = new $.jqx.dataAdapter(source,
			{
				async: false,
				autoBind: true,
			});
            // prepare jqxChart settings
            var settings = {
                title: "Préssion athmosphérique et température",
                description: "Temps réél",
                enableAnimations: true,
                animationDuration: 1000,
                enableAxisTextAnimation: true,
                showLegend: true,
                padding: { left: 5, top: 5, right: 5, bottom: 5 },
                titlePadding: { left: 0, top: 0, right: 0, bottom: 10 },
                source: dataAdapter,
			   enableAnimations: true,
			   xAxis: {
				   dataField: 'Date',
				   description: '',
				   baseUnit: 'houre',
				   unitInterval: 3,
				   showGridLines: true,
				   showTickMarks: true,
				   minValue: '00:00',
				   maxValue: '23:59',
				   valuesOnTicks: true,
				   textRotationAngle: -45,
				   textOffset: {
					   x: -17,
					   y: 0
				   }
			   },
			   
			   seriesGroups: [{
					type: 'stepline',
					valueAxis: {
						minValue: 930,
						maxValue: 1050,
						displayValueAxis: true,
						unitInterval: 10,
						description: 'en hPa',
						horizontalTextAlignment: 'right'
					},
					series: [{ emptyPointsDisplay: 'skip',	dataField: 'Pressure', displayText: 'Presure'}]
					},{
					
					type: 'spline',
					valueAxis:
					{
						position : 'right',
						minValue:-5,
						maxValue: 40,
						unitInterval: 5,
						displayValueAxis: true,
						description: '°C',
						showGridLines : false,
					},
					series: [{ dataField: 'Temp', displayText: 'Temperature' }]
					}]
		   };
            // create the chart
            $('#chartPressure').jqxChart(settings);
       
		}); // fin function + fin ready + fin $ 



		function refreshValues(){

			//$("#long").html((Math.random()*9999).toFixed(2));
			//$("#lat").html((Math.random()*9999).toFixed(2));
			//$("#vit").html((Math.random()*9999).toFixed(2));
			//$("#prof").html((Math.random()*9999).toFixed(2));
			
			$.get("ajax/", manageReponseAjaxServeur); // envoi d'une requete AJAX
			
		} // fin refresh value
		"""
		+

		manageReponseAjaxServeur()
		+
		"""
		""")
		
	elif affichage == "graphAmp":		
		codeJS=(
		"""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500); // fixe délai actualisation

        // Graph for amp
			var source =
            {
                datatype: "csv",
                datafields: [
                    { name: 'Date' },
                    { name: 'Amp' },
                    ],
                url: 'data/dataAmp.txt'
            };
            
			var dataAdapter = new $.jqx.dataAdapter(source,
			{
				async: false,
				autoBind: true,
			});
            // prepare jqxChart settings
            var settings = {
                title: "Evolution de la consommation ampérmètrique",
                description: "Temps réél",
                enableAnimations: true,
                animationDuration: 1000,
                enableAxisTextAnimation: true,
                showLegend: true,
                padding: { left: 5, top: 5, right: 5, bottom: 5 },
                titlePadding: { left: 0, top: 0, right: 0, bottom: 10 },
                source: dataAdapter,
			   enableAnimations: true,
			   xAxis: {
				   dataField: 'Date',
				   description: '',
				   baseUnit: 'minute',
				   unitInterval: 1,
				   showGridLines: true,
				   showTickMarks: true,
				   minValue: '00:00',
				   maxValue: '23:59',
				   valuesOnTicks: true,
				   textRotationAngle: -45,
				   textOffset: {
					   x: -17,
					   y: 0
				   }
			   },
			   
			   seriesGroups: [{
					type: 'stepline',
					valueAxis: {
						minValue: -25,
						maxValue: 25,
						displayValueAxis: true,
						unitInterval: 5,
						description: 'en Ah',
						horizontalTextAlignment: 'right'
					},
					series: [{ emptyPointsDisplay: 'skip', dataField: 'Amp', displayText: 'Ah'}]
					}]
		   };
            // create the chart
            $('#chartAmp').jqxChart(settings);
           
       		
		}); // fin function + fin ready + fin $ 



		function refreshValues(){

			//$("#long").html((Math.random()*9999).toFixed(2));
			//$("#lat").html((Math.random()*9999).toFixed(2));
			//$("#vit").html((Math.random()*9999).toFixed(2));
			//$("#prof").html((Math.random()*9999).toFixed(2));
			
			$.get("ajax/", manageReponseAjaxServeur); // envoi d'une requete AJAX
			
		} // fin refresh value
		"""
		+

		manageReponseAjaxServeur()
		+
		"""
		""")
		
	else:
		codeJS=(
		"""
		$(document).ready(function(){

			setInterval(function() { refreshValues()}, 500); // fixe délai actualisation

		}); // fin function + fin ready + fin $ 

		function refreshValues(){
			
			$.get("ajax/", manageReponseAjaxServeur); // envoi d'une requete AJAX
			
		} // fin refresh value
		"""
		+
		manageReponseAjaxServeur()
		+
		"""
		""")
	
	return codeJS

#--- fin du code Javascript / jQuery  ---

#========== fonction de gestion de la reponse du serveur aux requetes AJAX =========
def manageReponseAjaxServeur():
	manageReponseAjaxServeur=(
"""
//-- fonction de gestion de la réponse AJAX -- 


function manageReponseAjaxServeur(dataIn){

	var values=dataIn.split(','); // tableau de valeurs

	$("#temp").html(values[0]);
	$("#pressure").html(values[1]);
	$("#sog").html(values[2]);
	$("#lat").html(values[3]);
	$("#lon").html(values[4]);
	$("#cog").html(values[5]);
	$("#service").html(values[6]);
	$("#amp").html(values[7]);

	
} // fin fonction de gestion de la reponse AJAX 

""")
	
	return manageReponseAjaxServeur 

#===================== Envoi Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX

#def reponseAJAX(paramIn):
def reponseAJAX():
	
	global gpsd
	global last_received

	# la reponse
	try:
		sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
		pressure = (sensor.read_sealevel_pressure() / 100)
		gps = LatLon(gpsd.fix.latitude, gpsd.fix.longitude)
		degMin = gps.to_string('d% %m%')
		sec = gps.to_string('%S%')
		hemis = gps.to_string('%H')
		speed = gpsd.fix.speed
		cog = gpsd.fix.track
		
		latdegMin = degMin[0].strip("-(')")
		londegMin = degMin[1].strip("-(')")	
		latSec = '{0:0.3f}'.format(float(sec[0].strip("(')")))
		lonSec = '{0:0.3f}'.format(float(sec[1].strip("(')")))
		lathemis = hemis[0].strip("(')")
		lonhemis = hemis[1].strip("(')")
		
		reponseAjax=(
			str('{0:0.1f} °C'.format(sensor.read_temperature()))+","
			+str('{0:0.1f} hPa'.format(pressure))+","
			+str('{0} Kts'.format(speed))+","
			+str(latdegMin+" "+latSec+" "+lathemis)+","
			+str(londegMin+" "+lonSec+" "+lonhemis)+","
			+str('{0}°'.format(cog))+","
			+str('Service OK')+","
			+str('{0} Ah'.format(last_received))
		)  
		return reponseAjax
		
	except (ValueError, TypeError, IOError, UnboundLocalError):
		
		reponseAjax=(
			str('{0:0.1f} °C'.format(sensor.read_temperature()))+","
			+str('{0:0.1f} hPa'.format(pressure))+","
			+str("NOK,")
			+str("NOK,")
			+str("NOK,")
			+str("NOK,")
			+str('Service NON OK !! Vérifiez la connexion GPS ou du Baromètre')+","
			+str('{0} Ah'.format(last_received))
		)
		return reponseAjax
			

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
