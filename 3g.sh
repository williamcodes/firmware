
while true; do
    echo 'unbinding USB...'
    echo '1-1' > /sys/bus/usb/drivers/usb/unbind
    sleep 5
    echo 'binding USB...'
    echo '1-1' > /sys/bus/usb/drivers/usb/bind
    sleep 15
    # command copied from usb_modeswitch startup log in debug mode:
    usb_modeswitch --no-inquire --verbose --sysmode \
                   --check-success 20 --configuration -1 \
                   --default-vendor 12d1 --default-product 1446 \
                   -c conf/usb_modeswitch.conf
    sleep 10

    wvdial
done
