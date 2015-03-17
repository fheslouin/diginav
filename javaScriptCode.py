#!/usr/bin/python
# -*- coding: iso-8859-15 -

jsIncDisplay="""<script type="text/javascript" src="static/jquery-1.11.1.min.js"></script>"""

jsIncMain="""
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
	$("#amp").html(values[6]);

	
} // fin fonction de gestion de la reponse AJAX 

""")
	
	return manageReponseAjaxServeur 

jsCodePressure=("""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500); // fixe delai actualisation
		
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
                url: 'data/dataPressure.txt'
            };
            
			var dataAdapter = new $.jqx.dataAdapter(source,
			{
				async: false,
				autoBind: true,
			});
            // prepare jqxChart settings
            var settings = {
                title: "Air presure and temperature",
                description: 'data erased everyday at 13pm',
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
						description: 'deg C',
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

jsCodeAmp=(
		"""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500);

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
                title: "Amp consumption",
                description: "data are erased everyday at 13pm",
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
				   unitInterval: 5,
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
					type: 'spline',
					valueAxis: {
						minValue: 0,
						maxValue: 25,
						displayValueAxis: true,
						unitInterval: 5,
						description: 'Ah',
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
		
jsCodeDisplay=(
		"""
		$(document).ready(function(){
		
			setInterval(function() { refreshValues()}, 500); 

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
		
jsCodeMain=(
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
