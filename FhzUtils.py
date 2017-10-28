from array import array
import serial

class FhzUtils:
    
    def __init__(self, device):
        # SAY Hello Code:             81   06   c9   82   02   01   1f   60
        self.SAY_HELLO = array('B',[0x81,0x06,0xc9,0x82,0x02,0x01,0x1f,0x60])
        # Init HMS Code: 81	05	04	50	c9 01 86
        self.HMS_INIT = array('B', [0x81,0x05,0x04,0x50,0xc9,0x01,0x86])
        # Init FS20 Code: 81	05	04	60	c9 01 96
        self.FS20_INIT = array('B',[0x81,0x06,0x04,0x62,0xc9,0x96,0x60])
        #print "trying to open ",device,"..."
        self.comm = serial.Serial(device, baudrate=9600,\
                                  bytesize=serial.EIGHTBITS,\
                                  parity=serial.PARITY_NONE, \
                                  stopbits=serial.STOPBITS_ONE,\
                                  timeout=5, \
                                  xonxoff=0, \
                                  rtscts=0)

    def printHexDump(self, data, prefix=""):
        dump=""
        for b in data:
            dump = "%s %02x"%(dump, b)
        print prefix, dump

    def calculateByteAddress(self, address):
        byteAddress = array('B',[0x00,0x00,0x00])
        for b in range(3):
            i=3
            for z in range(4):
                f = round(pow(4,i))
                ziffer = (int(address[(z+b*4):(z+b*4)+1])-1)*f
                byteAddress[b]=byteAddress[b]+int(ziffer);
                i=i-1
        return byteAddress


    def sendCommand (self, data):
        dump=""
        self.sendData(data, True)

    def sendData (self, data, debug=False):
        if debug:
            self.printHexDump(data, "SENT -> ")
        self.comm.write(data.tostring())
        self.comm.flush()

    def recvData (self, debug=False):
        recvd = array('B')
        startByte=0

        while startByte != 0x81:
            startByte = ord(self.comm.read(1))

        recvd.append(startByte)
        lengthByte = ord(self.comm.read(1))
        recvd.append(lengthByte)
        
        for i in range(lengthByte):
            recvd.append(ord(self.comm.read(1)))
            
        if debug:
            self.printHexDump(recvd, "RCVD <- ")
        return recvd
    
    def bootUpSystem(self):
        self.sendData(self.SAY_HELLO,True)
        data = self.recvData(True)
        self.sendData(self.HMS_INIT, True)
        self.sendData(self.FS20_INIT, True  )

    def shutdown(self):
        self.comm.close()

