import time
import threading

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
    #color=(1.0,0.4,0)
    color=(255,80,0)

    def __init__(self,arduinoConnection):     
        self.arduinoConnection = arduinoConnection   
        print("init Light class")
        self.turnLightOff()

    def turnLightOn(self):
        print("set Light On")
        self.__accessPixel(self.color[0],self.color[1],self.color[2],self.__brightness)
        self.__state = True

    def turnLightOff(self):
        print("set Light Off")
        self.__accessPixel(0,0,0,self.__brightness)
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

    def __accessPixel(self,r,g,b,a):
        
        r = limit(int(round(r /(a))))
        g = limit(int(round(g /(a))))
        b = limit(int(round(b /(a))))
        
        #if self.debugMode:
        #    if self.r > 255:
        #        print("warning: r: " + str(self.r) + "  > 255!")
        #    elif self.r < 0:
        #        print("warning: r: " + str(self.r) + "  < 0!")
        #    if self.g > 255:
        #        print("warning: g: " + str(self.g) + "  > 255!")
        #    elif self.g < 0:
        #        print("warning: g: " + str(self.g) + "  < 0!")
        #    if self.b > 255:
        #        print("warning: b: " + str(self.b) + " > 255!")
        #    elif self.b < 0:
        #        print("warning: b: " + str(self.b) + " < 0!")

        #self.r = limit(self.r)
        #self.g = limit(self.g)
        #self.b = limit(self.b)

        if self.debugMode:            
            print("r: "+str(r))
            print("g: "+str(g))
            print("b: "+str(b))
            print("a: "+str(a))

        self.arduinoConnection.writeData("<led," + str(r) + "," + str(g) + "," + str(b) + "," + str(self.__startLed) + "," + str(self.__endLed) + ">")

    def startSunset(self):
        self.timeout = time.time() + self.__sunsetTime #conv to seconds

        print("Sunsest Loop started for " + str(self.__sunsetTime) + "sec")
        
        #calc iterations of Brightness
        self.__runSunsetLoop = True
        self.t = threading.Thread(target=self.ledSunsetLoop)
        self.t.start()

    def ledSunsetLoop(self):
        self.t = threading.currentThread()

        iterations = self.__sunsetTime / (self.__cycletimeMs / 1000)
        
        if self.debugMode:
            print("iterations: " + str(iterations))
        
        aTmp = 0.0 
        rTmp = 0.0 
        gTmp = 0.0
        bTmp = 0.0
        
        while self.__runSunsetLoop:
            
            rTmp = rTmp + (self.color[0] / iterations * 4)
            gTmp = gTmp + (self.color[1] / iterations)
            bTmp = bTmp + (self.color[2] / iterations)
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