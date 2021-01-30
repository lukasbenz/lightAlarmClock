
import serial
import threading
import requests
import json

url = 'http://127.0.0.1:5000/api/'

class ArduinoConnection():
    debugMode = False
    __runRecLoop = False

    def __init__(self):        
        try:
            self.s = serial.Serial('/dev/ttyACM0', 9600)
            self.s.flushInput()
            print("init ArduinoConnection class")
            self.startRecLoop()

        except:
            print("EXCEPTION ERROR init serial - no Arduino available")

    def startRecLoop(self):
        print("start recLoop with arduino")
        self.__runRecLoop = True
        self.t = threading.Thread(target=self.__recLoop)
        self.t.start()

    def __recLoop(self):
        self.t = threading.currentThread()
        while(self.__runRecLoop):
            try:
                rawData = self.s.readline()
                rawData.strip()

                rawDatadecoded = str(rawData.decode("utf-8"))
                
                if(self.debugMode):
                    print("rawRecData:" + str(rawData))
                    print("recDataDecoded: " + rawDatadecoded)    
                
                inputSplit = rawDatadecoded.split(",")
                
                #use encoder so control system Volume
                if(inputSplit[0] == "enc"):
                        
                        if(inputSplit[1] == "pressed"): #mute
                            response = requests.get(url+'system/volume/mute/state')
                            json_data = json.loads(response.text)  
                            if response.status_code == 200:
                                if(json_data['state']): #if TRUE system ist muted - so unmute it
                                        requests.post(url+'system/volume/mute/off')
                                else: #if FALSE system is unmuted - so mute it
                                        requests.post(url+'system/volume/mute/on')         
                        
                        elif(inputSplit[1] == "negEdge"): #set volume
                            response = requests.get(url+'system/volume')
                            json_data = json.loads(response.text)  
                            if response.status_code == 200:
                                volumeTmp = int(json_data['value'])
                                volumeTmp += 5
                                data = {'value': int(volumeTmp)}
                                requests.post(url+'system/volume', json=data)

                        elif(inputSplit[1] == "posEdge"): #set volume
                            response = requests.get(url+'system/volume')
                            json_data = json.loads(response.text)  
                            if response.status_code == 200:
                                volumeTmp = int(json_data['value'])
                                volumeTmp -= 5
                                data = {'value': int(volumeTmp)}
                                requests.post(url+'system/volume', json=data)

                        else:
                            print("unknown enc command from arduino")
                    
                # use main Button to turn light ON/OFF    
                elif(inputSplit[0] == "mainBtn"):
                    response = requests.get(url+'light/state')
                    json_data = json.loads(response.text)  
                    if response.status_code == 200:
                        if(json_data['state']): #if TRUE light is ON - so turn it off
                                requests.post(url+'light/off')
                                requests.post(url+'radio/stop')
                        else: #if FALSE light is OFF - so turn it on
                                requests.post(url+'light/on')
                                requests.post(url+'radio/play')         
                                         
            except:
                print("EXCEPTION ERROR in recLoop")
    
    def writeData(self,string):
        try:
            print("writeData: " + str(string))
            self.s.write(string.encode("utf-8"))
        except:
            print("EXCEPTION ERROR write data")

    def close(self):
        self.__runRecLoop = False
        if self.t.joinable():
            self.t.join()
        print("close serial arduino connection")
