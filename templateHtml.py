#!/usr/bin/python
# -*- coding: iso-8859-15 -

htmlMainPage="""<!--<textarea rows="4" cols="50" id="textarea"></textarea><br>-->
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
								<h3 class="panel-title">Direction & Speed</h3>
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
								<h3 class="panel-title">Pressure / Temperature</h3>
							</div>

							<div class="panel-body">
								<h2 id="pressure">8888</h2>
								<h2 id="temp">8888</h2>
								<p><a href="/graphPressure">Show graph</p></a>
							</div>
						</div>
					</div>
					
					<div class="col-xs-6 col-sm-4">
						<div class="panel panel-primary">
							<div class="panel-heading">
										<h3 class="panel-title">Amp consumption</h3>
							</div>

							<div class="panel-body">
								<h2 id="amp">8888</h2>
								<p><a href="/graphAmp">Show graph</p></a>
							</div>
						</div>
					</div>
				</div>
				
			</div>"""
			
htmlGraphAmp="""<p class="text-center">						
<div class="alert alert-info">
	<h1>DigiNav Dashboard</h1>
</div>
</p>
<br />
<div align="center">	
<div id="chartAmp" style="width:800px; height:300px;"></div>
</div>"""

htmlGraphPressure="""<p class="text-center">						
			<div class="alert alert-info">
				<h1>DigiNav Dashboard</h1>
			</div>
		</p>
			<br />
		<div align="center">	
			<div id="chartPressure" style="width:800px; height:300px;"></div>
		</div>"""
		
				
htmlAfficheur="""<!--<textarea rows="4" cols="50" id="textarea"></textarea><br>-->
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
