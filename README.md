# Installing ("flashing") firmware

## Raspberry π ("Heat Seek OS")
1. Place `heatseekos.img` on your Desktop _TODO put it in Google Drive_
1. Insert an SD card into your computer or a USB card reader, potentially with an adapter to make it fit.
1. Once you see the disk appear in Finder, go to Terminal.
1. Run `diskutil unmountDisk /dev/disk2`
1. Run `sudo dd bs=1m if=$HOME/Desktop/heatseekos.img of=/dev/disk2 && say "Done flashing SD card."`
