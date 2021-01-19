import flask
from flask import request, jsonify
from backendFunctions import BackendFunctions

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

backend = BackendFunctions()

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/alarmClock/dateTime', methods = ['GET'])
def apiTimeAndDate():
    if request.method == 'GET':
        return jsonify(backend.getTimeAndDate())


@app.route('/api/alarmClock/wakeUpTime', methods = ['GET','POST'])
def apiWakeUpTime():
    if request.method == 'GET':
       return jsonify(backend.getWakeUpTime())

    elif request.method == 'POST':
        return backend.setWakeUpTime(request.get_json())


@app.route('/api/alarmClock/sunsetTime', methods = ['GET','POST'])
def apiSunsetTime():
    if request.method == 'GET':
        return jsonify(backend.getSunsetTime())

    elif request.method == 'POST':
        return backend.setSunsetTime(request.get_json())


@app.route('/api/alarmClock/alarmActive', methods = ['GET','POST'])
def apiAlarmActive():
    if request.method == 'GET':
        return jsonify(backend.getAlarmActive())

    elif request.method == 'POST':
        return backend.setAlarmActive(request.get_json())


@app.route('/api/alarmClock/alarmState', methods = ['GET','POST'])
def apiAlarmState():
    if request.method == 'GET':
        return jsonify(backend.getAlarmState())

    elif request.method == 'POST':
        return backend.setAlarmState(request.get_json())


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


@app.route('/api/system/volume', methods = ['GET','POST'])
def apiSysVolume():
    if request.method == 'GET':
        return jsonify(backend.getVolume())

    elif request.method == 'POST':
        return backend.setVolume(request.get_json())


@app.route('/api/system/displayBrightness', methods = ['GET','POST'])
def apiSysDisplayBrightness():
    if request.method == 'GET':
        return jsonify(backend.getDisplayBrightness())

    elif request.method == 'POST':
        return backend.setDisplayBrightness(request.get_json())


@app.route('/api/system/displayOn', methods = ['GET','POST'])
def apiDispOn():
    if request.method == 'POST':
        return backend.turnDispOn()


@app.route('/api/system/displayOff', methods = ['GET','POST'])
def apiDispOff():
    if request.method == 'POST':
        return backend.turnDispOff()


@app.route('/api/light/state', methods = ['GET','POST'])
def apiLightState():
    if request.method == 'GET':
        return jsonify(backend.getLightState())


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


@app.route('/api/light/ledStripe/state', methods = ['GET','POST'])
def apiLedStripeState():
    if request.method == 'GET':
        return jsonify(backend.getLedStripeState())


@app.route('/api/light/ledStripe/on', methods = ['GET','POST'])
def apiLedStripeOn():
    if request.method == 'POST':
        return backend.turnLedStripeOn()

@app.route('/api/light/ledStripe/off', methods = ['GET','POST'])
def apiLedStripeOff():
    if request.method == 'POST':
        return backend.turnLedStripeOff()

# try:
app.run()
# except KeyboardInterrupt:
#     print('interrupted!')
#     BackendFunctions.close()
#     print("backend closed")