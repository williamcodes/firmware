if [ "$PWD" != "/home/pi/firmware" ]
then echo This file must be located in /home/pi/firmware
     exit
fi

read -p "Have you already run raspi-config? [yN]" yn
if [ "$yn" != "y" ]
then read -p $'Configure options 1, 2, 4 > Locale, 4 > Change Timezone, and 8 > Serial > Off.\nPress enter to begin.'
     sudo raspi-config
     sudo reboot
     exit
fi

set -ex

awk '/^Serial\t/ { print $3 }' /proc/cpuinfo | sudo tee /etc/hostname
sudo sed -i "s/raspberrypi/$(cat /etc/hostname)/" /etc/hosts
sudo /etc/init.d/hostname.sh

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install usb-modeswitch wvdial supervisor python3-pip vnstat screen

sudo pip-3.2 install -Ur requirements.txt

cat conf/relay_rsa.pub >> ~/.ssh/authorized_keys

sudo ssh-keygen
sudo ssh-copy-id hubs@relay.heatseeknyc.com

sudo ln -sf $PWD/conf/wvdial.conf /etc/
sudo sed -i 's/^usepeerdns/# usepeerdns/' /etc/ppp/peers/wvdial
sudo tee /etc/resolv.conf << EOF
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
sudo chattr +i /etc/resolv.conf

sudo ln -s $PWD/conf/supervisor.conf /etc/supervisor/conf.d/heatseeknyc.conf
sudo supervisorctl reload
