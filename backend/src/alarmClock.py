import time
from datetime import datetime
from flask.helpers import stream_with_context
import pytz

import threading

class AlarmClock():

    # init Values
    wakeUpTime = "07:00:00"
    sunsetTime = 30
    snoozeTime = 10
    snoozeState = False
    alarmState = True
    sunsetActive = False
    alarmActive = False

    def __init__(self):
        print("init alarmClock and start loop")
        self.runAlarmClock = True
        self.t = threading.Thread(target=self.alarmClockLoop)
        self.t.start()

    def setWakeUpTime(self,_input): 
        self.wakeUpTime = _input
        print("set wakeUpTime: " + self.wakeUpTime)

    def getWakeUpTime(self):
        #print("get wakeUpTime: " + self.wakeUpTime)
        return self.wakeUpTime

    def setSunsetTime(self,_input):
        self.sunsetTime = _input
        print("set sunsetTime: " + str(self.sunsetTime))
    
    def getSunsetTime(self):
        #print("get sunsetTime: " + str(self.sunsetTime))
        return self.sunsetTime

    def setSunsetActive(self, _input):
        self.sunsetActive = bool(_input)
        print("set SunsetState: " + str(self.alarmState))

    def getSunsetActive(self):
        #print("get SunsetState: " + str(self.alarmState))
        return self.sunsetActive

    def setAlarmActive(self,_input):
        self.alarmActive = bool(_input)
        print("set alarmActive: " + str(self.alarmActive))

    def getAlarmActive(self):
        #print("get alarmActive: " + str(self.alarmActive))
        return self.alarmActive

    def setAlarmState(self, _input):
        self.alarmState = bool(_input)
        print("set alarmState: " + str(self.alarmState))

    def getAlarmState(self):
        #print("get alarmState: " + str(self.alarmState))
        return self.alarmState

    def getSnoozeTime(self):
        #print("get sunsetTime: " + str(self.sunsetTime))
        return self.snoozeTime

    def setSnoozeTime(self, _input):
        self.snoozeTime = _input
        print("set sunsetTime: " + str(self.sunsetTime))
            
    def getSnoozeState(self):
        #print("get snoozeState: " + str(self.snoozeState))
        return self.snoozeState

    def setSnoozeState(self, _input):
        self.snoozeState = bool(_input)
        print("set snoozeState: " + str(self.snoozeState))

    def getTime(self):
        return self.currentTime[:5]

    def getDate(self):

        switchDays = {
            0: "Montag",
            1: "Dienstag",
            2: "Mittwoch",
            3: "Donnerstag",
            4: "Freitag",
            5: "Samstag",
            6: "Sonntag"}

        switchMonths = {
            1: "Januar",
            2: "Februar",
            3: "März",
            4: "April",
            5: "Mai",
            6: "Juni",
            7: "Juli",
            8: "August",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Dezember"}

        dayDate = self.currentDate[8:11]
        dayReadable = switchDays.get(int(self.currentDay), "errDay")
        
        monthDate = self.currentDate[5:7]
        monthReadable = switchMonths.get(int(monthDate),"errMonth")

        year = self.currentDate[:4]

        resultStr = dayReadable + ", " + dayDate + ". " + monthReadable + " " + year
        return resultStr


    def procActTimeAndDate(self):
        timezone = pytz.timezone('Europe/Berlin')
        timezone_date_time_obj = timezone.localize(datetime.now())
        self.currentDate = timezone_date_time_obj.strftime("%Y-%m-%d")
        self.currentTime = timezone_date_time_obj.strftime("%H:%M:%S")
        self.currentDay = timezone_date_time_obj.weekday()

    
    def alarmClockLoop(self):
        self.t = threading.currentThread()
        
        while self.runAlarmClock:
            self.procActTimeAndDate()

            sunsetStartTime = datetime.strptime(self.wakeUpTime,"%H:%M:%S") - datetime.strptime(str(self.sunsetTime),"%M")
            #print("sunsetStart: " + str(sunsetStartTime))
            #print("curr Time: " + self.currentTime)

            if(self.alarmState == True):
                if(str(sunsetStartTime) == self.currentTime):
                    self.sunsetActive = True
                if(self.wakeUpTime == self.currentTime):
                    self.alarmActive = True

            time.sleep(1.0)

        print("stop alarm clock loop")


