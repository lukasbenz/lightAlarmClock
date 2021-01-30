import numpy as np

class SystemSettings():

    # init Values
    __volume = 0
    __mute = False

    __displayBrightness = 10
    __displayOff = False
    
    def __init__(self,arduinoConnection):
        self.arduinoConnection = arduinoConnection
        print("init system settings class")

    #VOLUME
    def getVolume(self):
        #print("get Volume: " + str(self.__volume))
        return self.__volume

    def setVolume(self,_input): 
        self.__volume = int(_input)
        print("set Volume: " + str(self.__volume))

    def muteOn(self):
        self.__mute = True
        print("Mute System ON")

    def muteOff(self):
        self.__mute = False
        print("Mute System OFF")

    def getMuteState(self):
        #print("get mute State: " + str(self.__mute))
        return self.__mute

    #DISPLAY
    def getDispBright(self):
        #print("get DisplayBrightness: " + str(self.__displayBrightness))
        return self.__displayBrightness

    def setDispBright(self,_input): 
        self.__displayBrightness = int(_input)
        self.arduinoConnection.writeData("<display," + str(self.__displayBrightness) + ">")

    def setDispOn(self):
        self.__displayOff = False
        self.arduinoConnection.writeData("<display," + str(self.__displayBrightness) + ">")
        print("turn Display On")

    def setDispOff(self): 
        self.__displayOff = True
        self.arduinoConnection.writeData("<display,0>")
        print("turn Display Off")

    def getDispState(self):
        return self.__displayOff