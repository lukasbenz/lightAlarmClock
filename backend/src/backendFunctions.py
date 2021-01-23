from internetRadio import InternetRadio
from alarmClock import AlarmClock
from systemSettings import SystemSettings
from light import Light
from serialArduino import ArduinoConnection

import json
import threading
import time
import os
dir = os.path.dirname(__file__)

class BackendFunctions():

       ######## init function ########
       def __init__(self):

              self.arduinoConnection = ArduinoConnection()

              self.alarmClock = AlarmClock()
              self.internetRadio = InternetRadio() 
              self.systemSettings = SystemSettings(self.arduinoConnection)
              self.light = Light(self.arduinoConnection)

       #config thread
              self.loadConfig()
              self.runConfigThread = True
              self.tConfig = threading.Thread(target=self.saveConfig)
              self.tConfig.start()


       #alarm thread
              self.runAlarmThread = True
              self.tAlarm = threading.Thread(target=self.handleAlarm)
              self.tAlarm.start()


       #chekButtons Thread
              self.runCheckButtonsThread = True
              self.tButtons = threading.Thread(target=self.checkButtons)
              self.tButtons.start()


       ######## config ########
       def loadConfig(self):
              print("work dir: " + dir)
              print("load config:")
              with open(dir + '/config.json') as json_file:
                     data = json.load(json_file)

              self.alarmClock.setWakeUpTime(data["wakeUpTime"])
              self.alarmClock.setSunsetTime(data["sunsetTime"])
              self.alarmClock.setAlarmState(data["alarmState"])
              self.internetRadio.setRadioStation(data["radioStation"])
              self.systemSettings.setVolume(data["volume"])
              self.systemSettings.setDisplayBrightness(data["displayBrightness"])
              self.light.setBrightness(data["lightBrightness"]),
              self.light.setLedStripeState(data["useLedStripe"])

       def saveConfig(self):
              self.tConfig = threading.currentThread()
              while self.runConfigThread:
                     jsonData = {
                            "wakeUpTime": self.alarmClock.getWakeUpTime(),
                            "sunsetTime": self.alarmClock.getSunsetTime(),
                            "alarmState": self.alarmClock.getAlarmState(),
                            "radioStation": self.internetRadio.getRadioStation(),
                            "volume": self.systemSettings.getVolume(),
                            "displayBrightness": self.systemSettings.getDisplayBrightness(),
                            "lightBrightness": self.light.getBrightness(),    
                            "useLedStripe": self.light.getLedStripeState()  
                     }

                     with open('config.json', 'w') as outfile:
                            json.dump(jsonData, outfile)
                     #print("save JsonFile to disk")
                     time.sleep(5)


       ######## handle Alarm ########
       def handleAlarm(self):
              self.tAlarm = threading.currentThread()
              while self.runAlarmThread:
                     #start Sunset
                     if(self.alarmClock.getSunsetActive() == True):
                            self.light.setSunsetTime(self.alarmClock.getSunsetTime())
                            self.alarmClock.setSunsetActive(False)
                            self.light.startSunset()

                     #start Radio on Alarm
                     if(self.alarmClock.getAlarmActive() == True):
                            self.internetRadio.play()
                            self.light.turnLightOn()
                            time.sleep(2)
                            self.alarmClock.setAlarmActive(False)

                     time.sleep(1)


       def checkButtons(self):
              self.tButtons = threading.currentThread()
              while self.runAlarmThread:
                     if(self.arduinoConnection.hasNewData()):
                            self.light.checkNewBtnDataAvaiable(self.arduinoConnection.getRecData())

                            self.systemSettings.checkNewBtnDataAvaiable(self.arduinoConnection.getRecData())

                            self.arduinoConnection.resetRecData()

              #time.sleep(100)

#handle sleep Mode


       ###################### APLICATION PROGRAMMING INTERFACE ######################

       ######## ALARM CLOCK ########
       #TIME DATE
       def getTimeAndDate(self):
              return  {
                     'time': self.alarmClock.getTime(),
                     'date': self.alarmClock.getDate()
              }

       #WAKE UP TIME
       def getWakeUpTime(self):
              return  {
                     'wakeUpTime': self.alarmClock.getWakeUpTime()
              }

       def setWakeUpTime(self,data):
              self.alarmClock.setWakeUpTime(data['wakeUpTime'])
              return self.getWakeUpTime()


       #SUNSET TIME
       def getSunsetTime(self):
              return  {
                     'sunsetTime': self.alarmClock.getSunsetTime()
              }

       def setSunsetTime(self,data):
              self.alarmClock.setSunsetTime(data['sunsetTime'])
              return self.getSunsetTime()
  
       #ALARM ACTIVE
       def getAlarmActive(self):
              return  {
                     'state': self.alarmClock.getAlarmActive()
              }

       def setAlarmActive(self,data):
              self.alarmClock.setAlarmActive(data['state'])
              return self.getAlarmActive()

       #ALARM STATE
       def getAlarmState(self):
              return  {
                     'state': self.alarmClock.getAlarmState()
              }

       def setAlarmState(self,data):
              self.alarmClock.setAlarmState(data['state'])
              return self.getAlarmState() 

       #Snooze Mode
       def getSnoozeState(self):
              return  {
                     'state': self.alarmClock.getSnoozeState()
              }

       def setSnoozeState(self,data):
              self.alarmClock.setSnoozeState(data['state'])
              return self.getSnoozeState() 


       ######## RADIO STATION ########
       def getRadioStation(self):
              return  {
                     'name': self.internetRadio.getRadioStationInfo()
              }

       def setNextRadioStation(self):
              self.internetRadio.setNextRadioStation()       
              return "True" 
       
       def setPrevRadioStation(self):
              self.internetRadio.setPrevRadioStation()
              return "True"

       def playRadio(self):
              self.internetRadio.play()
              return "play radio"

       def stopRadio(self):
              self.internetRadio.stop()
              return "stop radio"


       ######## System ########
       # Volume
       def getVolume(self):
              return  {
                     'value': self.systemSettings.getVolume()
              }

       def setVolume(self,data):
              self.systemSettings.setVolume(data['value'])
              return self.getVolume() 

       # Display
       def getDisplayBrightness(self):
              return  {
                     'value': self.systemSettings.getDisplayBrightness()
              }

       def setDisplayBrightness(self,data):
              self.systemSettings.setDisplayBrightness(data['value'])
              return self.getDisplayBrightness()

       def turnDispOn(self):
              self.systemSettings.turnDispOn()
              return "turn Display On"

       def turnDispOff(self):
              self.systemSettings.turnDispOff()
              return "turn Display Off"


       ######## LIGHT ########
       def getLightState(self):
              return  {
                     'state': self.light.getLightState()
              }

       def getLightBrightness(self):
              return  {
                     'value': self.light.getBrightness()
              }

       def setLightBrightness(self,data):
              self.light.setBrightness(data['value'])
              return self.getDisplayBrightness()

       def turnLightOn(self):
              self.light.turnLightOn()
              return "turn on light"

       def turnLightOff(self):
              self.light.turnLightOff()
              return "turn off light"

       def getLedStripeState(self):
              return  {
                     'state': self.light.getLedStripeState()
              }

       def turnLedStripeOn(self):
              self.light.turnLedStripeOn()
              return "turn on led Stripe"

       def turnLedStripeOff(self):
              self.light.turnLedStripeOff()
              return "turn off led Stripe"


       ######## close function ########
       def close(self):
              self.runConfigThread = False
              self.tConfig.join()

              self.runAlarmThread = False
              self.tAlarm.join()

              print("close API")