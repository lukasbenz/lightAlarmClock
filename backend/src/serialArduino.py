
import serial
import threading
import requests
import json
import numpy as np

url = 'http://127.0.0.1:5000/api/'

class ArduinoConnection():
    debugMode = False
    __runRecLoop = False
    s = None
    
    def __init__(self):        
        try:
            self.s = serial.Serial('/dev/ttyACM0', 9600)
            self.s.flushInput()
            print("init ArduinoConnection class")
            self.__startRecLoop()
        except:
            print("EXCEPTION ERROR init serial - no Arduino available")

    def __startRecLoop(self):
        print("start recLoop with arduino")
        self.__runRecLoop = True
        self.t = threading.Thread(target=self.__recLoop)
        self.t.start()

    def __recLoop(self):
        self.t = threading.currentThread()
        while(self.__runRecLoop):
            try:
                rawData = self.s.readline()
                rawData.strip()
                rawData =""
                if(self.debugMode):
                    #print("rawRecData:" + str(rawData))
                    pass

                inputSplit = rawData(",")

                if(inputSplit[0] == "enc"):
                        if(inputSplit[1] == "pressed"): #mute
                            if(self.__mute):
                                print("unmute")
                            else:
                                print("mute")            
                        
                        elif(inputSplit[1] == "posEdge"): #set volume
                            self.__volume += 1
                            self.__volume = np.clip(self.__volume, 0, 100)
                            print("set system volume to: " + str(self.__volume))
                        
                        elif(inputSplit[1] == "negEdge"): #set volume
                            self.__volume -= 1
                            self.__volume = np.clip(self.__volume, 0, 100)
                            print("set system volume to: " + str(self.__volume))

                        else:
                            print("unknown enc command from arduino")
                    
                # light ON/OFF    
                elif(inputSplit[0] == "mainBtn"):
                    if(self.__state == True):
                        #self.turnLightOff()
                        #self.__state = False
                        print("turn light off")
                    else:
                        #self.turnLightOn()
                        #self.__state = True
                        print("turn light on")
                
            except:
                print("EXCEPTION ERROR in recLoop")
    
    
    def writeData(self,string):
        try:
            print("writeData: " + str(string))
            self.s.write(string.encode("utf-8"))
        except:
            print("EXCEPTION ERROR write data")

    def close(self):
        self.__runRecLoop = False
        if self.t.joinable():
            self.t.join()
        print("close serial")
