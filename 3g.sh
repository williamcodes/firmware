
while true
do
    usb_modeswitch -I -W -D -s 20 -u -1 -v 12d1 -p 1446 -c conf/usb_modeswitch.conf
    wvdial
    sleep 1
done
