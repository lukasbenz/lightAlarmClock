import numpy as np

class SystemSettings():

    # init Values
    __volume = 0
    __displayBrightness = 10
    __displayState = True
    __mute = False

    def __init__(self,arduinoConnection):
        print("init system settings class")

    def checkNewBtnDataAvaiable(self,input):
        inputSplit = input.split(",")
        if(inputSplit[0] == "enc"):
            if(inputSplit[1] == "posEdge"):
                self.__volume += 1
                self.__volume = np.clip(self.__volume, 0, 100)
                print("set system volume to: " + self.__volume)
            
            elif(inputSplit[1] == "negEdge"):
                self.__volume -= 1
                self.__volume = np.clip(self.__volume, 0, 100)
                print("set system volume to: " + self.__volume)

            elif(inputSplit[1] == "pressed"):
                if(self.__mute):
                    print("unmute system volume")
                else:
                    print("mute System volume")            
            
            else:
                print("unknown enc command from arduino")
        

    def getVolume(self):
        #print("get Volume: " + str(self.__volume))
        return self.__volume

    def setVolume(self,_input): 
        self.__volume = _input
        print("set Volume: " + str(self.__volume))

    def getDisplayBrightness(self):
        #print("get DisplayBrightness: " + str(self.__displayBrightness))
        return self.__displayBrightness

    def setDisplayBrightness(self,_input): 
        self.__displayBrightness = _input
        print("set DisplayBrightness: " + str(self.__displayBrightness))

    def turnDispOn(self):
        self.__displayState = True
        print("turn Display On")

    def turnDispOff(self): 
        self.__displayState = False
        print("turn Display Off")


