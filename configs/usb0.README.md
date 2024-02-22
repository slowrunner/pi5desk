Set up usb0 networking on Raspberry Pi 5 USB-C connector

Ref: https://forums.raspberrypi.com/viewtopic.php?p=2195159#p2195179

(For a never booted system REF: https://forums.raspberrypi.com/viewtopic.php?t=364247)

1) sudo nano /etc/network/interfaces.d/g_ether
```
auto usb0 
allow-hotplug usb0 
iface usb0 inet static
        address 192.168.186.3
        netmask 255.255.0.0

auto usb0.1
allow-hotplug usb0.1
iface usb0.1 inet dhcp

EOF
```

Known Issues:  
- This solution is IPv4 only.
- Using a static IP address is not ideal. There is a 1 in 64,516 chance of a conflict.
- If using this on multiple PI that will be connected together (e.g. using an ethernet switch) each Pi must have a unique IP address in the 169.254.0.0/16 subnet.
- Same thing applies when using multiple Pi connected via the USB ethernet gadget to the same USB host.
- This configures one end of the link only. Additional configuration may be required on the other end.
- Your Pi will show two ethernet interfaces. One may not be up.

How it works:  
Placing a file in /etc/network/interfaces.d makes Network Manager ignore any interfaces configured in it.  

The first block configures the actual interface with a static IP address in the link local/zeroconf/mDNS/avahi/Bonjour subnet.   
Most modern OS on the other end of the link will fallback to this subnet in the absense of a DHCP server.   
The Pi can be accessed via it's configured static address.  

The second block creates a virtual interface and configures ro use DHCP. 
If you later add a DHCP server to your network or move the Pi to a network with one it will get it's network configuration  
for this interface in the usual manner.  

2) sudo apt update && sudo apt upgrade -y

3) add to /boot/firmware/config.txt
dtoverlay2,dr_mode=peripheral

4) add to end of /boot/firmware/cmdline.txt
modules-load=dwc2,g_ether

5) reboot
