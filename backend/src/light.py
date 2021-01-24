import time
import threading
import numpy as np

def limit(num, minimum=0, maximum=255):
        """Limits input 'num' between minimum and maximum values.
        Default minimum value is 1 and maximum value is 255."""
        return max(min(num, maximum), minimum)

class Light():
    debugMode = True
    __state = False
    __useLedStripe = True
    __sunsetTime = 10
    __brightness = 100
    __runSunsetLoop = False
    __cycletimeMs = 1000
    __startLed = 0
    __endLed = 146
    __color=(255,120,10)

    def __init__(self,arduinoConnection):     
        self.arduinoConnection = arduinoConnection   
        print("init Light class")
        self.turnLightOff()

    def turnLightOn(self):
        print("set Light On")
        self.__color=(255,120,10) 
        self.__accessPixel()
        self.__state = True
        
    def turnLightOff(self):
        print("set Light Off")
        self.__color=(0,0,0) 
        self.__accessPixel()
        self.__state = False

    def getLightState(self):
        #print("get Light state: " + str(self.__state))
        return self.__state

    def getBrightness(self):
        #print("get Light brightness: " + str(self.__brightness))
        return self.__brightness

    def setBrightness(self,_input): 
        self.__brightness = _input
        print("set Light brightness: " + str(self.__brightness))

    def setSunsetTime(self,_input):
        self.sunsetTime = _input
        print("set sunsetTime: " + str(self.__sunsetTime))
    
    def getSunsetTime(self):
        #print("get sunsetTime: " + str(self.sunsetTime))
        return self.__sunsetTime

    def turnLedStripeOn(self):
        self.__useLedStripe = True
        self.__endLed = 146
        print("set LED Stripe On")

    def turnLedStripeOff(self):
        self.__useLedStripe = False
        self.__endLed = 27
        print("set LED Stripe Off")

    def getLedStripeState(self):
        #print("get LED Stripe state: " + str(self.__useLedStripe))
        return self.__useLedStripe

    def __accessPixel(self):
        
        brightnessConverted = np.interp(self.__brightness,[0,100],[255,1])
        print("bright converted" + str(brightnessConverted))
        print("raw: " + str(self.__brightness))

        r = limit(int(round(self.__color[0] / brightnessConverted)))
        g = limit(int(round(self.__color[1] / brightnessConverted)))
        b = limit(int(round(self.__color[2] / brightnessConverted)))
        
        if self.debugMode:            
            print("r: "+str(r))
            print("g: "+str(g))
            print("b: "+str(b))
            print("a: "+str(brightnessConverted))

        self.arduinoConnection.writeData("<led," + str(r) + "," + str(g) + "," + str(b) + "," + str(self.__startLed) + "," + str(self.__endLed) + ">")

    def startSunset(self):
        self.timeout = time.time() + self.__sunsetTime #conv to seconds

        print("Sunsest Loop started for " + str(self.__sunsetTime) + "sec")
        
        #calc iterations of Brightness
        self.__runSunsetLoop = True
        self.t = threading.Thread(target=self.__sunsetLoop)
        self.t.start()

    def __sunsetLoop(self):
        self.t = threading.currentThread()

        iterations = self.__sunsetTime / (self.__cycletimeMs / 1000)
        
        if self.debugMode:
            print("iterations: " + str(iterations))
        
        aTmp = 0.0 
        rTmp = 0.0 
        gTmp = 0.0
        bTmp = 0.0
        
        while self.__runSunsetLoop:
            
            rTmp = rTmp + (self.__color[0] / iterations * 4)
            gTmp = gTmp + (self.__color[1] / iterations)
            bTmp = bTmp + (self.__color[2] / iterations)
            aTmp = self.__brightness

            if self.debugMode:
                print("rTmp: "+str(rTmp))
                print("gTmp: "+str(gTmp))
                print("bTmp: "+str(bTmp))
                print("aTmp: "+str(aTmp))

            #for i in range(self.__countLEDs):
            self.__accessPixel(rTmp,gTmp,bTmp,aTmp,self.startLed,self.endLed)
            
            if self.debugMode:
                print("r: "+str(self.r))
                print("g: "+str(self.g))
                print("b: "+str(self.b))
                print("a: "+str(aTmp))

            if(time.time() >= self.timeout):
                print("sunset Loop closed")
                break
            
            time.sleep(self.__cycletimeMs/1000)

    def close(self):
        self.__runSunsetLoop = False
        if self.t.joinable():
            self.t.join()
        self.turnLightOff()
        print("close led stripe")