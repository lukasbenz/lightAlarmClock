
from kivy.config import Config
Config.set('graphics', 'resizable', 'False')
Config.set('graphics', 'fullscreen','False')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock      

import requests
import json

url = 'http://127.0.0.1:5000/api/'

class ScreenHome(Screen):

        def __init__(self,**kwargs):
                super(ScreenHome, self).__init__(**kwargs)
                
        def enterPage(self,**kwargs):
                
                self.eventUpdateClock = Clock.schedule_interval(self.updateClock,1)
                
                try:
                        response = requests.get(url+'alarmClock/wakeUpTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_wakeUpTime.text = json_data['wakeUpTime'][:-3]
                        else:
                                self.id_wakeUpTime.text = "err"
                                print(response)

                        response = requests.get(url+'alarmClock/alarmState')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_wakeUpTime.active = json_data['state']
                        else:
                                print(response)

                        response = requests.get(url+'light/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_light.active = json_data['state']
                        else:
                                print(response)
                except:
                        print("An exception occurred")

        def leavePage(self,**kwargs):
                self.eventUpdateClock.cancel()

        def updateClock(self, *args):
                try:
                        response = requests.get(url+'alarmClock/dateTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['time']
                                self.id_date.text = json_data['date']
                        else:
                                print(response)
                                self.id_clock.text = "err"
                                self.id_date.text = "err"
                except:
                        print("An exception occurred")

        def switch_wakeUpTime_callback(self, switchObject, switchValue):   
                data = {'state': switchValue}
                r = requests.post(url+'alarmClock/alarmState', json=data)           
                print("RESPONSE")
                print(r)

                if(switchValue == 0):
                        data = {'state': 0}
                        r = requests.post(url+'alarmClock/snoozeMode', json=data)           
                        print("RESPONSE")
                        print(r)


        def switch_light_callback(self, switchObject, switchValue):   
                if(switchValue == True):
                        requests.post(url+'light/on') 
                else:
                        requests.post(url+'light/off') 

        def btnDisplayState(self, *args):
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
                requests.post(url+'system/displayOff')           

        def leavePage(self,**kwargs):
                requests.post(url+'system/displayOn') 

        def btnDisplayState(self, *args):
                self.parent.current = "screenHomeID"

class ScreenAlarmClock(Screen):
                def __init__(self,**kwargs):
                        super(ScreenAlarmClock, self).__init__(**kwargs)

                def enterPage(self,**kwargs):
                        self.eventUpdateClock = Clock.schedule_interval(self.updateClock,1)

                        response = requests.get(url+'alarmClock/wakeUpTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                wakeUpTimeTmp = json_data['wakeUpTime'] 
                                print(wakeUpTimeTmp)
                                self.hours = int(wakeUpTimeTmp[:2])
                                self.minutes = int(wakeUpTimeTmp[3:5]) 
                                self.updateWakeUpTime()                            
                        else:
                                print(response)
                                self.id_wakeUpTime.text = 'err'

                        response = requests.get(url+'alarmClock/sunsetTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.sunsetMinutes = int(json_data['sunsetTime'])
                                self.updateSunsetTime()                            
                        else:
                                print(response)
                                self.id_sunsetTime.text = 'err'

                def leavePage(self,**kwargs):
                        self.eventUpdateClock.cancel()

                def updateClock(self, *args):
                        response = requests.get(url+'alarmClock/dateTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['time']
                        else:
                                print(response)
                                self.id_clock.text = "err"

                def updateWakeUpTime(self):
                        if(self.hours<10):
                                strHours = '0' + str(self.hours)
                        else:
                              strHours = str(self.hours)
                        
                        if(self.minutes<10):
                                strMinutes = '0' + str(self.minutes)
                        else:
                              strMinutes = str(self.minutes)
                             
                        newWakeUpTime = strHours + ":" + strMinutes + ":00"
                        self.id_wakeUpTime.text = newWakeUpTime[:-3]

                        data = {'wakeUpTime': newWakeUpTime}
                        r = requests.post(url+'alarmClock/wakeUpTime', json=data)           
                        print("RESPONSE")
                        print(r)
                                        
                def updateSunsetTime(self):

                        if(self.sunsetMinutes<10):
                                strMinutes = '0' + str(self.sunsetMinutes)
                        else:
                              strMinutes = str(self.sunsetMinutes)
                             
                        newSunsetTime = strMinutes
                        self.id_sunsetTime.text = newSunsetTime + " min"

                        data = {'sunsetTime': newSunsetTime*60} # convert to seconds
                        r = requests.post(url+'alarmClock/sunsetTime', json=data)           
                        print("RESPONSE")
                        print(r)

                def btn_wakeUpHoursTimeUp(self, *args):
                        self.hours += 1

                        if(self.hours>23):
                                self.hours = 0
                        self.updateWakeUpTime()
                               
                def btn_wakeUpHoursTimeDown(self, *args):
                        self.hours -= 1

                        if(self.hours<0):
                                self.hours = 23                    
                        self.updateWakeUpTime()

                def btn_wakeUpMinutesTimeUp(self, *args):
                        self.minutes += 1
                        if(self.minutes>59):
                                self.minutes = 0
                        self.updateWakeUpTime()

                def btn_wakeUpMinutesTimeDown(self, *args):
                        self.minutes -= 1
                        if(self.minutes<0):
                                self.minutes = 59
                        self.updateWakeUpTime()

                def btn_SunlightMinutesTimeUp(self, *args):
                        self.sunsetMinutes += 5
                        if(self.sunsetMinutes>60):
                                self.sunsetMinutes = 0
                        self.updateSunsetTime()

                def btn_SunlightMinutesTimeDown(self, *args):
                        self.sunsetMinutes -= 5
                        if(self.sunsetMinutes<0):
                                self.sunsetMinutes = 60
                        self.updateSunsetTime()
         
                def btn_backHome(self, *args):

                        self.parent.current = "screenHomeID"

class ScreenRadio(Screen):

                def __init__(self,**kwargs):
                        super(ScreenRadio, self).__init__(**kwargs)
                        
                def enterPage(self, *args):
                        self.eventUpdateClock = Clock.schedule_interval(self.updateClock,1)

                        self.updateRadioInfo()
                        response = requests.get(url+'system/volume')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_slider_volume.value = json_data['value']
                        else:
                                print(response)
                                self.id_wakeUpTime.text = 'err'

                def leavePage(self,**kwargs):
                        self.eventUpdateClock.cancel()

                def updateClock(self, *args):
                        response = requests.get(url+'alarmClock/dateTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['time']
                        else:
                                print(response)
                                self.id_clock.text = "err"

                def updateRadioInfo(self,**kwargs):
                        response = requests.get(url+'radio/stationName')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_label_radio_info.text = json_data['name']
                                self.id_image.source = 'radioImages/' + json_data['name'] + '.png'                                
                        else:
                                print(response)
                                self.id_wakeUpTime.text = 'err'

                        
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
                        self.id_slider_volume.value = 0
                        data = {'value': 0}
                        r = requests.post(url+'system/volume', json=data)           
                        print("RESPONSE")
                        print(r)  

                def slider_volume_value(self, value):  
                        data = {'value': int(value)}
                        r = requests.post(url+'system/volume', json=data)           
                        print("RESPONSE")
                        print(r)
                        
                def btn_backHome(self, *args):
                        self.parent.current = "screenHomeID"

class ScreenSettings(Screen):

                def __init__(self,**kwargs):
                        super(ScreenSettings, self).__init__(**kwargs)

                def enterPage(self, **kwargs):
                        self.eventUpdateClock = Clock.schedule_interval(self.updateClock,1)

                        response = requests.get(url+'system/displayBrightness')
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

                        response = requests.get(url+'light/ledStripe/state')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_switch_ledStripe.active = json_data['state']
                        else:
                                print(response)
          
                def leavePage(self,**kwargs):
                        self.eventUpdateClock.cancel()


                def updateClock(self, *args):
                        response = requests.get(url+'alarmClock/dateTime')
                        json_data = json.loads(response.text)  
                        if response.status_code == 200:
                                self.id_clock.text = json_data['time']
                        else:
                                print(response)
                                self.id_clock.text = "err"

                def slider_light_value(self, value):  
                        data = {'value': int(value)}
                        r = requests.post(url+'light/brightness', json=data)           
                        print("RESPONSE")
                        print(r)

                def slider_display_value(self, value):  
                        data = {'value': int(value)}
                        r = requests.post(url+'system/displayBrightness', json=data)           
                        print("RESPONSE")
                        print(r)

                def switch_ledStripe_callback(self, switchObject, switchValue): 
                        if(switchValue == True):
                                requests.post(url+'light/ledStripe/on') 
                        else:
                                requests.post(url+'light/ledStripe/off')

                def switch_light_callback(self, switchObject, switchValue): 
                        if(switchValue == True):
                                requests.post(url+'light/on') 
                        else:
                                requests.post(url+'light/off')

                def btn_backHome(self, *args):
                        self.parent.current = "screenHomeID"

class ScreenAlarmActive(Screen):

        def __init__(self,**kwargs):
                super(ScreenAlarmActive, self).__init__(**kwargs)

        def enterPage(self,**kwargs):
                self.eventUpdateClock = Clock.schedule_interval(self.updateClock,1) 

        def leavePage(self,**kwargs):
                self.eventUpdateClock.cancel()

        def updateClock(self, *args):
                response = requests.get(url+'alarmClock/dateTime')
                json_data = json.loads(response.text)  
                if response.status_code == 200:
                        self.id_clock.text = json_data['time']
                        self.id_date.text = json_data['date']
                else:
                        print(response)
                        self.id_clock.text = "err"
                        self.id_date.text = "err"

        def btnExtend(self, *args):
                data = {'state': 1}
                r = requests.post(url+'alarmClock/snoozeMode', json=data)           
                print("RESPONSE")
                print(r)

                self.parent.current = "screenHomeID"

        def btnStop(self, *args):
                self.parent.current = "screenHomeID"
 
 
class VisuAlarmClock(App):   

        def build(self):
                self.sm = ScreenManager(transition=FadeTransition())
                self.home_screen = ScreenHome(name='screenHomeID')
                self.displayOff_screen = ScreenDisplayOff(name='screenDisplayOffID')
                self.alarmClock_screen = ScreenAlarmClock(name='screenAlarmClockID')
                self.radio_screen = ScreenRadio(name='screenRadioID')
                self.settings_screen = ScreenSettings(name='screenSettingsID')
                self.alarmClockActive_screen = ScreenAlarmActive(name='screenAlarmActiveID')

                self.sm.add_widget(self.home_screen)
                self.sm.add_widget(self.displayOff_screen)
                self.sm.add_widget(self.alarmClock_screen)
                self.sm.add_widget(self.radio_screen)
                self.sm.add_widget(self.settings_screen)
                self.sm.add_widget(self.alarmClockActive_screen)

                self.sm.current = 'screenHomeID'

                return self.sm

        def on_start(self):
                self.eventCheckAlarm = Clock.schedule_interval(self.checkAlarmActive,1)

        def checkAlarmActive(self,*args):
                try:
                        response = requests.get(url+'alarmClock/alarmActive')
                        json_data = json.loads(response.text)
                        if response.status_code == 200:
                                if(json_data['state'] == 1):
                                        self.sm.current = "screenAlarmActiveID"
                        else:
                                print(response)
                except:
                        print("An exception occurred")
        
        #def on_touch_down(self, touch):
        #       print("TOUCH TOUCH TOUCH TOUCH TOUCH TOUCH TOUCH TOUCH")

        #Window.bind(on_touch_down=on_touch_down)

visu = VisuAlarmClock()
visu.run()