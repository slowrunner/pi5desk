#/bin/bash

echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

echo -e "RULES LOADED - NOW DISCONNECT AND RECONNECT THE USB CABLE TO THE OAK-D-LITE"
