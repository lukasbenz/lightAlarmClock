import flask
from flask import request, jsonify

import json
import threading
import time
import os

from internetRadio import InternetRadio
from alarmClock import AlarmClock
from systemSettings import SystemSettings
from light import Light
from serialArduino import ArduinoConnection

#no logging output from FLASK [202] etc...
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

arduinoConnection = ArduinoConnection()
alarmClock = AlarmClock()
internetRadio = InternetRadio()
systemSettings = SystemSettings(arduinoConnection)
light = Light(arduinoConnection)


################## config ##################
def loadConfig(self):
    dir = os.path.dirname(__file__)
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


################## start save config Thread ##################
loadConfig()
runConfigThread = True
tConfig = threading.Thread(target=saveConfig)
tConfig.start()

################## start alarm handle thread ##################
runAlarmThread = True
tAlarm = threading.Thread(target=handleAlarm)
tAlarm.start()


############################################ APLICATION PROGRAMMING INTERFACE ############################################

################## ALARM CLOCK ##################
@app.route('/api/alarmClock/dateTime', methods = ['GET'])
def timeAndDate():
    if request.method == 'GET':
        return jsonify({
                'time': alarmClock.getTime(),
                'date': alarmClock.getDate()
            })
            
@app.route('/api/alarmClock/wakeUpTime', methods = ['GET','POST'])
def wakeUpTime():
    if request.method == 'GET':
        return jsonify({
            'value': alarmClock.getWakeUpTime()
            })        
    elif request.method == 'POST':
        alarmClock.setWakeUpTime(request.get_json(['value']))
        return jsonify({
                     'value': alarmClock.getWakeUpTime()
            })

@app.route('/api/alarmClock/sunsetTime', methods = ['GET','POST'])
def sunsetTime():
    if request.method == 'GET':
        return jsonify({
            'value': alarmClock.getSunsetTime()
            })
    elif request.method == 'POST':
        alarmClock.setSunsetTime(request.get_json(['value']))
        return jsonify({
            'value': alarmClock.getSunsetTime()
            })

@app.route('/api/alarmClock/on', methods = ['GET','POST'])
def alarmOn():
    if request.method == 'POST':
        alarmClock.setAlarmOn()
        return jsonify({
            'state': alarmClock.getAlarmState()
            })

@app.route('/api/alarmClock/off', methods = ['GET','POST'])
def alarmOff():
    if request.method == 'POST':
        alarmClock.setAlarmOff()
        return jsonify({
            'state': alarmClock.getAlarmState()
            })
    
@app.route('/api/alarmClock/state', methods = ['GET','POST'])
def alarmState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getAlarmState()
            })

@app.route('/api/alarmClock/snoozeMode/on', methods = ['GET','POST'])
def SnoozeModeOn():
    if request.method == 'POST':
        alarmClock.setSnoozeModeOn()
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })

@app.route('/api/alarmClock/snoozeMode/off', methods = ['GET','POST'])
def SnoozeModeOff():
    if request.method == 'POST':
        alarmClock.setSnoozeModeOff()
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })
    
@app.route('/api/alarmClock/snoozeMode/state', methods = ['GET','POST'])
def SnoozeModeState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })
          
@app.route('/api/alarmClock/snoozeMode/time', methods = ['GET','POST'])
def SnoozeTime():
    if request.method == 'GET':
        return jsonify({
            'value': alarmClock.setSnoozeTime()
            })        
    elif request.method == 'POST':
        alarmClock.setWakeUpTime(request.get_json(['value']))
        return jsonify({
                     'value': alarmClock.getSnoozeTime()
            })

@app.route('/api/alarmClock/active/off', methods = ['GET','POST'])
def alarmActiveOff():
    if request.method == 'POST':
        alarmClock.setAlarmActiveOff()
        return jsonify({
            'state': alarmClock.getAlarmActive()
            })
    
@app.route('/api/alarmClock/active/state', methods = ['GET','POST'])
def alarmActiveState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getAlarmActive()
            })


################## RADIO STATION ##################
@app.route('/api/radio/stationName', methods = ['GET','POST'])
def radioStationName():
    if request.method == 'GET':
        return jsonify({
            'state': internetRadio.getRadioStationInfo()
            })

@app.route('/api/radio/nextStation', methods = ['GET','POST'])
def nextRadioStation():
    if request.method == 'POST':
        internetRadio.setNextRadioStation()
        return jsonify({
            'state': internetRadio.getRadioStationInfo()
            })

@app.route('/api/radio/prevStation', methods = ['GET','POST'])
def prevRadioStation():
    if request.method == 'POST':
        internetRadio.setNextRadioStation()
        return jsonify({
            'state': internetRadio.getRadioStationInfo()
            })

@app.route('/api/radio/play', methods = ['GET','POST'])
def playRadio():
    if request.method == 'POST':
        internetRadio.play()
        return jsonify({
            'state': internetRadio.getRadioState()
            })

@app.route('/api/radio/stop', methods = ['GET','POST'])
def stopRadio():
    if request.method == 'POST':
        internetRadio.stop()
        return jsonify({
            'state': internetRadio.getRadioState()
            })

@app.route('/api/radio/state', methods = ['GET','POST'])
def radioState():
    if request.method == 'GET':
        return jsonify({
            'state': internetRadio.getRadioState()
            })


################## LIGHT ##################
@app.route('/api/light/brightness', methods = ['GET','POST'])
def lightBrightness():
    if request.method == 'GET':
            return jsonify({
            'value': light.getBrightness()
            })
    elif request.method == 'POST':
        light.setBrightness(request.get_json(['value']))
        return jsonify({
            'value': light.getBrightness()
            })

@app.route('/api/light/on', methods = ['GET','POST'])
def setLightOn():
    if request.method == 'POST':
        return light.turnLightOn()

@app.route('/api/light/off', methods = ['GET','POST'])
def setLightOff():
    if request.method == 'POST':
        return light.turnLightOff()

@app.route('/api/light/state', methods = ['GET','POST'])
def getLightState():
    if request.method == 'GET':
        return jsonify(light.getLightState())

@app.route('/api/light/ledStripe/on', methods = ['GET','POST'])
def setLedStripeOn():
    if request.method == 'POST':
        return light.turnLedStripeOn()

@app.route('/api/light/ledStripe/off', methods = ['GET','POST'])
def setLedStripeOff():
    if request.method == 'POST':
        return light.turnLedStripeOff()

@app.route('/api/light/ledStripe/state', methods = ['GET','POST'])
def getLedStripeState():
    if request.method == 'GET':
        return jsonify(light.getLedStripeState())


################## VOLUME ##################
@app.route('/api/system/volume', methods = ['GET','POST'])
def sysVolume():
    if request.method == 'GET':
            return jsonify({
            'value': systemSettings.getVolume()
            })
    elif request.method == 'POST':
        systemSettings.getVolume(request.get_json(['value']))
        return jsonify({
            'value': systemSettings.getVolume()
            })

@app.route('/api/system/volume/mute/on', methods = ['GET','POST'])
def setSysMute():
    if request.method == 'POST':
        systemSettings.mute()
        return jsonify({
            'value': systemSettings.getMuteState()
            })

@app.route('/api/system/volume/mute/off', methods = ['GET','POST'])
def setSysUnmute():
    if request.method == 'POST':
        systemSettings.unmute()
        return jsonify({
            'value': systemSettings.getMuteState()
            })

@app.route('/api/system/volume/mute/state', methods = ['GET','POST'])
def getSysMuteState():
    if request.method == 'GET':
        return jsonify({
            'value': systemSettings.getMuteState()
            })


################## DISPLAY ##################
@app.route('/api/system/display/brightness', methods = ['GET','POST'])
def dispBrightness():
    if request.method == 'GET':
            return jsonify({
            'value': systemSettings.getDispBright()
            })
    elif request.method == 'POST':
        systemSettings.setDispBright(request.get_json(['value']))
        return jsonify({
            'value': systemSettings.getDispBright()
            })

@app.route('/api/system/display/on', methods = ['GET','POST'])
def setDispOn():
    if request.method == 'POST':
        systemSettings.setDispOn()
        return jsonify({
            'value': systemSettings.getDispState()
            })

@app.route('/api/system/display/off', methods = ['GET','POST'])
def setDispOff():
    if request.method == 'POST':
        systemSettings.setDispOff()
        return jsonify({
            'value': systemSettings.getDispState()
            })

@app.route('/api/system/display/state', methods = ['GET'])
def getDispState():
    if request.method == 'GET':
            return jsonify({
            'value': systemSettings.getDispState()
            })









# try:
app.run()
# except KeyboardInterrupt:
#     print('interrupted!')
#     BackendFunctions.close()
#     print("backend closed")