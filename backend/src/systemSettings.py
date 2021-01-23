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
    
    '''
    def checkNewBtnDataAvaiable(self,input):
        inputSplit = input.split(",")
        if(inputSplit[0] == "enc"):
            if(inputSplit[1] == "posEdge"):
                self.__volume += 1
                self.__volume = np.clip(self.__volume, 0, 100)
                print("set system volume to: " + str(self.__volume))
            
            elif(inputSplit[1] == "negEdge"):
                self.__volume -= 1
                self.__volume = np.clip(self.__volume, 0, 100)
                print("set system volume to: " + str(self.__volume))

            elif(inputSplit[1] == "pressed"):
                if(self.__mute):
                    print("unmute system volume")
                else:
                    print("mute System volume")            
            
            else:
                print("unknown enc command from arduino")
        
    '''
    
    def getVolume(self):
        #print("get Volume: " + str(self.__volume))
        return self.__volume

    def setVolume(self,_input): 
        self.__volume = _input
        print("set Volume: " + str(self.__volume))

    def setMuteSystem(self):
        self.__mute = True
        print("Mute ON")

    def setUnmuteSystem(self):
        self.__mute = False
        print("Mute OFF")

    def getMuteState(self):
        #print("get mute State: " + str(self.__mute))
        return self.__mute

    def getDispBright(self):
        #print("get DisplayBrightness: " + str(self.__displayBrightness))
        return self.__displayBrightness

    def setDispBright(self,_input): 
        self.__displayBrightness = _input
        print("set DisplayBrightness: " + str(self.__displayBrightness))
        self.arduinoConnection.sendDisplayData(self.__displayBrightness)

    def setDispOn(self):
        self.__displayOff = False
        print("turn Display On")

    def setDispOff(self): 
        self.__displayOff = True
        print("turn Display Off")

    def getDispState(self):
        return self.__displayOff
        
