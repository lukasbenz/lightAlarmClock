import time
from datetime import datetime, timedelta
from flask.helpers import stream_with_context
import pytz
import threading


switchDaysJson = {
            0: "mon",
            1: "tue",
            2: "wed",
            3: "thu",
            4: "fri",
            5: "sat",
            6: "sun"
            }


switchDaysReadable = {
            0: "Montag",
            1: "Dienstag",
            2: "Mittwoch",
            3: "Donnerstag",
            4: "Freitag",
            5: "Samstag",
            6: "Sonntag"
            }

switchMonthsReadable = {
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
            12: "Dezember"
            }


class AlarmClock():
    debugMode = False
    wakeUpTime = "06:45:00"
    sunsetTime = "15"
    snoozeTime = 10

    # init private Values

    __alarmDayArray= {
    "mon": False,
    "tue": False,
    "wed": False,
    "thu": False,
    "fri": False,
    "sat": False,
    "sun": False
    }

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
        dayReadable = switchDaysReadable.get(int(self.currentDay), "errDay")
        
        monthDate = self.currentDate[5:7]
        monthReadable = switchMonthsReadable.get(int(monthDate),"errMonth")

        year = self.currentDate[:4]

        resultStr = dayReadable + ", " + dayDate + ". " + monthReadable + " " + year
        
        return resultStr

    def setWakeUpTime(self,_input): 
        self.wakeUpTime = _input
        print("set wakeUpTime: " + self.wakeUpTime)

    def getWakeUpTime(self):
        #print("get wakeUpTime: " + self.wakeUpTime)
        return self.wakeUpTime

    def setSunsetTime(self,_input):
        self.sunsetTime = _input
        print("set sunsetTime: " + self.sunsetTime)
    
    def getSunsetTime(self):
        #print("get sunsetTime: " + str(self.sunsetTime))
        return self.sunsetTime

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

    def setAlarmDayArray(self,_input):
        self.__alarmDayArray = _input
        print("set __alarmDayArray: " + str(self.__alarmDayArray))

    def getAlarmDayArray(self):
        print("get alarmDayArray: " + str(self.__alarmDayArray))
        return self.__alarmDayArray

    def getAlarmState(self):
        print("get alarmState: " + str(self.__alarmClockState))
        return self.__alarmClockState

    def setSnoozeModeOn(self):
        self.__snoozeState = True
        print("set __snoozeState: " + str(self.__snoozeState))

    def setSnoozeModeOff(self):
        self.__snoozeState = False
        print("set __snoozeState: " + str(self.__snoozeState))

    def getSnoozeTime(self):
        #print("get sunsetTime: " + str(self.sunsetTime))
        return str(self.snoozeTime)

    def setSnoozeTime(self, _input):
        self.snoozeTime = _input
        print("set snoozeTime: " + self.snoozeTime)

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

            #sunsetTimeDelta = 
            sunsetStartTime = datetime.strptime(self.wakeUpTime,"%H:%M:%S") - timedelta(minutes=int(self.sunsetTime))
            sunsetStartTimeStr = sunsetStartTime.strftime("%H:%M:%S")

            if(self.debugMode):
                print("") 
                print("current Day:" + self.currentDay)
                print("current Time: " + self.currentTime)
                print("wakeup Time: " + self.wakeUpTime)
                print("sunset Time: " + sunsetStartTimeStr)
                print("alarmClockState: " + str(self.__alarmClockState))
                print("")
            
            if(self.__alarmClockState == True):

                ### if(self.__alarmDayArray[SwitchDaysJson] == True):
                if(sunsetStartTimeStr == self.currentTime):
                    self.__sunsetState = True

                if(self.wakeUpTime == self.currentTime):
                    self.__alarmActiveState = True

            time.sleep(1)

        print("stop alarm clock loop")


