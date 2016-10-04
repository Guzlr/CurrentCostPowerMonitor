# CurrentCostPowerMonitor
Tool to read the serial output of a Current Cost meter and generate a web page 
with various power and temperature graphs

The Current Cost CC128 power meter generates an XML output stream on its serial 
port. Every 7 seconds it generates XML containing various tags including current 
power usage and temerature. This tool parses the XML and injects the power and 
temperature readings in to a round-robin database (RRD). Each minute or so the 
tool will generate a set of graphs as PNG images, using the RRD graphing tool. 
These PNGs are included in a basic web page that auto-refreshes every 60 seconds.

This tool is basically a proof of concept and is a way for me to practice Python.

Limitations and things to think about:

- Ideally this tool will run as a daemon. 

- I run this tool on my Ubuntu machine as root/sudo to allow access to the serial 
  port - I'm sure this could be done in a safer way.

- The graph generation is a bit over-zealous in that the longer term graphs don't 
  need to be regenerated evey minute and the 15 minute graph could be refreshed 
  more frequently. I'm sure some AJAX or similar could make this more dynamic.

- The meter also outputs some history XML data periodically. The Python script 
  manages to ignore this output by parsing for the specific tags required.

- Sometimes the serial read results in an (apparently) empty string. This is 
  handled/ignored by a try/except block on the XML parse call. It would be 
  interesting to work out why these empty strings appear.
