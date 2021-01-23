import serial
import threading

url = 'http://127.0.0.1:5000/api/'

class ArduinoConnection():
    debugMode = False
    __runRecLoop = False
    __newDataReceived = False
    __receivedData = ""

    def __init__(self):        
        self.s = serial.Serial('/dev/ttyACM0', 9600)
        self.s.flushInput()
        print("init ArduinoConnection class")
        self.startRecLoop()

    def startRecLoop(self):
        print("start recLoop with arduino")
        self.__runRecLoop = True
        self.t = threading.Thread(target=self.recLoop)
        self.t.start()


    def sendLedData(self,r,g,b,startLed,endLed):
        self.__writeData("<led," + str(r) + "," + str(g) + "," + str(b) + "," + str(startLed) + "," + str(endLed) + ">")


    def sendDisplayData(self,brightness):
        self.__writeData("<display," + str(brightness) + ">")


#    def setVolume(self):
#        data = {'value': int(value)}
#        r = requests.post(url+'system/volume', json=data)           
#        print("RESPONSE")
#        print(r)

#    def setDiplayData


#    def setMuteSystem():


    def hasNewData(self):
        return self.__newDataReceived

    def getRecData(self):
        return self.__receivedData

    def resetRecData(self):
        print("resetRecData")
        self.__newDataReceived = False

    def recLoop(self):
        self.t = threading.currentThread()
        while(self.__runRecLoop):
            rawData = self.s.readline()
            rawData.strip()
            if(self.debugMode):
                print("rawRecData:" + str(rawData))

            self.__receivedData = rawData.decode("utf-8")






            self.__newDataReceived = True
            

    def __writeData(self,string):
        print("writeData: " + str(string))
        self.s.write(string.encode("utf-8"))


    def close(self):
        self.__runRecLoop = False
        if self.t.joinable():
            self.t.join()
        print("close serial")


#light = Light()
#light.startRecLoop()

#light.writeData('<led,100,0,100,0,27>')
#light.writeData('<display,0>')