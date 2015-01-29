#!/usr/bin/python
# -*- coding: utf-8 -*-

# code Python obtenu avec l'IDE Pyduino - www.mon-club-elec.fr 

#from pyduino_pcduino import * # importe les fonctions Arduino pour Python

#import random
import Adafruit_BMP.BMP085 as BMP085
from LatLon import LatLon
from bottle import route, run, template, static_file # importe classes utile du module Bottle

#from gpsdThreading import GpsPoller

import os
from gps import *
from time import *
import time
import threading

gpsd = None #seting the global variable

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
			
gpsp = GpsPoller() # create the thread
gpsp.start() # start it up

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
	
@route('/graphique')
def bottleHtmlInitial():
	return pageInitialeHTMLJS("graphique")

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
	return static_file(filename, root='./static/') # utilisation chemin relatif
	# le rep /static doit exister dans rép app *.py--
	#return static_file(filename, root=currentdir()+'static/') # si utilisation chemin absolu
	
@route('/data/<filename:path>')
def send_static(filename):
	return static_file(filename, root='./data/') # utilisation chemin relatif

#--- setup ---
def setup():
	
	#print "dir="+os.getcwd()+"/"+'static/' # debug
	#print "dir="+currentdir()+'static/' # debug
	
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
		
		bodyHTML="""<!--<textarea rows="4" cols="50" id="textarea"></textarea><br>-->
		<table width="100%">
		<tr>
		<td align="center">SOG</td>
		<tr></tr>
		<td align="center"><h1 id="sog" style="font-size:40pt;">8888</h1></td>
		<tr></tr>
		<td align="center">COG</td>
		<tr></tr>
		<td align="center"><h1 id="cog" style="font-size:40pt;">8888</h1></td>
		</tr>
		<td align="center">Latitude</td>
		<tr></tr>
		<td align="center"><h2 id="lat" style="font-size:40pt;">8888</h2></td>
		</tr>
		<tr>
		<td align="center">Longitude</td>
		<tr></tr>
		<td align="center"><h2 id="lon" style="font-size:40pt;">8888</h2></td>
		</table>"""	
	elif affichage == "graphique":
		
		bodyHTML="""<p class="text-center">						
						<div class="alert alert-info">
							<h1>DigiNav Dashboard</h1>
						</div>
					</p>
						<br />
					<div align="center">	
						<div id="chartContainer" style="width:800px; height:300px;"></div>
					</div>"""
		
	else :
	
		bodyHTML="""<!--<textarea rows="4" cols="50" id="textarea"></textarea><br>-->
				<p class="text-center">
					<div class="alert alert-info">
						<h1>DigiNav Dashboard</h1>
					</div>
				</p>

				<div class="container-fluid">
				<div class="row">
					<div class="col-xs-6 col-sm-4">
						<div class="panel panel-primary">
							<div class="panel-heading">
								<h3 class="panel-title">Latidude / Longitude</h3>
							</div>

							<div class="panel-body">
								<h2 id="lat">8888</h2>

								<h2 id="lon">8888</h2>
							</div>
						</div>
					</div>

					<div class="col-xs-6 col-sm-4">
						<div class="panel panel-primary">
							<div class="panel-heading">
								<h3 class="panel-title">Direction</h3>
							</div>

							<div class="panel-body">
								<h2 id="cog">8888</h2>
								<h2 id="sog">8888</h2>
							</div>
						</div>
					</div>
					<!-- Optional: clear the XS cols if their content doesn't match in height -->

					<div class="clearfix visible-xs-block"></div>

					<div class="col-xs-6 col-sm-4">
						<div class="panel panel-primary">
							<div class="panel-heading">
								<h3 class="panel-title">Préssion / Température</h3>
							</div>

							<div class="panel-body">
								<h2 id="pressure">8888</h2>
								<h2 id="temp">8888</h2>
								<p><a href="/graphique">Afficher le graphique</p></a>
							</div>
						</div>
					</div>
				</div>
				
			</div>		
        """
	
	return bodyHTML
	
	
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
		
			$('#myModal').on('shown.bs.modal', function () {
				$('#myInput').focus()
			})

			// prepare the data
			var source =
            {
                datatype: "csv",
                datafields: [
                    { name: 'Date' },
                    { name: 'Temp' },
                    { name: 'Pressure' }
                    ],
                url: 'data/dataOpenNav.txt'
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
						minValue: 920,
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
            $('#chartContainer').jqxChart(settings);
           
       		
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
	
	return codeJS

#--- fin du code Javascript / jQuery  ---

#========== fonction de gestion de la reponse du serveur aux requetes AJAX =========
def manageReponseAjaxServeur():
	manageReponseAjaxServeur=(
"""
//-- fonction de gestion de la réponse AJAX -- 


function manageReponseAjaxServeur(dataIn){
	
	//dataIn=parseInt(dataIn); 
	//$("#textarea").append("ajax : "+ dataIn+"\\n"); 
	//$("#textarea").get(0).setSelectionRange($("#textarea").get(0).selectionEnd-1,$("#textarea").get(0).selectionEnd-1); // se place en derniere ligne -1 pour avant saut de ligne 

	var values=dataIn.split(','); // tableau de valeurs

	$("#temp").html(values[0]);
	$("#pressure").html(values[1]);
	$("#sog").html(values[2]);
	$("#lat").html(values[3]);
	$("#lon").html(values[4]);
	$("#cog").html(values[5]);
	$("#service").html(values[6]);
	
	//var timestamp = new Date();
	//timestamp.setSeconds(timestamp.getSeconds());
	//timestamp.setMilliseconds(0);
	//data.push({ Date: timestamp, value: values[1] });
	//$('#chartContainer').jqxChart('update');


	
} // fin fonction de gestion de la reponse AJAX 

""")
	
	return manageReponseAjaxServeur 

#===================== Envoi Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX

#def reponseAJAX(paramIn):
def reponseAJAX():
	sensor = BMP085.BMP085()
	sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
	
	global gpsd

	# la reponse
	try:
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
			+str('{0} hPa'.format(sensor.read_pressure()/100))+","
			+str('{0} Kts'.format(speed))+","
			+str(latdegMin+" "+latSec+" "+lathemis)+","
			+str(londegMin+" "+lonSec+" "+lonhemis)+","
			+str('{0}°'.format(cog))+","
			+str('Service OK')
		)  
		return reponseAjax
		
	except (ValueError, TypeError):
		
		print "Problème de communicaton avec le GPS\nVérifier la connectique ou le service GPSD \"service gpsd restart\""
		
		reponseAjax=(
			str('{0:0.1f} °C'.format(sensor.read_temperature()))+","
			+str('{0} hPa'.format(sensor.read_pressure()/100))+","
			+str("NOK")+","
			+str("NOK")+","
			+str("NOK")+","
			+str("NOK")+","
			+str('Service NON OK !! Vérifiez la connexion au GPS')
		)  
		return reponseAjax
			

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
