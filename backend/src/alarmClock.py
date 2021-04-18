import time
from datetime import datetime, timedelta
from flask.helpers import stream_with_context
import pytz
import threading


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


class AlarmClock():
    debugMode = False
    # init private Values
    
    __wakeUpTime = "06:45:00"
    __sunsetTime = "15"
    __snoozeTime = 10
    __alarmOnWeekend = False
    __snoozeState = False
    __sunsetState = False
    __alarmClockState = False
    __alarmActiveState = False

    def __init__(self):
        print("init alarmClock and start loop")
        self.runAlarmClock = True
        self.t = threading.Thread(target=self.alarmClockLoop)
        self.t.start()

    def getTime(self):
        return self.currentTime[:5]

    def getDate(self):

        dayDate = self.currentDate[8:11]
        dayReadable = switchDays.get(int(self.currentDay), "errDay")
        
        monthDate = self.currentDate[5:7]
        monthReadable = switchMonths.get(int(monthDate),"errMonth")

        year = self.currentDate[:4]

        resultStr = dayReadable + ", " + dayDate + ". " + monthReadable + " " + year
        
        return resultStr

    def setWakeUpTime(self,_input): 
        self.__wakeUpTime = _input
        print("set wakeUpTime: " + self.__wakeUpTime)

    def getWakeUpTime(self):
        #print("get wakeUpTime: " + self.__wakeUpTime)
        return self.__wakeUpTime

    def setAlarmOnWeekendOn(self):
        self.__alarmOnWeekend = True
        print("set alarmOnWeekend: " + str(self.__alarmOnWeekend))

    def setAlarmOnWeekendOff(self):
        self.__alarmOnWeekend = False
        print("set alarmOnWeekend: " + str(self.__alarmOnWeekend))

    def getAlarmOnWeekend(self):
        #print("get alarmOnWeekend: " + str(self.__alarmOnWeekend))
        return self.__alarmOnWeekend

    def setSunsetTime(self,_input):
        self.__sunsetTime = _input
        print("set sunsetTime: " + self.__sunsetTime)
    
    def getSunsetTime(self):
        #print("get sunsetTime: " + str(self.__sunsetTime))
        return self.__sunsetTime

    def setSunsetOff(self):
        self.__sunsetState = False
        print("set SunsetState: " + str(self.__sunsetState))

    def getSunsetActive(self):
        #print("get SunsetState: " + str(self.alarmState))
        return self.__sunsetState

    def setAlarmOn(self):
        self.__alarmClockState = True
        print("set __alarmClockState: " + str(self.__alarmClockState))

    def setAlarmOff(self):
        self.__alarmClockState = False
        print("set __alarmClockState: " + str(self.__alarmClockState))

    def getAlarmState(self):
        #print("get alarmState: " + str(self.__alarmClockState))
        return self.__alarmClockState

    def setSnoozeModeOn(self):
        self.__snoozeState = True
        print("set __snoozeState: " + str(self.__snoozeState))

    def setSnoozeModeOff(self):
        self.__snoozeState = False
        print("set __snoozeState: " + str(self.__snoozeState))

    def getSnoozeTime(self):
        #print("get snoozeTime: " + str(self.snoozeTime))
        return str(self.__snoozeTime)

    def setSnoozeTime(self, _input):
        self.__snoozeTime = _input
        print("set snoozeTime: " + self.__snoozeTime)

    def getSnoozeState(self):
        #print("get snoozeState: " + str(self.snoozeState))
        return self.__snoozeState

    def setAlarmActiveOff(self):
        self.__alarmActiveState = False
        print("set alarmActive: " + str(self.__alarmActiveState))

    def getAlarmActiveState(self):
        #print("get alarmActive: " + str(self.__alarmActiveState))
        return self.__alarmActiveState

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
            time.sleep(1)

            if(self.__alarmClockState == False):
                print("alarm clock off")
                continue;

            #sunsetTimeDelta = 
            sunsetStartTime = datetime.strptime(self.__wakeUpTime,"%H:%M:%S") - timedelta(minutes=int(self.__sunsetTime))
            sunsetStartTimeStr = sunsetStartTime.strftime("%H:%M:%S")

            if(self.debugMode):
                print("") 
                print("current Time: " + self.currentTime)
                print("wakeup Time: " + self.__wakeUpTime)
                print("sunset Time: " + sunsetStartTimeStr)
                print("alarmClockState: " + str(self.__alarmClockState))
                print("")

            if(self.__alarmOnWeekend == False):
                dayReadable = switchDays.get(int(self.currentDay), "errDay")
                if(dayReadable == "Samstag" or dayReadable == "Sonntag"):
                    print("alarmClock is off for the weekend")
                    continue
                        
            if(sunsetStartTimeStr == self.currentTime):
                self.__sunsetState = True

            if(self.__wakeUpTime == self.currentTime):
                self.__alarmActiveState = True


        print("stop alarm clock loop")


