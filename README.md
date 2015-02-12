# DigiMesh Firmware

## Cell
- **D0** = 2
- **D5** = 0
- **D7** = 0
- **D8** = 0
- **P0** = 0
- **PR** = 80 *TODO in the future we'll use 0 for cell≥v0.4, when DIN/!CONFIG is grounded*
- **IR** = FFFF
- **SM** = 8

## Hub
- **AP** = 1
- **SM** = 7
- **SO** = 1
- **SP** = 1 *thence 57C4C (59m55s)*
- **ST** = 1388 (5s) *(note default is 7D0 = 2s)*


# Raspberry π "Firmware" aka "Heat Seek OS"

## Overview
- connect XBee to GPIO serial pins directly
- device is /dev/ttyAMA0
- use `pyserial` library to communicate with XBee

## Basic Setup
```sh
sudo raspi-config
# 1, 2, 4 > Locale, reboot
sudo raspi-config
# 4 > Change Timezone, 8 > Serial > Off, reboot

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install usb-modeswitch wvdial supervisor python3-pip vnstat

git clone https://github.com/heatseeknyc/firmware.git
cd firmware

sudo pip-3.2 install -Ur requirements.txt

sudo ssh-keygen
sudo ssh-copy-id hubs@hubs.heatseeknyc.com

sudo ln -sf $PWD/conf/wvdial.conf /etc/
sudo nano /etc/ppp/peers/wvdial
# # usepeerdns
sudo nano /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 8.8.4.4
sudo chattr +i /etc/resolv.conf

sudo ln -s $PWD/conf/supervisor.conf /etc/supervisor/conf.d/heatseeknyc.conf
sudo supervisorctl reload
```

## (Optional) Direct Ethernet Connection to a Computer
**remove this when you're done, or things will misbehave**
```sh
emacs /Volumes/boot/cmdline.txt
# ip=169.254.169.254
```
