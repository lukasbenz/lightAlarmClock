import numpy as np
import alsaaudio

class SystemSettings():

    # init Values
    __volume = 0
    __mute = False

    __displayBrightness = 10
    __displayOff = False
    
    def __init__(self,arduinoConnection):
        self.arduinoConnection = arduinoConnection
        scanCards = alsaaudio.cards()
        print("cards:", scanCards)
        
        # i = 0
        # for card in scanCards:
            
        #     print("cardname: " + str(card))
        #     scanMixers = alsaaudio.mixers(scanCards.index(card))
        #     print("mixers:", scanMixers)
        #     for mixer in scanMixers:
        #         i+=1
        #         print("index: " + str(i))
        #         print("mixer: " + mixer)
        #         self.mixer = alsaaudio.mixers(scanCards.index(card))

        self.mixer = alsaaudio.Mixer('Digital', cardindex=0)
        #self.mixer.setvolume(20)
        
        print("init system settings class")

    #VOLUME
    def getVolume(self):
        #print("get Volume: " + str(self.__volume))
        return int(self.__volume)

    def setVolume(self,_input): 
        if(not self.__mute):
            #transform 0-100 to 0-80
            self.__volume = int(_input)
            self.__volume = np.clip(self.__volume, 0, 100)
            print("set Volume: " + str(self.__volume))
            self.mixer.setvolume(self.__volume)
        else:
            print("system muted!")

    def muteOn(self):
        self.__mute = True
        self.mixer.setvolume(0)
        print("system muted")
    
    def muteOff(self):
        self.__mute = False
        self.mixer.setvolume(self.__volume)
        print("system unmuted")

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