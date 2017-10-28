#!/usr/bin/python

import os
import os.path
import sys
import cgi
import cgitb;
from subprocess import call
cgitb.enable()
import FhzUtils
import FS20
import array
import time


print "content-type: text/html\n"
print "<pre>Running test program"
fhz = FhzUtils.FhzUtils('/dev/ttyUSB0')
#address = fhz.calculateByteAddress('233244141119')
address = fhz.calculateByteAddress('233244141115')

mainCode = array.array('B', [0x00,0x00])
deviceCode = array.array('B', [0x00])

mainCode[0] = address[0]
mainCode[1] = address[1]
deviceCode[0] = address[2]

form = cgi.FieldStorage()
if form.has_key("Helligkeit"):
    print "****",form["Helligkeit"]
    brightness = int (form["Helligkeit"].value)
else:
    brightness =0

if form.has_key("device"):
    print "****",form["device"]
    address = fhz.calculateByteAddress(form["device"].value)
else:
    address = fhz.calculateByteAddress('233244141115')

#address = fhz.calculateByteAddress('233244141119')
#address = fhz.calculateByteAddress('233244141115')

mainCode = array.array('B', [0x00,0x00])
deviceCode = array.array('B', [0x00])

mainCode[0] = address[0]
mainCode[1] = address[1]
deviceCode[0] = address[2]

print "codes ..."
print "%x : %x @ %x"%(mainCode[0], mainCode[1], deviceCode[0])

fhz.bootUpSystem()
time.sleep(1)

fs20 = FS20.FS20(mainCode, deviceCode)

#fhz.sendCommand(fs20.off())
#time.sleep(10)
print "powered off"
fhz.sendCommand(fs20.dimm(brightness))

#while True:
#    try:
#        fhz.recvData(True)
#    except:
#        pass #evil !

print "<A href='/home/index.html'>xxxxxxxxxxxxxxxxx</a>"
fhz.shutdown()
