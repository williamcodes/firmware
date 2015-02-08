# Raspberry π

## Overview
- connect XBee to GPIO serial pins directly
- device is /dev/ttyAMA0
- then standard python `serial` library can be used

## Basic Setup
```sh
sudo raspi-config
# 1, 2, 4 > Locale, reboot
sudo raspi-config
# 4 > Change Timezone, Change Keyboard Layout, 8 > Serial > Off, reboot

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install usb-modeswitch wvdial supervisor python3-pip vnstat
sudo pip3 install -Ur requirements.txt

sudo ln -sf /home/pi/pi/conf/wvdial.conf /etc/
sudo emacs /etc/ppp/peers/wvdial
# # usepeerdns
sudo emacs /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 8.8.4.4
sudo chattr +i /etc/resolv.conf

sudo ssh-keygen
sudo ssh-copy-id hubs@hubs.heatseeknyc.com

sudo ln -s /home/pi/pi/conf/supervisor.conf /etc/supervisor/conf.d/heatseeknyc.conf
sudo supervisorctl reload
```

## (Optional) Direct Ethernet Connection to a Computer
**remove this when you're done, or things will misbehave**
```sh
emacs /Volumes/boot/cmdline.txt
# ip=169.254.169.254
```

# DigiMesh Firmware

## Cell
- **ID** = 311
- **D0** = 2
- **D9** = 1
- **D*** = 0
- **PR** = 80 *will use 0 for cell≥v0.4, where DIN/!CONFIG is grounded*
- **IR** = FFFF
- **SM** = 8

## Hub
- **ID** = 311
- **AP** = 1
- **SM** = 7
- **SO** = 1 *TODO change to zero, in case multiple hubs see each other?*
- **SP** = 1770 (1 minute) or 57E40 (1 hour)
