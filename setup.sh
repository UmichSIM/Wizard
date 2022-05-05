#!/bin/bash

# activate racing wheel
sudo usb_modeswitch -c /etc/usb_modeswitch.d/046d:c261
sudo usb_modeswitch -c /etc/usb_modeswitch.d/046d:c261

# disable firewall
sudo systemctl stop firewalld.service
sudo systemctl stop ufw

# launch carla server
cd ~/carla
make launch &

# second server
cd ~/Desktop/SIM_Wizard/Wizard-Server
./bin/wizard-server &

# launch client
# cd ~/Desktop/SIM_Wizard/Wizard
# poetry run python ./wizard/main.py