import flask
from flask import request, jsonify

from backendFunctions import BackendFunctions

from internetRadio import InternetRadio
from alarmClock import AlarmClock
from systemSettings import SystemSettings
from light import Light
from serialArduino import ArduinoConnection

#no logging output from FLASK [202] etc...
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

backend = BackendFunctions()

app = flask.Flask(__name__)
app.config["DEBUG"] = True


alarmClock = AlarmClock()

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



@app.route('/api/alarmClock/snoozeMode', methods = ['GET','POST'])
def apiSnoozeMode():
    if request.method == 'GET':
        return jsonify(backend.getSnoozeState())

    elif request.method == 'POST':
        return backend.setSnoozeState(request.get_json())


# RADIO STATION
@app.route('/api/radio/stationName', methods = ['GET','POST'])
def apiRadioStationName():
    if request.method == 'GET':
        return jsonify(backend.getRadioStation())


@app.route('/api/radio/nextStation', methods = ['GET','POST'])
def apiNextRadioStation():
    if request.method == 'POST':
        return backend.setNextRadioStation()


@app.route('/api/radio/prevStation', methods = ['GET','POST'])
def apiPrevRadioStation():
    if request.method == 'POST':
        return backend.setPrevRadioStation()


@app.route('/api/radio/play', methods = ['GET','POST'])
def apiPlayRadio():
    if request.method == 'POST':
        return backend.playRadio()


@app.route('/api/radio/stop', methods = ['GET','POST'])
def apiStopRadio():
    if request.method == 'POST':
        return backend.stopRadio()

# VOLUME
@app.route('/api/system/volume', methods = ['GET','POST'])
def apiSysVolume():
    if request.method == 'GET':
        return jsonify(backend.getVolume())

    elif request.method == 'POST':
        return backend.setVolume(request.get_json())


@app.route('/api/system/volume/mute/on', methods = ['GET','POST'])
def apiSysMute():
    if request.method == 'POST':
        return backend.setMuteSystem()


@app.route('/api/system/volume/mute/off', methods = ['GET','POST'])
def apiSysUnmute():
    if request.method == 'POST':
        return backend.setUnmuteSystem()


@app.route('/api/system/volume/mute/state', methods = ['GET','POST'])
def apiSysMuteState():
    if request.method == 'GET':
        return jsonify(backend.getMuteSystemState())


# DISPLAY
@app.route('/api/system/display/brightness', methods = ['GET','POST'])
def apiSysDisplayBrightness():
    if request.method == 'GET':
        return jsonify(backend.getDispBright())

    elif request.method == 'POST':
        return backend.setDispBright(request.get_json())


@app.route('/api/system/display/on', methods = ['GET','POST'])
def apiDispOn():
    if request.method == 'POST':
        return backend.setDispOn()


@app.route('/api/system/display/off', methods = ['GET','POST'])
def apiDispOff():
    if request.method == 'POST':
        return backend.setDispOff()


@app.route('/api/system/display/state', methods = ['GET'])
def apiDispState():
    if request.method == 'GET':
        return backend.getDispState()


@app.route('/api/light/brightness', methods = ['GET','POST'])
def apiLightBrightness():
    if request.method == 'GET':
        return jsonify(backend.getLightBrightness())

    elif request.method == 'POST':
        return backend.setLightBrightness(request.get_json())



@app.route('/api/light/on', methods = ['GET','POST'])
def apiLightOn():
    if request.method == 'POST':
        return backend.turnLightOn()


@app.route('/api/light/off', methods = ['GET','POST'])
def apiLightOff():
    if request.method == 'POST':
        return backend.turnLightOff()


@app.route('/api/light/state', methods = ['GET','POST'])
def apiLightState():
    if request.method == 'GET':
        return jsonify(backend.getLightState())


@app.route('/api/light/ledStripe/on', methods = ['GET','POST'])
def apiLedStripeOn():
    if request.method == 'POST':
        return backend.turnLedStripeOn()


@app.route('/api/light/ledStripe/off', methods = ['GET','POST'])
def apiLedStripeOff():
    if request.method == 'POST':
        return backend.turnLedStripeOff()


@app.route('/api/light/ledStripe/state', methods = ['GET','POST'])
def apiLedStripeState():
    if request.method == 'GET':
        return jsonify(backend.getLedStripeState())


# try:
app.run()
# except KeyboardInterrupt:
#     print('interrupted!')
#     BackendFunctions.close()
#     print("backend closed")