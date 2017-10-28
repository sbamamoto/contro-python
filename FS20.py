import copy
import array
import FhzUtils

class FS20:
    CRC_INDEX = 3
    MAINCODE_INDEX = 7
    DEVICECODE_INDEX = 9
    COMMANDCODE_INDEX = 10
    MAINCODE_LENGTH = 2
    DEVICECODE_LENGTH = 1
    PAYLOAD_START_INDEX = 4
    BUFFER_LENGTH = 11
    
    def __init__ (self, mainCode, deviceCode):
        self.mainCode = copy.copy(mainCode)
        self.deviceCode = copy.copy(deviceCode)
    
##    def __init__ (self,address):
##        self.mainCode = copy.copy(mainCode)
##        self.mainCode = self.mainCode[0:MAINCODE_LENGTH]
##        self.deviceCode = copy.copy(deviceCode)
##        self.deviceCode = self.deviceCode[MAINCODE_LENGTH:MAINCODE_LENGTH+DEVICECODE_LENGTH]
        
    def createFS20Command (self, commandByte):
        buffer = array.array('B',[0x81,0x09,0x04,0x00,0x02,0x01,0x01,0x00,0x00,0x00,0x00]) 
##        fhz = FhzUtils.FhzUtils()
        for i in range(self.MAINCODE_LENGTH):
            buffer[self.MAINCODE_INDEX+i]=self.mainCode[i];
        buffer[self.DEVICECODE_INDEX] = self.deviceCode[0]
        buffer[self.COMMANDCODE_INDEX] = commandByte
        buffer[self.CRC_INDEX] = self.crc8(buffer, self.PAYLOAD_START_INDEX, self.BUFFER_LENGTH)
        
       
        return buffer

    def crc8 (self,data, start, end):
        result = 0
        for i in range(start,end):
            result = result + data[i]
        return 0x000000ff&result   

    def off (self) :
        return self.createFS20Command(0x00)

    def on (self):
        return self.createFS20Command(0x11)
    
    def dimm (self, percent):
        return self.createFS20Command(percent/10)
    
    def sendState (self):
         return self.createFS20Command(0x17)
        
    def dimmUp (self):
        return self.createFS20Command(0x13)
    
    def dimmDown (self):
        return self.createFS20Command(0x14)
    
    def toggle (self):
        return self.createFS20Command(0x15)