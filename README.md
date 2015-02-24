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
- **SP** = 1 *thence 57A58 (59m50s)*
- **ST** = 2710 (10s)


# Raspberry π "Firmware" aka "Heat Seek OS"

## Overview
- connect XBee to GPIO serial pins directly
- device is /dev/ttyAMA0
- use `pyserial` library to communicate with XBee

## Basic Setup
```sh
bash setup.sh
```

## (Optional) Direct Ethernet Connection to a Computer
**remove this when you're done, or things will misbehave**
```sh
emacs /Volumes/boot/cmdline.txt
# ip=169.254.169.254
```
