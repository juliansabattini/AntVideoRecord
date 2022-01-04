# AntVideoRecord Version 1.0

---
### Build instructions
---

*Assembling the physical support.*
1. Take the Waterproof Dustproof IP65 ABS plastic box (P4) and make a square cut in the center of 8 mm x 8 mm to insert the Raspberry camera (P10). Assemble the chamber and seal with silicone glue.
2. Make eight circular cuts of 4.8 mm in diameter at a radius of 25 mm to insert the lighting system with LEDs (P14). Insert the led diodes with silicone sealant to prevent the entry of moisture.
3. On each side, make two circular cuts of 10 mm diameter to glue the metric bolts (P15) with the threads facing out of the box. The AntvRecrord is then attached with nuts to each side.
4. On the back side of one side, make a 6 mm diameter cut to insert the gland plastic waterproof IP65 adjustable cable (P5). On the same side, make three cuts to place the LED Light Emitting Diode Diffused Red, Yellow and Green (P7). Then seal with silicone from both sides.
5. Optionally, a support printed in ABS can be made for the USB Female connector with a cover (Fig. 5), to extract the pendrive without having to remove the four fixing screws from the box. The installation of the waterproof IP65 12V 10A ON / OFF Rocker Switch (P6) on the sides of the box is also optional.

---

*Assembling the electronic circuit.*
1. Assemble the power system that consists of connecting the cables from the solar panel (P2) and the gel battery (P1) to the solar voltage regulator (P3) keeping polarity.
2. Solder the input cables of the power system to each voltage regulator (P11) in the IN + and IN- position according to the corresponding polarity. Do the same with the egress ones (OUT +, OUT-). With a flat screwdriver, turn the upper screw to modify the output voltage until it reaches the desired one. For this it is necessary to have a multitester. For the Raspberry Pi Zero W the output voltage has to be 5.2v, while for the lighting system 3.0v. To carry out this operation, you must temporarily connect the power system to make the electronic configuration of the voltage regulators.
2. Join the voltage regulator cables coming out for the Raspberry Pi Zero W with a mini USB male plug and connect it to the PWR IN. An alternative is to feed power through the GPIO, with pins 2 (+) and 4 (GND).
3. Make the series connection of two White LED diodes (P14) joining anode with cathode of each one. This way, you will assemble four series pairs that you must connect them in parallel with each other, that is, anode with anode of each pair, and cathode with cathode of each pair. Once the connection is finished, connect with the output cables of the other voltage regulator (P11).
4. Once the video camera (P10) is inserted, use the cable (P9) to connect it with the Raspberry Pi Zero W (P8)
5. The Red, Yellow and Green LEDs (P7) must connect the anode in parallel to pin 34 (GND). The Red connect to the GPIO14 (pin 8), Yellow GPIO27 (pin 13) and the Green GPIO22 (pin 15).
6. Connect the Mini USB to USB Female OTG Cable, and insert a 2.0 pendrive

---
### Operation Instructions 
---

*Installing the software suite*
1. Take the microSD card (P12) and connect it to your computer.
2. Use free software such as SD Card Formatter to format the microSD card.
3. Download the image (.img) file Raspbian Buster with Desktop from the Raspberry Pi website (https://www.raspberrypi.org/downloads/raspbian/).
4. Copy the Raspbian image to the microSD card using Raspberry Pi Imager.
5. Once Raspbian is installed on the microSD card it will appear on the computer as two separate drives boot and roots. 
6. Eject the microSD card from the computer and insert it in the AntVRecord’s Raspberry Pi.
7. Connect a mouse, keyboard and monitor to the Raspberry Pi and turn the power on. This step will require a micro-USB to USB adapter, a USB hub, and a mini-HDMI to HDMI adapter. The Raspberry Pi will boot and the graphical interface of Raspbian will appear on the monitor.
8. Upon the first start, a window will appear with instructions to configure the OS. Follow all the instructions to set up the country, password, wifi connection, and updates.
9. If not already done, connect to your Wifi network using the Wifi icon at the top right of the screen.
10. Open a terminal window and type the following commands: 
	(a) Ensure the OS is up to date:
	```
	sudo apt-get update && sudo apt-get upgrade
	```
	(b) Install Python 3:
	```
	sudo apt-get install python3
	```
	(c) Enable camera, SSH connection service, VNC Server from Raspberry PI configuration menu on desktop startup.
	(d) Install Remotely Access Raspberry Pi Via Bluetooth (SSH / VNC) via terminal and then reboot:
	```
	sudo apt install network-manager-gnome blueman
	```
	(e) When restarting click on the recently installed Bluetooth icon, then Local Service, Services, check the Network Access Point (NAp) option and then assign an IP route for connection via VNC Windows (ejm IP Address: 10.20.30. # #). Then click on Bluetooth Devices and search for the device you want to pair. It is recommended to pair all the devices that will be used for recording, at least one laptop, tablet and smartphone. In Windows it is recommended to install the VNC Viewer application as well as in the tables or smartphone by Google Play or AppStore. In the first case, enable and pair bluetooth with AntVRecord, and then right click on the Bluetooth icon, Join a Personal Area Network, then select the device, right click and Connect Using Access Point. After that, in the VNC Viewer application enter the previously configured IP address, and then it will ask for User and Password. It is recommended to change it from the Raspberry environment in the configuration section.
	11. Restart the Raspberry Pi to apply all the changes. 

---

*Installing AntVRecord OS*
1. Once Raspbian has restarted, open a terminal windows and type:
  ```
	cd Desktop
	git clone https://www.github.com/fd-sturniolo/ant_project
  ```
2. Install the necessary library for the operation AntVRecord OS, open a terminal Windows and type:
  ```
	sudo apt-get install python3-pyqt5
	sudo apt-get install python3-rpi.gpio
	sudo apt install python3-smbus
	sudo pip3 install Adafruit_DHT
	pip3 install tomlkit
  ```
	
3. Move the shortcut AntVRecord contained in the ‘ant_project’ folder to the Raspbian desktop. Open AntVRecord OS using “terminal mode” 

---

## Contribution
*Dr. Julian Alberto Sabattini (julian.sabattini@fca.uner.edu.ar)
*Developers*
⌨️ [Martin Paz](https://github.com/freischarler) (martin.paz@live.com.ar) 
⌨️ [Sturniolo Francisco](https://github.com/fd-sturniolo) (fd.sturniolo@gmail.com)

---

