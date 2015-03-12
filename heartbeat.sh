PI_ID=$(awk '/^Serial\t/ { print $3 }' /proc/cpuinfo)

# TODO query local xbee MAC via serial
# TODO vnstat -i ppp0 --oneline

PORT=""
FAILURES=0
while true
do
    # check if our tunnel port has changed, once a minute for up to 10 minutes:
    for _ in $(seq 10)
    do NEWPORT=$(supervisorctl tail ssh | awk '/^Allocated port / { print $3 }' | tail -1)
	if [ "$NEWPORT" != "$PORT" ]
	then echo "port changed from $PORT to $NEWPORT"
	     break
	fi
	sleep 60
    done

    # port has changed or 10 minutes have passed, so time to send a heartbeat:
    echo "posting hub=$PI_ID&port=$NEWPORT..."
    if curl -sS -d "hub=$PI_ID" -d "port=$NEWPORT" http://relay.heatseeknyc.com/hubs
    then echo # server response often has no newline
	PORT="$NEWPORT"
	FAILURES=0
    elif ! ping -c 1 google.com
    then # internet is down :'(
	echo "$((++FAILURES)) failures in a row!"
	if [ $FAILURES -lt 36 ] # 6*6*10 minutes = 6 hours
	then # try to fix it
	    supervisorctl stop wvdial
	    killall wvdial
	    usb_modeswitch -I -W -D -s 20 -u -1 -v 12d1 -p 1446 -c conf/usb_modeswitch.conf
	    sleep 5
	    supervisorctl start wvdial
	else # give up and try rebooting...
	    reboot
	    exit
	fi
    fi

    sleep 60
done
