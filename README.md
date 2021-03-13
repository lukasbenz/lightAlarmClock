# lightAlarmClock

#### DIY light alarm Clock. Build in a tissue box from Amazon. Totaly overengineered and way to expensive - but i dont care! 
#### Feel free to use some code or build it for yourself!(:

![lightAlarmClock](https://github.com/lukasbenz/lightAlarmClock/blob/develop/docuImg/world_map_of_cpp_STL_algorithms.png)


Hardware:
- Case tissue box: 
 	- https://www.amazon.de/gp/product/B079VHRWJQ/ref=ppx_yo_dt_b_asin_title_o02_s02?ie=UTF8&psc=1 
- Raspberry Pi 4 4gb    
- Case for the raspberry pi Geekworm Raspberry Pi 4 Gehäuse CNC ultra Slim   
- Arduino Nano
- Touch display waveshare 4inch HDMI
	- https://www.waveshare.com/wiki/4inch_HDMI_LCD
- Soundcard Hifiberry Amp2
	- https://www.hifiberry.com/shop/boards/hifiberry-amp2/
- Speaker Visaton vs-frs8 m
- LED Stripe WS2812b
- Plugable USB Bluetooth Adapter
- 12V to 5V converter
- Power Supply LEICKE 72W 12V 6A
 	- https://www.amazon.de/gp/product/B07FLZ1SGY/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&psc=1 
 
- other Stuff:
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
   						-   
 
     
      
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
