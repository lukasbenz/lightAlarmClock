
from kivy.config import Config
Config.set('graphics', 'resizable', 'False')
Config.set('graphics', 'fullscreen','True')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics','show_cursor','0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.clock import Clock      

import requests
import json

url = 'http://127.0.0.1:5000/api/'

global timerWithoutTouchingDisplay

class ScreenHome(Screen):

        def __init__(self,**kwargs):
                super(ScreenHome, self).__init__(**kwargs)
                
        def enterPage(self,**kwargs):
                self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.1)

                #wakeup time
                response = requests.get(url+'alarmClock/time')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        wakeUpTimeTmp = json_data['value']
                        self.id_wakeUpTime.text = wakeUpTimeTmp[:-3]                          
                else:
                        self.id_wakeUpTime.text = 'err'
                        
                #alarm clock state
                response = requests.get(url+'alarmClock/state')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        self.id_switch_wakeUpTime.active = json_data['state']
                else:
                        print(response)

                                                
        def leavePage(self,**kwargs):
                self.eventUpdatePage.cancel()

        def updatePage(self, *args):
                try:
                        #time
                        response = requests.get(url+'time')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['value']
                        else:
                                self.id_clock.text = "err"

                        #date
                        response = requests.get(url+'date')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_date.text = json_data['value']
                        else:
                                self.id_date.text = "err"

                        
                        #light state
                        response = requests.get(url+'light/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_light.active = json_data['state']
                        else:
                                print(response)

                        #muted
                        response = requests.get(url+'system/volume/mute/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                if(json_data['state'] == True):
                                        self.id_muted.text = "MUTED"
                                else:
                                        self.id_muted.text = ""

                        else:
                                self.id_muted.text = "err"                        

                except:
                        print("exception updating page")

        def switchAlarmClockCallback(self, switchObject, switchValue):
                if(switchValue == True):
                        requests.post(url+'alarmClock/on') 
                else:
                        requests.post(url+'alarmClock/off') 
                        
        def switchLightCallback(self, switchObject, switchValue):   
                if(switchValue == True):
                        requests.post(url+'light/on') 
                else:
                        requests.post(url+'light/off') 

        def btnDisplayState(self, *args):
                requests.post(url+'system/display/off')
                self.parent.current = "screenDisplayOffID"

        def btnMenue1(self, *args):
                self.parent.current = "screenAlarmClockID"

        def btnMenue2(self, *args):
                self.parent.current = "screenRadioID"
        
        def btnMenue3(self, *args):
                self.parent.current = "screenSettingsID"

class ScreenDisplayOff(Screen):

        def __init__(self,**kwargs):
                super(ScreenDisplayOff, self).__init__(**kwargs)
                
        def enterPage(self,**kwargs):
                self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.1)
                

        def updatePage(self, *args):
                App.get_running_app().timerWithoutTouchingDisplay = 0

                response = requests.get(url+'system/display/state')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        if(json_data['state'] == True):
                                self.parent.current = "screenHomeID"
                else:
                        print(response)

        def leavePage(self,**kwargs):
                self.eventUpdatePage.cancel()

        def btnDisplayState(self, *args):
                requests.post(url+'system/display/on')

class ScreenAlarmClock(Screen):

                def __init__(self,**kwargs):
                        super(ScreenAlarmClock, self).__init__(**kwargs)
                        
                def enterPage(self,**kwargs):
                        self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.1)

                        response = requests.get(url+'alarmClock/alarmOnWeekend/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_weekend.active = json_data['state']
                        else:
                                print(response)

                def leavePage(self,**kwargs):
                        self.eventUpdatePage.cancel()

                def updatePage(self, *args):
                        #time
                        response = requests.get(url+'time')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['value']
                        else:
                                self.id_clock.text = "err"

                        #wakeup time
                        response = requests.get(url+'alarmClock/time')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                wakeUpTimeTmp = json_data['value'] 
                                self.hours = int(wakeUpTimeTmp[:2])
                                self.minutes = int(wakeUpTimeTmp[3:5])
                                self.convertWakeUpTime()
                                self.id_wakeUpTime.text = self.newWakeUpTime[:-3]                          
                        else:
                                self.id_wakeUpTime.text = 'err'
                        

                        #sunset time
                        response = requests.get(url+'alarmClock/sunsetTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.sunsetMinutes = int(json_data['value'])
                                self.displaySunsetTime()                           
                        else:
                                self.id_sunsetTime.text = 'err'
                        

                def convertWakeUpTime(self):
                        if(self.hours<10):
                                strHours = '0' + str(self.hours)
                        else:
                                strHours = str(self.hours)
                                
                        if(self.minutes<10):
                                strMinutes = '0' + str(self.minutes)
                        else:
                                strMinutes = str(self.minutes)

                        self.newWakeUpTime = strHours + ":" + strMinutes + ":00"
                
                def sendWakeUpTime(self):
                        data = {'value': self.newWakeUpTime}
                        r = requests.post(url+'alarmClock/time', json=data)           

                def displaySunsetTime(self):
                        if(self.sunsetMinutes<10):
                                strMinutes = '0' + str(self.sunsetMinutes)
                        else:
                              strMinutes = str(self.sunsetMinutes)
                
                        self.id_sunsetTime.text = strMinutes + " min"

                def btn_wakeUpHoursTimeUp(self, *args):
                        self.hours += 1

                        if(self.hours>23):
                                self.hours = 0

                        self.convertWakeUpTime()
                        self.sendWakeUpTime()
  
                def btn_wakeUpHoursTimeDown(self, *args):
                        self.hours -= 1

                        if(self.hours<0):
                                self.hours = 23                    
                        self.convertWakeUpTime()
                        self.sendWakeUpTime()

                def btn_wakeUpMinutesTimeUp(self, *args):
                        self.minutes += 1
                        if(self.minutes>59):
                                self.minutes = 0
                        self.convertWakeUpTime()
                        self.sendWakeUpTime()

                def btn_wakeUpMinutesTimeDown(self, *args):
                        self.minutes -= 1
                        if(self.minutes<0):
                                self.minutes = 59
                        self.convertWakeUpTime()
                        self.sendWakeUpTime()

                def btn_SunlightMinutesTimeUp(self, *args):
                        self.sunsetMinutes += 1
                        if(self.sunsetMinutes>60):
                                self.sunsetMinutes = 0
                        data = {'value': str(self.sunsetMinutes)}
                        r = requests.post(url+'alarmClock/sunsetTime', json=data)

                def btn_SunlightMinutesTimeDown(self, *args):
                        self.sunsetMinutes -= 1
                        if(self.sunsetMinutes<0):
                                self.sunsetMinutes = 60
                        data = {'value': str(self.sunsetMinutes)}
                        r = requests.post(url+'alarmClock/sunsetTime', json=data)
         

                def switchWeekendCallback(self, switchObject, switchValue):   
                        if(switchValue == True):
                                requests.post(url+'alarmClock/alarmOnWeekend/on') 
                        else:
                                requests.post(url+'alarmClock/alarmOnWeekend/off') 

                def btn_backHome(self, *args):
                        self.parent.current = "screenHomeID"

class ScreenRadio(Screen):

                def __init__(self,**kwargs):
                        super(ScreenRadio, self).__init__(**kwargs)
                        
                def enterPage(self, *args):
                        self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.1)
                        self.updateRadioInfo()

                def leavePage(self,**kwargs):
                        self.eventUpdatePage.cancel()

                def updatePage(self, *args):
                        #time
                        response = requests.get(url+'time')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['value']
                        else:
                                self.id_clock.text = "err"

                        
                        #Volume
                        response = requests.get(url+'system/volume')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_slider_volume.value = json_data['value']
                        else:
                                print(response)
                                self.id_wakeUpTime.text = 'err'

                        #muted
                        response = requests.get(url+'system/volume/mute/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                if(json_data['state'] == True):
                                        self.id_muted.text = "MUTED"
                                else:
                                        self.id_muted.text = ""
                        else:
                                self.id_muted.text = "err"
                        

                def updateRadioInfo(self,**kwargs):
                        response = requests.get(url+'radio/stationName')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_label_radio_info.text = json_data['value']
                                self.id_image.source = 'radioImages/' + json_data['value'] + '.png'                                
                        else:
                                print(response)
                                self.id_label_radio_info.text = 'err'

                def btn_back(self, *args):
                        requests.post(url+'radio/prevStation')  
                        self.updateRadioInfo()
                        print("btn_back")

                def btn_pause(self, *args):
                        requests.post(url+'radio/stop') 
                        self.updateRadioInfo()
                        print("btn_pause")

                def btn_play(self, *args):
                        requests.post(url+'radio/play') 
                        self.updateRadioInfo()
                        print("btn_play")

                def btn_next(self, *args):
                        requests.post(url+'radio/nextStation')  
                        self.updateRadioInfo()
                        print("btn_next")

                def btn_mute(self, *args):
                        response = requests.get(url+'system/volume/mute/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                if(json_data['state']): #if TRUE system ist muted - so unmute it
                                        requests.post(url+'system/volume/mute/off')
                                else: #if FALSE system is unmuted - so mute it
                                        requests.post(url+'system/volume/mute/on')

                def slider_volume_value(self, value):  
                        data = {'value': int(value)}
                        r = requests.post(url+'system/volume', json=data)           
                        
                def btn_backHome(self, *args):
                        self.parent.current = "screenHomeID"

class ScreenSettings(Screen):

                def __init__(self,**kwargs):
                        super(ScreenSettings, self).__init__(**kwargs)

                def enterPage(self, **kwargs):
                        self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.1)

                        response = requests.get(url+'system/display/brightness')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_slider_display.value = json_data['value']
                        else:
                                print(response)

                        response = requests.get(url+'light/brightness')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_slider_light.value = json_data['value']
                        else:
                                print(response)

                        response = requests.get(url+'light/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_light.active = json_data['state']
                        else:
                                print(response)


                        response = requests.get(url+'system/display/screensaver/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_screensaver.active = json_data['state']
                        else:
                                print(response)

                        response = requests.get(url+'light/ledStripe/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_ledStripe.active = json_data['state']
                        else:
                                print(response)
          
                def leavePage(self,**kwargs):
                        self.eventUpdatePage.cancel()

                def updatePage(self, *args):
                        # time
                        response = requests.get(url+'time')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['value']
                        else:
                                print(response)
                                self.id_clock.text = "err"

                        # light state
                        response = requests.get(url+'light/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_light.active = json_data['state']
                        else:
                                print(response)

                def slider_light_value(self, value):  
                        data = {'value': value}
                        r = requests.post(url+'light/brightness', json=data)           

                def slider_display_value(self, value):  
                        data = {'value': value}
                        r = requests.post(url+'system/display/brightness', json=data)           

                def switch_light_callback(self, switchObject, switchValue): 
                        if(switchValue == True):
                                pass
                                requests.post(url+'light/on') 
                        else:
                                pass
                                requests.post(url+'light/off')


                def switch_screensaver_callback(self, switchObject, switchValue): 
                        if(switchValue == True):
                                requests.post(url+'system/display/screensaver/on') 
                        else:
                                requests.post(url+'system/display/screensaver/off')


                def switch_ledStripe_callback(self, switchObject, switchValue): 
                        if(switchValue == True):
                                requests.post(url+'light/ledStripe/on') 
                        else:
                                requests.post(url+'light/ledStripe/off')


                def btn_backHome(self, *args):
                        self.parent.current = "screenHomeID"

'''
class ScreenAlarmActive(Screen):

        def __init__(self,**kwargs):
                super(ScreenAlarmActive, self).__init__(**kwargs)

        def enterPage(self,**kwargs):
                self.eventUpdatePage = Clock.schedule_interval(self.updatePage,0.5) 

        def leavePage(self,**kwargs):
                self.eventUpdatePage.cancel()

        def updatePage(self, *args):
                #time
                response = requests.get(url+'time')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        self.id_clock.text = json_data['value']
                else:
                        self.id_clock.text = "err"

                #date
                response = requests.get(url+'date')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        self.id_date.text = json_data['value']
                else:
                        self.id_date.text = "err"

        def btnSnooze(self, *args):
                requests.post(url+'alarmClock/snoozeMode/on')           
                #requests.post(url+'/alarmClock/active/off')
                self.parent.current = "screenHomeID"

        def btnStop(self, *args):
                #requests.post(url+'/alarmClock/active/off')
                self.parent.current = "screenHomeID"
'''

class VisuAlarmClock(App):   
        timerWithoutTouchingDisplay = 0

        def build(self):
                self.sm = ScreenManager(transition=NoTransition())
                self.home_screen = ScreenHome(name='screenHomeID')
                self.displayOff_screen = ScreenDisplayOff(name='screenDisplayOffID')
                self.alarmClock_screen = ScreenAlarmClock(name='screenAlarmClockID')
                self.radio_screen = ScreenRadio(name='screenRadioID')
                self.settings_screen = ScreenSettings(name='screenSettingsID')
                #self.alarmClockActive_screen = ScreenAlarmActive(name='screenAlarmActiveID')

                self.sm.add_widget(self.home_screen)
                self.sm.add_widget(self.displayOff_screen)
                self.sm.add_widget(self.alarmClock_screen)
                self.sm.add_widget(self.radio_screen)
                self.sm.add_widget(self.settings_screen)
                #self.sm.add_widget(self.alarmClockActive_screen)

                self.sm.current = 'screenHomeID'

                return self.sm
        
        def on_start(self):
                self.eventCheckAlarm = Clock.schedule_interval(self.checkScreenSaver,1)
                self.maxTimeWithputTouchingDisplay = 30 #60s
                
        def checkScreenSaver(self, *args):
                useScreensaver = False
                response = requests.get(url+'system/display/screensaver/state')
                json_data = json.loads(response.text)  
                
                if response.status_code == 200:
                        useScreensaver = json_data['state']
                else:
                        print(response)

                #print("useScreensaver: " + str(useScreensaver))
                #print("timerWithoutTouchingDisplay: " + str(self.timerWithoutTouchingDisplay))
                
                if(useScreensaver):
                        self.timerWithoutTouchingDisplay += 1
                        if(self.timerWithoutTouchingDisplay == self.maxTimeWithputTouchingDisplay):
                                requests.post(url+'system/display/off')
                                self.sm.current = "screenDisplayOffID"
                                print("turn screen off to safe energy")
                else:
                        self.timerWithoutTouchingDisplay = 0   


        def on_touch_down(self, touch):
                App.get_running_app().timerWithoutTouchingDisplay = 0
                #print("DEBUGGING TOUCH TOUCH TOUCH TOUCH TOUCH")

        Window.bind(on_touch_down=on_touch_down)

visu = VisuAlarmClock()
visu.run()
