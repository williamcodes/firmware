# How to set up a hub from scratch

## Ingredients
- Raspberry π
- XBee
- Heat Seek hub board (allows you to connect the XBee to the π)
- SD card
- SD card adapter (lets you put the SD card into a computer to copy Raspbian to it)
- USB-to-Ethernet adapter. [This one](http://www.amazon.com/Cable-Matters%C2%AE-SuperSpeed-Gigabit-Ethernet/dp/B00BBD7NFU) works. Others, including a Gigaware one I tried, may not.

## Steps
1. Download the [latest Raspbian](http://downloads.raspberrypi.org/raspbian_latest)
1. Extract the .zip archive to get the .img file.
1. Copy it to the SD card. On a Mac, you do `diskutil list` to see which device is the SD card (for me it's always `/dev/disk2`, then `diskutil unmountDisk /dev/disk2` (or whatever device yours is), and finally `sudo dd bs=1m if=2015-05-05-raspbian-wheezy.img of=/dev/disk2` (or whatever Raspbian and disk you have). The final command takes about half an hour.
1. Eject the SD card, with Command+E in the Finder.
1. Put the SD card in the π, connect the USB-to-ethernet adapter from the π to your router, and plug in the π!
1. On a computer, try `ssh pi@raspberrypi.local`. If that doesn't work, run `nmap -p 22 --open 192.168.1.0/24` (with whatever your router's IP address range is) to find the ip address, and then run `ssh pi@192.168.1.108` (with the IP address you found). The password is 'raspberry'.
1. Now you're on the π! Run `git clone https://github.com/heatseeknyc/firmware.git && cd firmware && bash setup.sh`
1. The setup script will ask you to configure the π, which involves changing the password, setting up the timezone and keyboard layout, et cetera… It will then reboot and you should run `cd firmware && bash setup.sh` again, to finish the setup.

## (Optional) Direct Ethernet Connection to a Computer
If you can't connect to a router, or something running a DHCP server, then you may need to use a fixed IP address:
**remove this when you're done, or things will misbehave**
On your Mac, with the SD card inserted, edit /Volumes/boot/cmdline.txt to set `ip=169.254.169.254`


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
