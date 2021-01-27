import time
import threading
import numpy as np

def limit(num, minimum=0, maximum=255):
        """Limits input 'num' between minimum and maximum values.
        Default minimum value is 1 and maximum value is 255."""
        return max(min(num, maximum), minimum)

class Light():
    debugMode = True
    __lightstate = False
    __ledStripeState = True
    __runSunsetLoop = False
    __cycletimeMs = 1000
    __startLed = 0
    __endLed = 146
    __brightness = 100
    
    __startLoopSec = 2
    
    def __init__(self,arduinoConnection):     
        self.arduinoConnection = arduinoConnection   
        print("init Light class")
        self.turnLightOff()

    def turnLightOn(self):
        print("set Light On")
        self.__color=(255,200,100) 
        self.__accessPixel()
        self.__lightstate = True
        
    def turnLightOff(self):
        print("set Light Off")
        self.__color=(0,0,0) 
        self.__accessPixel()
        self.__lightstate = False

    def getLightState(self):
        #print("get Light state: " + str(self.__lightstate))
        return self.__lightstate

    def getBrightness(self):
        #print("get Light brightness: " + str(self.__brightness))
        return self.__brightness

    def setBrightness(self,_input): 
        self.__brightness = int(_input)
        print("set Light brightness: " + str(self.__brightness))

        #if light already on change brightness
        if(self.__lightstate):
            self.__accessPixel()

    def setSunsetTime(self,_input):
        self.sunsetTimeSeconds = int(_input)*60
        print("set sunsetTime: " + str(self.sunsetTimeSeconds) + " sec")
    
    def turnLedStripeOn(self):
        self.__ledStripeState = True
        self.__endLed = 146
        print("set LED Stripe On")

        if(self.__lightstate):    
            self.__accessPixel()
        
    def turnLedStripeOff(self):
        self.__ledStripeState = False
        
        print("set LED Stripe Off")

        if(self.__lightstate):
            self.__startLed = 28
            self.__endLed = 146
            self.__color=(0,0,0)
            self.__accessPixel()
        
        self.__startLed = 0
        self.__endLed = 28
        self.__color=(255,200,100)
         
    def getLedStripeState(self):
        #print("get LED Stripe state: " + str(self.__ledStripeState))
        return self.__ledStripeState

    def __accessPixel(self):
        brightnessConverted = np.interp(self.__brightness,[0,100],[0.1,1])

        r = limit( round(self.__color[0] * brightnessConverted) ) 
        g = limit( round(self.__color[1] * brightnessConverted) ) 
        b = limit( round(self.__color[2] * brightnessConverted) ) 
        
        if self.debugMode:            
            print("r: "+str(r))
            print("g: "+str(g))
            print("b: "+str(b))
            print("a: "+str(brightnessConverted))

        self.arduinoConnection.writeData("<led," + str(r) + "," + str(g) + "," + str(b) + "," + str(self.__startLed) + "," + str(self.__endLed) + ">")

    def startSunset(self):
        self.timeout = time.time() + self.sunsetTimeSeconds #conv to seconds
        print("Sunsest Loop started for " + str(self.sunsetTimeSeconds) + "sec *******************************************************+") 
        
        self.__runSunsetLoop = True
        self.t = threading.Thread(target=self.__sunsetLoop)
        self.t.start()

    # def startWelcomeLoop(self):

    #     self.timeoutMainLoop = time.time() + self.__startLoopSec
    #     print("Sunsest Loop started for " + str(self.__startLoopSec) + "sec")

    #     #calc iterations of Brightness
    #     self.__runStartLoop = True
    #     self.tStartLoop = threading.Thread(target=self.__startLoop)
    #     self.tStartLoop.start()

    def __sunsetLoop(self):
        self.t = threading.currentThread()

        iterations = self.sunsetTimeSeconds / (self.__cycletimeMs / 1000)
        
        if self.debugMode:
            print("iterations: " + str(iterations))
        
        rTmp = 0 
        gTmp = 0
        bTmp = 0
        
        targetColor=(255,80,0) 
        
        while self.__runSunsetLoop:
            
            rTmp = rTmp + (targetColor[0] / iterations * 4)
            gTmp = gTmp + (targetColor[1] / iterations)
            bTmp = bTmp + (targetColor[2] / iterations)
        
            self.__color=(rTmp,gTmp,bTmp) 
            self.__accessPixel()

            if(time.time() >= self.timeout):
                print("sunset Loop closed")
                break
            
            time.sleep(self.__cycletimeMs/1000)

    def __startLoop(self):
        self.tStartLoop = threading.currentThread()

        iterations = self.__startLoopSec / (self.__cycletimeMs / 1000)
            
        if self.debugMode:
            print("iterations: " + str(iterations))
            
        rTmp = 0.0 
        gTmp = 0.0
        bTmp = 0.0
            
        while self.__runSunsetLoop:
            if(time.time() >= self.timeoutMainLoop/2):  

                rTmp = rTmp + (self.__color[0] / iterations)
                gTmp = gTmp + (self.__color[1] / iterations)
                bTmp = bTmp + (self.__color[2] / iterations)
                
            else:
                rTmp = rTmp - (self.__color[0] / iterations)
                gTmp = gTmp - (self.__color[1] / iterations)
                bTmp = bTmp - (self.__color[2] / iterations)

            if(time.time() >= self.timeout):
                print("sunset Loop closed")
                break

            self.__accessPixel()
                
            time.sleep(self.__cycletimeMs/1000)

        self.turnLedStripeOff()

    def close(self):
        self.__runSunsetLoop = False
        if self.t.joinable():
            self.t.join()
        self.turnLightOff()
        print("close led stripe")