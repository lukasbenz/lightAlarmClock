import time
import threading
import numpy as np

class Light():
    debugMode = True
    __lightstate = False
    __ledStripeState = True
    __runSunsetLoop = False
    __startLed = 0
    __endLed = 146
    __brightness = 100
    #Pink __lightColor = (255,100,100)
    __lightColor = (255,120,20)
    #__onOffLoopSec = 1

    def __init__(self,arduinoConnection):     
        self.arduinoConnection = arduinoConnection   
        #self.__onOffLoop = True
        #self.tonOffLoop = threading.Thread(target=self.__smoothOnOffLoop)
        #self.tonOffLoop.start()
        self.turnLightOff()
        print("init Light class")

    def turnLightOn(self):
          print("set Light On")
          self.__color = self.__lightColor
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
        self.__color=self.__lightColor
         
    def getLedStripeState(self):
        #print("get LED Stripe state: " + str(self.__ledStripeState))
        return self.__ledStripeState

    def __accessPixel(self):
        
        brightnessConverted = np.interp(self.__brightness,[0,100],[0,1])

        r = round(self.__color[0] * brightnessConverted) 
        g = round(self.__color[1] * brightnessConverted)  
        b = round(self.__color[2] * brightnessConverted)  

        r = np.clip(r, 0, 255)
        g = np.clip(g, 0, 255)
        b = np.clip(b, 0, 255)
                
        if self.debugMode:            
            print("r: "+str(r))
            print("g: "+str(g))
            print("b: "+str(b))
            print("a: "+str(brightnessConverted))

        self.arduinoConnection.writeData("<led," + str(r) + "," + str(g) + "," + str(b) + "," + str(self.__startLed) + "," + str(self.__endLed) + ">")

    def startSunset(self):
        print("Sunsest Loop started for " + str(self.sunsetTimeSeconds) + "sec *******************************************************+") 
        
        #self.__lightstate = True
        
        self.__runSunsetLoop = True
        self.t = threading.Thread(target=self.__sunsetLoop)
        self.t.start()


    def __sunsetLoop(self):
        self.t = threading.currentThread()

        timeout = time.time() + self.sunsetTimeSeconds #conv to seconds
        timeoutHalf = time.time() + self.sunsetTimeSeconds/2 #conv to seconds
        
        #iterations = self.sunsetTimeSeconds / (self.__cycletimeMs / 1000)
        iterations = self.sunsetTimeSeconds

        #if self.debugMode:
            #print("iterations: " + str(iterations))
        
        rTmp = 0 
        gTmp = 0
        bTmp = 0
        
        targetColor = (255,100,0)
        
        while self.__runSunsetLoop:
            #first half of the time only red color
            if(time.time() < timeoutHalf):
                rTmp = rTmp + (targetColor[0] / iterations / 4)

            #second half smoothly add green to reach yellow color
            else:
                rTmp = rTmp + (targetColor[0] / iterations * 3)
                gTmp = gTmp + (targetColor[1] / iterations * 2)
                bTmp = bTmp + (targetColor[2] / iterations * 2)

            self.__color=(rTmp,gTmp,bTmp) 
            self.__accessPixel()

            if(time.time() > timeout):
                print("sunset Loop closed")
                break
            
            time.sleep(1) #1 second cycle
            #time.sleep(self.__cycletimeMs/1000)

    def __smoothOnOffLoop(self):
        self.tStartLoop = threading.currentThread()
        iterations = self.__onOffLoopSec / 100

        rTmp = self.__color[0]
        gTmp = self.__color[1]
        bTmp = self.__color[2]
        
        while self.__runSunsetLoop:
            rTmp = rTmp - (self.__color[0] / iterations)
            gTmp = gTmp - (self.__color[1] / iterations)
            bTmp = bTmp - (self.__color[2] / iterations)

            self.__color=(rTmp,gTmp,bTmp) 
            self.__accessPixel()
            
            if(time.time() >= self.timeout):
                pass

            time.sleep(100)

    def close(self):
        self.__runSunsetLoop = False
        if self.t.joinable():
            self.t.join()
        self.turnLightOff()
        print("close led stripe")