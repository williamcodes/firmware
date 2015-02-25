PI_ID=$(awk '/^Serial\t/ { print $3 }' /proc/cpuinfo)

# TODO query local xbee MAC via serial
# TODO vnstat -i ppp0 --oneline

PORT=""
while true
do
    # check if our tunnel port has changed, once a minute for up to 10 minutes:
    for _ in $(seq 10)
    do NEWPORT=$(supervisorctl tail ssh stderr | awk '/^Allocated port / { print $3 }' | tail -1)
	if [ "$NEWPORT" != "$PORT" ]
	then break
	fi
	sleep 60
    done

    # port has changed or 10 minutes have passed, so time to send a heartbeat:
    if curl -sS -d "hub=$PI_ID" -d "port=$NEWPORT" http://relay.heatseeknyc.com/hubs
    then PORT="$NEWPORT"
    elif ! ping -c 1 google.com
    then # internet is down :'(
	supervisorctl stop wvdial
	killall wvdial
	usb_modeswitch -I -W -D -s 20 -u -1 -v 12d1 -p 1446 -c conf/usb_modeswitch.conf
	sleep 1
	supervisorctl start wvdial
    fi

    sleep 1
done
