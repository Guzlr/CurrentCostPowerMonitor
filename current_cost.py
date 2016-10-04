#! /usr/bin/python

import serial
import xml.etree.ElementTree as ET
import rrdtool as rrd
import time

#####################################################################
def generateGraphs():

   print "Generating Graphs"

   rrd.graph ('./power-15m.png', 
               '--title= Power Usage - 15 minutes',    
               '--start=end-15m',
               '--width=1024',    
               '--height=210',
               '--end=now',          
               '--vertical-label=Watts', 
               #'--lower-limit=0',          
               '--logarithmic',
               '--alt-autoscale-max',                  
               '--units=si',
               'DEF:Power=powertemp.rrd:Power:AVERAGE',
               'VDEF:PAve=Power,AVERAGE',
               'VDEF:PMax=Power,MAXIMUM',
               'VDEF:PMin=Power,MINIMUM',
               'LINE2:Power#0F00FF:Average',
               'GPRINT:PAve:%6.0lf',
               'LINE1:PMax#ff0000:Maximum',
               'GPRINT:PMax:%6.0lf',
               'LINE1:PMin#00ff00:Minimum',
               'GPRINT:PMin:%6.0lf')

   rrd.graph ('./power-15m.png',   
             '--title= Power Usage - 15 minutes',    
             '--start=end-15m',
             '--width=1024',    
             '--height=200',
             '--end=now',          
             '--vertical-label=Watts', 
             #'--lower-limit=0',          
             '--logarithmic',
             '--alt-autoscale-max',                  
             '--units=si',
             'DEF:Power=powertemp.rrd:Power:AVERAGE',
             'VDEF:PAve=Power,AVERAGE',
             'VDEF:PMax=Power,MAXIMUM',
             'VDEF:PMin=Power,MINIMUM',
             'LINE2:Power#0F00FF:Average',
             'GPRINT:PAve:%6.0lf',
             'LINE1:PMax#ff0000:Maximum',
             'GPRINT:PMax:%6.0lf',
             'LINE1:PMin#00ff00:Minimum',
             'GPRINT:PMin:%6.0lf')

   rrd.graph ('./power-1h.png',   
             '--title= Power Usage - 1 hour',    
             '--start=end-1h',      
             '--width=1024',    
             '--height=200',
             '--end=now',          
             '--vertical-label=Watts', 
             '--logarithmic',
             '--alt-autoscale-max',                  
             '--units=si',
             'DEF:Power=powertemp.rrd:Power:AVERAGE',
             'VDEF:PAve=Power,AVERAGE',
             'VDEF:PMax=Power,MAXIMUM',
             'VDEF:PMin=Power,MINIMUM',
             'LINE2:Power#0F00FF:Average',
             'GPRINT:PAve:%6.0lf',
             'LINE1:PMax#ff0000:Maximum',
             'GPRINT:PMax:%6.0lf',
             'LINE1:PMin#00ff00:Minimum',
             'GPRINT:PMin:%6.0lf')

   rrd.graph ('./power-24h.png',   
             '--title= Power Usage - 24 hours',    
             '--start=end-24h',      
             '--width=1024',    
             '--height=200',
             '--end=now',          
             '--vertical-label=Watts', 
             '--logarithmic',
             '--alt-autoscale-max',                  
             '--units=si',
             'DEF:Power=powertemp.rrd:Power:AVERAGE',
             'VDEF:PAve=Power,AVERAGE',
             'VDEF:PMax=Power,MAXIMUM',
             'VDEF:PMin=Power,MINIMUM',
             'LINE2:Power#0F00FF:Average',
             'GPRINT:PAve:%6.0lf',
             'LINE1:PMax#ff0000:Maximum',
             'GPRINT:PMax:%6.0lf',
             'LINE1:PMin#00ff00:Minimum',
             'GPRINT:PMin:%6.0lf')

   rrd.graph ('./power-7d.png',
             '--title= Power Usage - 7 days',
             '--start=end-7d',
             '--width=1024',
             '--height=200',
             '--end=now',
             '--vertical-label=Watts',
             '--logarithmic',
             '--alt-autoscale-max',
             '--units=si',
             'DEF:Power=powertemp.rrd:Power:AVERAGE',
             'VDEF:PAve=Power,AVERAGE',
             'VDEF:PMax=Power,MAXIMUM',
             'VDEF:PMin=Power,MINIMUM',
             'LINE2:Power#0F00FF:Average',
             'GPRINT:PAve:%6.0lf',
             'LINE1:PMax#ff0000:Maximum',
             'GPRINT:PMax:%6.0lf',
             'LINE1:PMin#00ff00:Minimum',
             'GPRINT:PMin:%6.0lf')

   rrd.graph ('./temperature-7d.png',
             '--title= Temperature - 7 days',
             '--start=end-7d',
             '--width=1024',
             '--height=200',
             '--end=now',
             '--vertical-label=Degrees C',
             '--alt-autoscale-max',
             '--lower-limit=0',
             '--units=si',
             'DEF:Temperature=powertemp.rrd:Temperature:AVERAGE',
             'VDEF:TAve=Temperature,AVERAGE',
             'VDEF:TMax=Temperature,MAXIMUM',
             'VDEF:TMin=Temperature,MINIMUM',
             'LINE2:Temperature#0F00FF:Average',
             'GPRINT:TAve:%6.0lf',
             'LINE1:TMax#ff0000:Maximum',
             'GPRINT:TMax:%6.0lf',
             'LINE1:TMin#00ff00:Minimum',
             'GPRINT:TMin:%6.0lf')


#########################################################################
ser = serial.Serial('/dev/ttyUSB0',57600,timeout=10)
ser.reset_input_buffer()

temperature = 0
power = 0
lastGraphGen = 0

while (True):
   record = ser.readline()
#   print (record)

   try:
      root = ET.fromstring(record)
   except:
      print "Error parsing record"
      continue

   for child in root:
      if child.tag == "tmpr":
         temperature = child.text
      if child.tag == "ch1":
         power = child[0].text

   print ('power = %s, temperature = %s' % (power, temperature))

   rrd.update('powertemp.rrd', 'N:%s:%s' % (power, temperature))

   if (time.time() - lastGraphGen) >= 59:
      lastGraphGen = time.time()
      generateGraphs()

ser.close()

# Format of XML string from meter:
# <msg>
#    <src>CC128-v0.11</src>
#    <dsb>02383</dsb>
#    <time>10:04:11</time>
#    <tmpr>23.4</tmpr>
#    <sensor>0</sensor>
#    <id>00740</id>
#    <type>1</type>
#    <ch1>
#       <watts>00968</watts>
#    </ch1>
# </msg>
