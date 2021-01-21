 // NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#include <Bounce2.h>

//------------------------------------------
// LED STRIPE
// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(146, 7, NEO_GRB + NEO_KHZ800);

//27 intern
//146 stripe

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing


//------------------------------------------
// ENCODER

#define encoderPinA 2
#define encoderPinB 3
#define btnMain 5
#define btnEnc1 4
#define pinDispLight 9

volatile int encoderPos = 0; // a counter for the dial

unsigned int lastReportedPos = 1; // change management
static boolean rotating = false; // debounce management

int button = LOW;
int old_button = LOW;

// interrupt service routine variables
boolean A_set = false;
boolean B_set = false;

//------------------------------------------
// variables to hold the parsed data
int intR = 0;
int intG = 0;
int intB = 0;
int startLed = 0;
int endLed = 0;
boolean newData = false;

int bright = 255;
int brightNorm = 1;

Bounce debounceBtn1 = Bounce();
Bounce debounceBtn2 = Bounce();

//============

void setup() {

//LED STRIPE
    // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
    // Any other board, you can remove this part (but no harm leaving it):
    #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
      clock_prescale_set(clock_div_1);
    #endif
    // END of Trinket-specific code.
    pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
    
    pixels.clear();
    pixels.show();

    Serial.begin(9600);

//ENCODER
    pinMode(encoderPinA, INPUT_PULLUP);
    pinMode(encoderPinB, INPUT_PULLUP);
    
    attachInterrupt(0, doEncoderA, CHANGE); // encoder pin on interrupt 0 (pin 2)
    attachInterrupt(1, doEncoderB, CHANGE); // encoder pin on interrupt 1 (pin 3)

//Buttons
    pinMode(btnMain, INPUT_PULLUP);
    pinMode(btnEnc1, INPUT_PULLUP);
   
    debounceBtn1.attach(btnMain);
    debounceBtn1.interval(10);
    debounceBtn2.attach(btnEnc1);
    debounceBtn2.interval(10);

}

//============
bool test = true;
void loop() 
{
    rotating = true; // reset the debouncer
    if (lastReportedPos != encoderPos)
    {
      //sendPosition();
      
      if(encoderPos > lastReportedPos)
      {
        sendPosEdge();
      }
      else
      { 
        sendNegEdge();
      }
      lastReportedPos = encoderPos;
    }
  
    //Button check positive edges
    
    debounceBtn1.update();
    debounceBtn2.update();

    if(debounceBtn1.fell())
    {
    Serial.println("mainBtn,pressed");     
    }   
    if(debounceBtn2.fell())
    {
      Serial.println("enc,pressed");     
    }

    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        setLedStripe();
        setDisplayBrightness();
        newData = false;
    }
  
}

//============

void sendPosEdge()
{
Serial.println("enc,posEdge");
}

void sendNegEdge()
{
Serial.println("enc,negEdge");
}

void sendPosition()
{
Serial.print("enc1Pos,");
Serial.println(encoderPos,DEC);
}
//============


// ------------- Interrupt Service Routines ------------------------------

// ISR Interrupt on A changing state (Increment position counter)
void doEncoderA()
{
if( digitalRead(encoderPinA) != A_set ) // debounce once more
{
  A_set = !A_set;
  // adjust counter +1 if A leads B
  if ( A_set && !B_set )
    encoderPos += 1;
    rotating = false; // no more debouncing until loop() hits again
}
}// ------------------- doEncoderA ----------------------------------------

// ISR Interrupt on B changing state, same as A above
void doEncoderB()
{
if( digitalRead(encoderPinB) != B_set )
{
  B_set = !B_set;
  //adjust counter -1 if B leads A
  if( B_set && !A_set )
    encoderPos -= 1;
    rotating = false;
}
}// -------------------- doEncoderB --------------------------------------



//---------------Communication-----------------------------------
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars, ",");
    
    if(strtokIndx == "ledStripe") {
      strtokIndx = strtok(tempChars, ",");     
      intR = atoi(strtokIndx);        
  
      strtokIndx = strtok(NULL, ",");     
      intG = atoi(strtokIndx);        
  
      strtokIndx = strtok(NULL, ",");     
      intB = atoi(strtokIndx);        
  
      strtokIndx = strtok(NULL, ",");     
      startLed = atoi(strtokIndx);        
  
      strtokIndx = strtok(NULL, ",");     
      endLed = atoi(strtokIndx);        
    }
    else if(strtokIndx == "display") {
      strtokIndx = strtok(NULL, ",");
      bright = atoi(strtokIndx);
    }   
}

void setLedStripe() {
  showParsedLedData();
  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
  for(int i=startLed; i<endLed; i++) { // For each pixel...
    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    // Here we're using a moderately bright green color:
    pixels.setPixelColor(i, pixels.Color(intR, intG, intB));
  }
  pixels.show();   // Send the updated pixel colors to the hardware.
}


void showParsedLedData(){
    Serial.print("R: ");
    Serial.println(intR);
    Serial.print("G: ");
    Serial.println(intG);
    Serial.print("B: ");
    Serial.println(intB);
    Serial.print("startLed: ");
    Serial.println(startLed);
    Serial.print("endLed: ");
    Serial.println(endLed);
}


void setDisplayBrightness(){
  brightNorm = round((bright * 255) / 100);
  showParsedDisplayData();
  analogWrite(pinDispLight, brightNorm);
}

void showParsedDisplayData(){
    Serial.print("brightness input 0-100: ");
    Serial.println(bright);
    Serial.print("brightness normalized 0-255: ");
    Serial.println(brightNorm);
}
