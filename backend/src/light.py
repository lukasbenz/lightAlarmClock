import time
import threading
import numpy as np

class Light():

    debugMode = False
    __lightstate = False
    __runSunsetLoop = False
    __ledStripeState = True
    
    __startLed = 0
    __endLed = 146
        
    __countLedsBuildIn = 28     #here define amount of LED´s within the case
    __countLedStripe = 146      #here define amount of LED´s within the LED Stripe

    __brightness = 100          #brightness of the LEds
    __colorSunset = (255,150,0) #custom color for sunset 
    __colorOn = (255,255,120)     #standard color On
    __colorOff = (0,0,0)        #standard color Off

    threadSunsetLoopName = "threadSunsetLoop"
    #Pink __lightColor = (255,100,100)

    def __init__(self,arduinoConnection):     
        self.arduinoConnection = arduinoConnection
        self.turnLightOff()
        print("init Light class")

    def turnLightOn(self):
          print("set Light On")
          self.__color = self.__colorOn
          self.__accessPixel()
          self.__lightstate = True
        
    def turnLightOff(self):
        self.stopSunsetLoop()

        print("set Light Off")
        self.__color = self.__colorOff
        self.__accessPixel()
        self.__lightstate = False

    def getLightState(self):
        if (self.debugMode):
            print("get Light state: " + str(self.__lightstate))
        return self.__lightstate

    def getBrightness(self):
        if (self.debugMode):
            print("get Light brightness: " + str(self.__brightness))
        return self.__brightness

    def setBrightness(self,_input): 
        self.__brightness = int(_input)
        if (self.debugMode): 
            print("set Light brightness: " + str(self.__brightness))

        #if light already on change brightness
        if(self.__lightstate):
            self.__accessPixel()

    def setSunsetTime(self,_input):
        self.sunsetTimeSeconds = int(_input)*60
        if (self.debugMode):
            print("set sunsetTime: " + str(self.sunsetTimeSeconds) + " sec")
    
    def turnLedStripeOn(self):
        self.__ledStripeState = True
        self.__endLed = self.__countLedStripe
        print("set LED Stripe On")

        if(self.__lightstate): #turn Led Stripe On - if it was active
            self.__accessPixel()
        
    def turnLedStripeOff(self):
        self.__ledStripeState = False
        print("set LED Stripe Off")

        if(self.__lightstate): #turn only Led Stripe off - if it was active
            self.__startLed = self.__countLedsBuildIn
            self.__endLed = self.__countLedStripe
            self.__color= self.__colorOff
            self.__accessPixel()
        
        self.__startLed = 0
        self.__endLed = self.__countLedsBuildIn
        self.__color=self.__colorOn

    def getLedStripeState(self):
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
        self.stopSunsetLoop()

        self.t = threading.Thread(target=self.__sunsetLoop, name=self.threadSunsetLoopName)
        print("Sunsest Loop started for " + str(self.sunsetTimeSeconds) + "sec") 
        
        self.__runSunsetLoop = True
        self.t.start()

    def stopSunsetLoop(self):
        for th in threading.enumerate():
            if (th.name == self.threadSunsetLoopName):
                print("Thread sunsetLoop is running")
                self.__runSunsetLoop = False
                th.join()
                print("stop sunsest Loop")
                break

    def __sunsetLoop(self):
        self.t = threading.currentThread()

        timeout = time.time() + self.sunsetTimeSeconds 
        timeoutHalf = time.time() + self.sunsetTimeSeconds/2 
        
        #iterations = self.sunsetTimeSeconds / (self.__cycletimeMs / 1000)
        iterations = self.sunsetTimeSeconds

        if self.debugMode:
            print("iterations: " + str(iterations))
        
        rTmp = 0 
        gTmp = 0
        bTmp = 0
        
        while self.__runSunsetLoop:
            #first half of the time only show red LED to create a realistic sunset
            if(time.time() < timeoutHalf):
                rTmp = rTmp + (self.__colorSunset[0] / iterations / 4)

            #second half smoothly add rest of the colors to reach sunset color
            else:
                rTmp = rTmp + (self.__colorSunset[0] / iterations * 3)
                gTmp = gTmp + (self.__colorSunset[1] / iterations * 2)
                bTmp = bTmp + (self.__colorSunset[2] / iterations * 2)

            self.__color=(rTmp,gTmp,bTmp) 
            self.__accessPixel()

            if(time.time() > timeout):
                print("sunset Loop closed")
                break
            
            time.sleep(1) #1 second cycle
            #time.sleep(self.__cycletimeMs/1000)

    def close(self):
        self.__runSunsetLoop = False
        if self.t.joinable():
            self.t.join()
        self.turnLightOff()
        print("close led stripe")


'''
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
'''
