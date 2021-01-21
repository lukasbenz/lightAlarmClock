import serial
import threading

class Light():
    debugMode = True
    __runRecLoop = False

    def __init__(self):        
        self.s = serial.Serial('/dev/ttyACM0', 9600)
        self.s.flushInput()
        print("init Serial")

    def startRecLoop(self):
        self.__runRecLoop = True
        print("start recLoop with arduino")
        self.t = threading.Thread(target=self.recLoop)
        self.t.start()

    def recLoop(self):
        self.t = threading.currentThread()

        while(self.__runRecLoop):
            line = self.s.readline()
            line.strip()
            print (line.decode("utf-8"))

    def writeData(self,string):
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