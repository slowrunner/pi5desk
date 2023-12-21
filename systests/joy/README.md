# Setup 2.4GHz Wireless USB SNES Gamepad


1) Plugged in USB WiFi Gamepad adapter

```
$ lsusb
  ...
  Bus 001 Device 005: ID 0079:0126 DragonRise Inc.
```

# Don't need this to be installed, but it allows testing before solving the "joystick in docker" configuration

```
sudo apt install joystick

jstest --normal /dev/input/js0

Driver version is 2.1.0.
Joystick (Controller) has 6 axes (X, Y, Z, Rz, Hat0X, Hat0Y)
and 13 buttons (BtnA, BtnB, BtnC, BtnX, BtnY, BtnZ, BtnTL, BtnTR, BtnTL2, BtnTR2, BtnSelect, BtnStart, BtnMode).
Testing ... (interrupt to exit)
Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:off  9:off 10:off 11:off 12:off 


Pad Up:    Axis 1: -32767
Pad Dn:    Axis 1:  32767

Pad Left:  Axis 0: -32767
Pad Right: Axis 0:  32767

Select: Button 8
Start:  Button 9

X: Button 0
B: Button 2
Y: Button 3
A: Button 1

Forefinger pads:
Left:  Button 4
Right: Button 5


```


NOTE:  
- Charging: blinking red  
- Fully Charged: LED off  

- Low Battery: blinking red  
- Battery OK: solid red  


- Instructions say do not charge more than 2 hours  

- Power Consumption:  12 mA at 11.13v (probably 25mA at 5v through USB)`  

=== Instruction manual for 2.4 GHz Wireless USB Controller ===  

Please read before use:  
1. Make sure the controller is fully charged prior to first use to ensure battery is at maximum capacity.  
2. Make sure to use a standard 5v 1A charger to avoid damage to the controller.  
3. Do not charge the controller for over 2 hours.  
4. The red LED will flash rapidly during normal use indicating that the controller is low on battery.  
   Please charge the controller immediately to avoid losing connection.  
5. The red LED will blink slowly when the controller is charging, it will disappear once the   
   controller is fully charged and ready for use.  
6. When the controller and the receiver cannot be connected successfully,  
   press the DOWN+SELECT+START buttons at the same time, and the red LED  
   of the controller flashes to reset.  They can be paired successfully.  


Pairing the controller:  
1. Turn on the controller by pressing the START button, the red LED will blink slowly  
2. Press the START button again, the red LED will flash rapidly indicating the controller  
   is ready to pair.  
3. Plug in the USB receiver to the PC, the red LED will stay lit  
   to indicate the controller has been paired successfully.  


LED Functions:  
1.  Press START button, LED flashes slowly: controller is "On"  
2.  With controller on, press START again, and LED flashes quickly: searching for adapter  
3.  LED on continuously:  connected/paired successfully  
4.  During charging, LED flashing every 2 seconds: charging - LED turns off when fully charged  
5.  LED flashes quickly intermittently:  battery low  


# Examples

For Python access, install evdev:

```
sudo pip3 install --break-system-packages evdev

see: https://python-evdev.readthedocs.io/en/latest/usage.html

pi@RPi5DESK:~/pi5desk/systests/joy $ sudo python3 -m evdev.evtest
ID  Device               Name                                Phys                                Uniq
-----------------------------------------------------------------------------------------------------------------
0   /dev/input/event0    pwr_button                          gpio-keys/input0                        
1   /dev/input/event1    vc4-hdmi-0                          vc4-hdmi-0/input0                       
2   /dev/input/event2    vc4-hdmi-1                          vc4-hdmi-1/input0                       
3   /dev/input/event3    Jieli Technology UACDemoV1.0        usb-xhci-hcd.1-2/input2             1120040804060316
4   /dev/input/event4    Controller                          usb-xhci-hcd.0-1/input0                 

Select devices [0-4]: 4
Listening for events (press ctrl-c to exit) ...

=== PRESSED JOYPAD-UP
time 1703175481.424277 type 3 (EV_ABS), code 1    (ABS_Y), value 0
time 1703175481.424277 --------- SYN_REPORT --------
time 1703175481.576286 type 3 (EV_ABS), code 1    (ABS_Y), value 128
time 1703175481.576286 --------- SYN_REPORT --------
time 1703175482.344332 type 3 (EV_ABS), code 1    (ABS_Y), value 255
time 1703175482.344332 --------- SYN_REPORT --------
time 1703175482.520343 type 3 (EV_ABS), code 1    (ABS_Y), value 128
time 1703175482.520343 --------- SYN_REPORT --------
time 1703175483.080381 type 3 (EV_ABS), code 0    (ABS_X), value 0
time 1703175483.080381 --------- SYN_REPORT --------

=== PRESSED JOYPAD-DN
time 1628955329.737951 type 3 (EV_ABS), code 1    (ABS_Y), value 255
time 1628955329.737951 --------- SYN_REPORT --------
time 1628955329.907947 type 3 (EV_ABS), code 1    (ABS_Y), value 128
time 1628955329.907947 --------- SYN_REPORT --------

=== PRESSED JOYPAD-RIGHT
time 1628955374.335807 type 3 (EV_ABS), code 0    (ABS_X), value 255
time 1628955374.335807 --------- SYN_REPORT --------
time 1628955374.451807 type 3 (EV_ABS), code 0    (ABS_X), value 128
time 1628955374.451807 --------- SYN_REPORT --------

=== PRESSED JOYPAD-LEFT
time 1628955400.639726 type 3 (EV_ABS), code 0    (ABS_X), value 0
time 1628955400.639726 --------- SYN_REPORT --------
time 1628955400.767729 type 3 (EV_ABS), code 0    (ABS_X), value 128
time 1628955400.767729 --------- SYN_REPORT --------

```

# FOR JOYSTICK IN DOCKER SEE ../configs/docker/README
