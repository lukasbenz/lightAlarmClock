
class SystemSettings():

    # init Values
    __volume = 0
    __displayBrightness = 10
    __displayState = True
    
    def __init__(self):
        pass

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


