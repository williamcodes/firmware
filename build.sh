if [ "$PWD" != "/home/pi/firmware" ]; then
    echo This file must be located in /home/pi/firmware
    exit
fi

read -p "Have you already run raspi-config? [yN]" yn
if [ "$yn" != "y" ]; then
    read -p $'Configure options 1, 2, 4 > Locale, 4 > Change Timezone, and 8 > Serial > Off.\nPress enter to begin.'
    sudo raspi-config
    sudo reboot
    exit
fi

set -ex

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install usb-modeswitch wvdial supervisor python3-pip vnstat screen

sudo vnstat -u -i ppp0  # start vnstat listening on ppp0 database

sudo pip-3.2 install -Ur requirements.txt

mkdir -p ~/.ssh
cat conf/relay_rsa.pub >> ~/.ssh/authorized_keys

sudo ssh-keygen  # TODO how to statically build this in to Heat Seek OS without compromising relay server?
sudo ssh-copy-id hubs@relay.heatseeknyc.com

sudo ln -sf $PWD/conf/wvdial.conf /etc/
sudo sed -i 's/^usepeerdns/# usepeerdns/' /etc/ppp/peers/wvdial
sudo tee /etc/resolv.conf << EOF
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
sudo chattr +i /etc/resolv.conf

sudo ln -s $PWD/conf/supervisor.conf /etc/supervisor/conf.d/heatseeknyc.conf