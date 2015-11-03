
    echo This file must be located in /home/pi/firmware
    exit
fi
git checkout master  # don't use dev branch in production

read -p "Have you already run raspi-config? [yN]" yn if [ "$yn" != "y" ]; then
read -p $'Configure options 2, 4 > Locale, 4 > Change Timezone, and 8 > Serial
> No.\nDo not do option 1.\nPress enter to begin.' sudo raspi-config sudo
reboot exit fi

set -ex

sudo apt-get update
sudo apt-get -y install usb-modeswitch wvdial supervisor python3-pip vnstat

# TODO this doesn't work during setup without a modem
# sudo vnstat -u -i ppp0  # start vnstat listening on ppp0 database

sudo pip-3.2 install -Ur requirements.txt

# TODO set up heatseeknyc.db using schema.sql, either by installing sqlite3 command or via python

mkdir -p ~/.ssh
