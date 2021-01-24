
#import os
#os.add_dll_directory(r'C:\Program Files\VLC Plus Player')

import vlc

class InternetRadio():
    isPlaying = False
    instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    player=instance.media_player_new()
    stationIndex = 1

    stationName = ""
    switchRadioStations = {
            1: "DASDING",
            2: "YOU FM",
            3: "RADIO BOB",
            4: "ENERGY",
            5: "ANTENNE 1"}

    urlDict = {
        "DASDING": "https://swr-edge-2035-fra-lg-cdn.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3",
        "YOU FM": "http://www.youfmradio.gr:8880/stream?type=.mp3",
        "RADIO BOB": "http://streams.radiobob.de/bob-live/mp3-192/mediaplayer",
        "ENERGY": "http://cdn.nrjaudio.fm/adwz1/de/33005/aac_64.mp3",
        "ANTENNE 1": "https://stream.antenne1.de/a1stg/livestream2.mp3"
    }

    def __init__(self):
        print("init internet radio")
    
    def getRadioStation(self):
        #print("get radio station: " + self.stationName)
        return self.stationIndex

    def getRadioStationInfo(self):
        #print("get radio station: " + self.stationName)
        return self.stationName

    def setRadioStation(self,_input):
        self.stationIndex = _input
        self.__changeRadioStation()
        print("set radio station: " + self.stationName)

    def setNextRadioStation(self):
        self.stationIndex+=1
        if(self.stationIndex > len(self.switchRadioStations)):
            self.stationIndex = 1
           
        print("set radio station: " + str(self.stationIndex) + ": " + self.stationName)
        self.__changeRadioStation() 
        
    def setPrevRadioStation(self):
        self.stationIndex-=1
        if(self.stationIndex == 0):
            self.stationIndex = len(self.switchRadioStations)

        print("set radio station: " + str(self.stationIndex) + ": " + self.stationName)
        self.__changeRadioStation()

    def getRadioState(self):
        return self.isPlaying

    def play(self):
        if(self.isPlaying == False):
            self.isPlaying = True
            self.player.play()
            print("play internet radio")
        else:
            print("internet radio is already playing")

    def stop(self):
        if(self.isPlaying == True):
            self.isPlaying = False
            self.player.stop()
            print("stop internet radio")
        else:
            print("internet radio is already stopped")

    def __changeRadioStation(self):
        pass