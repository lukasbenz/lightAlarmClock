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


       ################## config ##################
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
              self.systemSettings.setDispBright(data["displayBrightness"])
              self.light.setBrightness(data["lightBrightness"]),
              
              if(data["useLedStripe"]):
                     self.light.turnLedStripeOn()
              else:
                     self.light.turnLedStripeOff()

       def saveConfig(self):
              self.tConfig = threading.currentThread()
              while self.runConfigThread:
                     jsonData = {
                            "wakeUpTime": self.alarmClock.getWakeUpTime(),
                            "sunsetTime": self.alarmClock.getSunsetTime(),
                            "alarmState": self.alarmClock.getAlarmState(),
                            "radioStation": self.internetRadio.getRadioStation(),
                            "volume": self.systemSettings.getVolume(),
                            "displayBrightness": self.systemSettings.getDispBright(),
                            "lightBrightness": self.light.getBrightness(),    
                            "useLedStripe": self.light.getLedStripeState()  
                     }

                     with open('config.json', 'w') as outfile:
                            json.dump(jsonData, outfile)
                     #print("save JsonFile to disk")
                     time.sleep(5)


       ################## handle Alarm ##################
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

       #ALARM ACTIVE
       def getAlarmActive(self):
              return  {
                     'state': self.alarmClock.getAlarmActiveState()
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


       ################## RADIO STATION ##################
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


       ################## VOLUME ##################
       def getVolume(self):
              return  {
                     'value': self.systemSettings.getVolume()
              }

       def setVolume(self,data):
              self.systemSettings.setVolume(data['value'])
              return self.getVolume() 

       def setMuteSystem(self):
              self.systemSettings.setMuteSystem()
              return "mute system ON"

       def setUnmuteSystem(self):
              self.systemSettings.setUnmuteSystem()
              return "mute system OFF"

       def getMuteSystemState(self):
              return  {
                     'value': self.systemSettings.getMuteState()
              }

       ################## DISPLAY ##################
       def getDispBright(self):
              return  {
                     'value': self.systemSettings.getDispBright()
              }

       def setDispBright(self,data):
              self.systemSettings.setDispBright(data['value'])
              return self.getDispBright()

       def turnDispOn(self):
              self.systemSettings.turnDispOn()
              return "turn Display On"

       def turnDispOff(self):
              self.systemSettings.turnDispOff()
              return "turn Display Off"

       def getDispState(self):
              return  {
                     'value': self.systemSettings.getDispState()
              }
              

       ################## LIGHT ##################
       def turnLightOn(self):
              self.light.turnLightOn()
              return "turn on light"

       def turnLightOff(self):
              self.light.turnLightOff()
              return "turn off light"

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
              return self.getLightBrightness()

       def turnLedStripeOn(self):
              self.light.turnLedStripeOn()
              return "turn on led Stripe"

       def turnLedStripeOff(self):
              self.light.turnLedStripeOff()
              return "turn off led Stripe"

       def getLedStripeState(self):
              return  {
                     'state': self.light.getLedStripeState()
              }


       ################## close function ##################
       def close(self):
              self.runConfigThread = False
              self.tConfig.join()

              self.runAlarmThread = False
              self.tAlarm.join()

              print("close API")