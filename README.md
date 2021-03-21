# lightAlarmClock

#### DIY light alarm Clock. Build in a tissue box from Amazon. Totaly over engineered and way to expensive - but i dont care! 
#### Feel free to use some code or build it for yourself!:)

<p float="center">
<img src="https://github.com/lukasbenz/lightAlarmClock/blob/develop/docuImg/outside/main.JPG" width="1000" />
</p>
<p float="left">
  <img src="https://github.com/lukasbenz/lightAlarmClock/blob/develop/docuImg/outside/left.JPG" width="500" />
  <img src="https://github.com/lukasbenz/lightAlarmClock/blob/develop/docuImg/outside/right.JPG" width="500" />
</p>

Hardware:
- Case tissue box: 
 	- https://www.amazon.de/gp/product/B079VHRWJQ/ref=ppx_yo_dt_b_asin_title_o02_s02?ie=UTF8&psc=1 
- Raspberry Pi 4 4gb:
	- https://www.raspberrypi.org/products/raspberry-pi-4-model-b/
- Case for the raspberry pi Geekworm Raspberry Pi 4 Gehäuse CNC ultra Slim:
	- https://www.amazon.de/Geekworm-Raspberry-Ultra-D%C3%BCnne-Aluminium-K%C3%BChlk%C3%B6rper/dp/B07WZXPR2W/ref=dp_prsubs_1?pd_rd_i=B07WZXPR2W&psc=1
- Arduino Nano:
	- https://store.arduino.cc/arduino-nano
- Touch display waveshare 4inch HDMI
	- https://www.waveshare.com/wiki/4inch_HDMI_LCD
- Soundcard Hifiberry Amp2
	- https://www.hifiberry.com/shop/boards/hifiberry-amp2/
- Speaker Visaton vs-frs8 m:
	- https://www.amazon.de/gp/product/B0017KT3S2/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&psc=1
- LED Stripe WS2812b:
	- https://www.amazon.de/gp/product/B01CDTEID0/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1
- Plugable USB Bluetooth Adapter:
	- https://www.amazon.de/gp/product/B009ZIILLI/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1
- Pololu 12V to 5V converter:
	- https://eckstein-shop.de/Pololu-5V-32A-Step-Down-Voltage-Regulator-D36V28F5
- Power Supply LEICKE 72W 12V 6A
 	- https://www.amazon.de/gp/product/B07FLZ1SGY/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&psc=1 
 
- other small parts:
	- Rotary Encoder Modul EC11 Digital Potentiometer
   		- https://www.amazon.de/gp/product/B08728PS6N/ref=ppx_yo_dt_b_asin_title_o02_s02?ie=UTF8&psc=1
   	- Push-Button
   		- https://www.amazon.de/gp/product/B0811QKG1R/ref=ppx_yo_dt_b_asin_title_o02_s02?ie=UTF8&psc=1 
   	- USB connection for extrnal handy charging 
   		- https://www.amazon.de/gp/product/B003L79T06/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1
	- XLR connection for external LED Stripe
   		- https://www.amazon.de/gp/product/B00A7W4RKK/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1
   		- https://www.amazon.de/gp/product/B002A3IWIW/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1
	- Micro USB cables for connection from raspberry pi to arduino & touch display
   		- https://www.amazon.de/gp/product/B001D1H4BS/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1
	- HDMI cable between raspberry pi & display
   		- https://www.amazon.de/gp/product/B01E6UKVKS/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1
	- Connection cable between Display / RaspberryPI (very useful!): 
   		- https://www.berrybase.de/raspberry-pi/raspberry-pi-computer/kabel-adapter/gpio-csi-dsi-kabel/gpio-adapter-kabel-f-252-r-raspberry-pi-40-pin-buchse-26-pin-buchse-grau-15cm				-   
 
     
      
Features: 
 - InternetConnection for WLAN Radio / Time synchronization
 - AlarmClock
 - REST API
 - KIVY Visualization
 - Remote Handy connection via VNC Client APP     
 - LED Stripe WS2812b
 - GPIO Encoder / Buttons
 
- Alarm clock using the Internet Time 
	- synchronized via Wlan
- Internet Radio 
	- can be used separate & for the alarm clock tone
- WS2812B LED Stripe 
	- can be used as a sunset & for the normal light
	- the LED Stripe is splitted in an intern Light & an external LED Stripe
- Bluetooth adapter to use the light alarm clock as a bluetooth speaker 
- Touchdisplay with a "Kivy" based GUI
