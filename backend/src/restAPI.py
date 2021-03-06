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

arduinoConnection = ArduinoConnection()
alarmClock = AlarmClock()
internetRadio = InternetRadio()
systemSettings = SystemSettings(arduinoConnection)
light = Light(arduinoConnection)

################## config ##################
def loadConfig():
    #dir = os.path.dirname(__file__)
    #print("work dir: " + str(dir))
    #print("load config:")

    dir = os.path.dirname(__file__)
    with open(dir + 'config.json') as json_file:
        data = json.load(json_file)

        alarmClock.setWakeUpTime(data["wakeUpTime"])
        alarmClock.setSunsetTime(data["sunsetTime"])

        if(data["alarmOnWeekend"]):
            alarmClock.setAlarmOnWeekendOn()
        else:
            alarmClock.setAlarmOnWeekendOff()

        if(data["alarmState"]):
            alarmClock.setAlarmOn()
        else:
            alarmClock.setAlarmOff()

        internetRadio.setRadioStation(data["radioStation"])
        systemSettings.setVolume(data["volume"])
        systemSettings.setDispBright(data["displayBrightness"])
        light.setBrightness(data["lightBrightness"]),

        if(data["useLedStripe"]):
            light.turnLedStripeOn()
        else:
            light.turnLedStripeOff()

        if(data["screensaver"]):
            systemSettings.setDispScreensaverOn()
        else:
            systemSettings.setDispScreensaverOff()

def saveConfig(): #save all 10s current state - if you turn the power on/off
    tConfig = threading.currentThread()
    while runConfigThread:
        jsonData = {
        "wakeUpTime": alarmClock.getWakeUpTime(),
        "alarmOnWeekend": alarmClock.getAlarmOnWeekend(),
        "sunsetTime": alarmClock.getSunsetTime(),
        "alarmState": alarmClock.getAlarmState(),
        "radioStation": internetRadio.getRadioStationName(),
        "volume": systemSettings.getVolume(),
        "displayBrightness": systemSettings.getDispBright(),
        "lightBrightness": light.getBrightness(),
        "useLedStripe": light.getLedStripeState(),
        "screensaver": systemSettings.getDispScreensaverState()
        }

        dir = os.path.dirname(__file__)
        with open(dir + 'config.json', 'w') as outfile:
            json.dump(jsonData, outfile)
        
        time.sleep(60)

################## handle Alarm ##################
def handleAlarm():
    #TODO TRY CATCH EXCEPTIONS
    tAlarm = threading.currentThread()
    while runAlarmThread:
        #start Sunset
        if(alarmClock.getSunsetActive() == True):        
            light.setSunsetTime(alarmClock.getSunsetTime())
            light.startSunset()
            alarmClock.setSunsetOff()

        #start Radio on Alarm
        if(alarmClock.getAlarmActiveState() == True):
            systemSettings.setDispOn()
            internetRadio.play()
            time.sleep(2)
            alarmClock.setAlarmActiveOff()

        time.sleep(1)

############################################ APLICATION PROGRAMMING INTERFACE ############################################

################## SYSTEM TIME / DATE ##################
@app.route('/api/time', methods = ['GET'])
def getTime():
    if request.method == 'GET':
        return jsonify({
                'value': alarmClock.getTime()
            })

@app.route('/api/date', methods = ['GET'])
def getDate():
    if request.method == 'GET':
        return jsonify({
                'value': alarmClock.getDate()
            })


################## ALARM CLOCK ##################
@app.route('/api/alarmClock/time', methods = ['GET','POST'])
def wakeUpTime():
    if request.method == 'GET':
        return jsonify({
            'value': alarmClock.getWakeUpTime()
            })
    elif request.method == 'POST':
        alarmClock.setWakeUpTime(request.get_json()['value'])
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
        alarmClock.setSunsetTime(request.get_json()['value'])
        return jsonify({
            'value': alarmClock.getSunsetTime()
            })

@app.route('/api/alarmClock/on', methods = ['POST'])
def alarmOn():
    if request.method == 'POST':
        alarmClock.setAlarmOn()
        return jsonify({
            'state': alarmClock.getAlarmState()
            })

@app.route('/api/alarmClock/off', methods = ['POST'])
def alarmOff():
    if request.method == 'POST':
        alarmClock.setAlarmOff()
        return jsonify({
            'state': alarmClock.getAlarmState()
            })

@app.route('/api/alarmClock/state', methods = ['GET'])
def alarmState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getAlarmState()
            })

@app.route('/api/alarmClock/alarmOnWeekend/on', methods = ['POST'])
def alarmOnWeekendOn():
    if request.method == 'POST':
        alarmClock.setAlarmOnWeekendOn()
        return jsonify({
            'state': alarmClock.getAlarmOnWeekend()
            })

@app.route('/api/alarmClock/alarmOnWeekend/off', methods = ['POST'])
def alarmOnWeekendOff():
    if request.method == 'POST':
        alarmClock.setAlarmOnWeekendOff()
        return jsonify({
            'state': alarmClock.getAlarmOnWeekend()
            })


@app.route('/api/alarmClock/alarmOnWeekend/state', methods = ['GET'])
def alarmOnWeekendState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getAlarmOnWeekend()
            })

@app.route('/api/alarmClock/snoozeMode/on', methods = ['POST'])
def snoozeModeOn():
    if request.method == 'POST':
        alarmClock.setSnoozeModeOn()
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })

@app.route('/api/alarmClock/snoozeMode/off', methods = ['POST'])
def snoozeModeOff():
    if request.method == 'POST':
        alarmClock.setSnoozeModeOff()
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })

@app.route('/api/alarmClock/snoozeMode/state', methods = ['GET'])
def SnoozeModeState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getSnoozeState()
            })

@app.route('/api/alarmClock/snoozeMode/time', methods = ['GET','POST'])
def SnoozeTime():
    if request.method == 'GET':
        return jsonify({
            'value': alarmClock.getSnoozeTime()
            })
    elif request.method == 'POST':
        alarmClock.setSnoozeTime(request.get_json(['value']))
        return jsonify({
                     'value': alarmClock.getSnoozeTime()
            })

@app.route('/api/alarmClock/active/off', methods = ['POST'])
def alarmActiveOff():
    if request.method == 'POST':
        alarmClock.setAlarmActiveOff()
        return jsonify({
            'state': alarmClock.getAlarmActiveState()
            })

@app.route('/api/alarmClock/active/state', methods = ['POST'])
def alarmActiveState():
    if request.method == 'GET':
        return jsonify({
            'state': alarmClock.getAlarmActiveState()
            })


################## RADIO STATION ##################
@app.route('/api/radio/stationName', methods = ['GET'])
def radioStationName():
    if request.method == 'GET':
        return jsonify({
            'value': internetRadio.getRadioStationName()
            })

@app.route('/api/radio/nextStation', methods = ['POST'])
def nextRadioStation():
    if request.method == 'POST':
        internetRadio.setNextRadioStation()
        return jsonify({
            'value': internetRadio.getRadioStationName()
            })

@app.route('/api/radio/prevStation', methods = ['POST'])
def prevRadioStation():
    if request.method == 'POST':
        internetRadio.setNextRadioStation()
        return jsonify({
            'value': internetRadio.getRadioStationName()
            })

@app.route('/api/radio/play', methods = ['POST'])
def playRadio():
    if request.method == 'POST':
        internetRadio.play()
        return jsonify({
            'state': internetRadio.getRadioState()
            })

@app.route('/api/radio/stop', methods = ['POST'])
def stopRadio():
    if request.method == 'POST':
        internetRadio.stop()
        return jsonify({
            'state': internetRadio.getRadioState()
            })

@app.route('/api/radio/state', methods = ['GET'])
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
        light.setBrightness(request.get_json()['value'])
        return jsonify({
            'value': light.getBrightness()
            })

@app.route('/api/light/on', methods = ['POST'])
def setLightOn():
    if request.method == 'POST':
        light.turnLightOn()
        return jsonify({
            'state': light.getLightState()
            })

@app.route('/api/light/off', methods = ['POST'])
def setLightOff():
    if request.method == 'POST':
        light.turnLightOff()
        return jsonify({
            'state': light.getLightState()
            })

@app.route('/api/light/state', methods = ['GET'])
def getLightState():
    if request.method == 'GET':
        return jsonify({
            'state': light.getLightState()
            })

@app.route('/api/light/ledStripe/on', methods = ['POST'])
def setLedStripeOn():
    if request.method == 'POST':
        light.turnLedStripeOn()
        return jsonify({
            'state': light.getLedStripeState()
            })

@app.route('/api/light/ledStripe/off', methods = ['POST'])
def setLedStripeOff():
    if request.method == 'POST':
        light.turnLedStripeOff()
        return jsonify({
            'state': light.getLedStripeState()
            })

@app.route('/api/light/ledStripe/state', methods = ['GET'])
def getLedStripeState():
    if request.method == 'GET':
        return jsonify({
            'state': light.getLedStripeState()
            })

################## VOLUME ##################
@app.route('/api/system/volume', methods = ['GET','POST'])
def sysVolume():
    if request.method == 'GET':
            return jsonify({
            'value': systemSettings.getVolume()
            })
    elif request.method == 'POST':
        systemSettings.setVolume(request.get_json()['value'])
        return jsonify({
            'value': systemSettings.getVolume()
            })

@app.route('/api/system/volume/mute/on', methods = ['POST'])
def setSysMute():
    if request.method == 'POST':
        systemSettings.muteOn()
        return jsonify({
            'state': systemSettings.getMuteState()
            })

@app.route('/api/system/volume/mute/off', methods = ['POST'])
def setSysUnmute():
    if request.method == 'POST':
        systemSettings.muteOff()
        return jsonify({
            'state': systemSettings.getMuteState()
            })

@app.route('/api/system/volume/mute/state', methods = ['GET'])
def getSysMuteState():
    if request.method == 'GET':
        return jsonify({
            'state': systemSettings.getMuteState()
            })

################## DISPLAY ##################
@app.route('/api/system/display/brightness', methods = ['GET','POST'])
def dispBrightness():
    if request.method == 'GET':
            return jsonify({
            'value': systemSettings.getDispBright()
            })
    elif request.method == 'POST':
        systemSettings.setDispBright(request.get_json()['value'])
        return jsonify({
            'value': systemSettings.getDispBright()
            })

@app.route('/api/system/display/on', methods = ['POST'])
def setDispOn():
    if request.method == 'POST':
        systemSettings.setDispOn()
        return jsonify({
            'value': systemSettings.getDispState()
            })

@app.route('/api/system/display/off', methods = ['POST'])
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
            'state': systemSettings.getDispState()
            })

@app.route('/api/system/display/screensaver/on', methods = ['POST'])
def setDispScreensaverOn():
    if request.method == 'POST':
        systemSettings.setDispScreensaverOn()
        return jsonify({
            'value': systemSettings.getDispScreensaverState()
            })

@app.route('/api/system/display/screensaver/off', methods = ['POST'])
def setDispScreensaverOff():
    if request.method == 'POST':
        systemSettings.setDispScreensaverOff()
        return jsonify({
            'value': systemSettings.getDispScreensaverState()
            })

@app.route('/api/system/display/screensaver/state', methods = ['GET'])
def getDispScreensaverState():
    if request.method == 'GET':
            return jsonify({
            'state': systemSettings.getDispScreensaverState()
            })

################## start save config Thread ##################
loadConfig()
runConfigThread = True
tConfig = threading.Thread(target=saveConfig, name="saveConfigThread")
tConfig.start()

################## start alarm handle thread ##################
runAlarmThread = True
tAlarm = threading.Thread(target=handleAlarm, name="handleAlarmThread")
tAlarm.start()

time.sleep(1)

app.config["DEBUG"] = False
#app.run(host='192.168.2.112')
app.run()

