# contro-python
Python implementation to switch and dimm FS20 and 433MHz wireless power switches and dimmers.

# FS20
Switching a device on Linux:

```python
import FhzUtils
import FS20
import array
import time

# initialize com port
fhz = FhzUtils.FhzUtils('/dev/ttyUSB0')

# identify target address first six digits are teh house code last six digits are the device code.
address = fhz.calculateByteAddress('233244141115')

# get the binary address
mainCode = array.array('B', [0x00,0x00])
deviceCode = array.array('B', [0x00])
mainCode[0] = address[0]
mainCode[1] = address[1]
deviceCode[0] = address[2]

# booting up the fhz base 
fhz.bootUpSystem()
# sleep one second to let the fhz time to boot up
time.sleep(1)

# create fs20 controller for the target
fs20 = FS20.FS20(mainCode, deviceCode)

# powering off the addressed device
fhz.sendCommand(fs20.off())

# no more commands we can shut the fhz down
fhz.shutdown()
```
