
PI_ID=$(python3 -m hub.get_pi_id)

# TODO vnstat -i ppp0 --oneline

function get_xbee_id {
    # query SH and SL. receiver.py should receive the response and write to db:
    # (thus note that even if id is already in db, this refreshes it)
    python3 -m hub.request_xbee_id
    sleep 6
    XBEE_ID=$(python3 -m hub.get_xbee_id)
}

get_xbee_id

PORT=""
FAILURES=0
while true
do
    for _ in $(seq 10)  # watch for new tunnel port every minute for up to 10 minutes
    do
        I=0
        while [ "$XBEE_ID" == "" ]  # try to read XBee ID every 6 seconds for up to a minute
        do
            get_xbee_id
            [ $((++I)) -gt 10 ] && break
        done

        NEWPORT=$(supervisorctl tail ssh | awk '/^Allocated port / { print $3 }' | tail -1)
	if [ "$NEWPORT" != "$PORT" ]
	then echo "port changed from $PORT to $NEWPORT"
	     break
	fi
	sleep 60
    done

    # port has changed or 10 minutes have passed, so time to send a heartbeat:
    echo "posting hub=$PI_ID&xbee=$XBEE_ID&port=$NEWPORT..."
    if curl -sS -d "hub=$PI_ID" -d "xbee=$XBEE_ID" -d "port=$NEWPORT" http://relay.heatseeknyc.com/hubs
    then echo # server response often has no newline
	PORT="$NEWPORT"
	FAILURES=0
    elif ! ping -c 1 google.com
    then # internet is down :'(
	echo "$((++FAILURES)) failures in a row!"
	if [ $FAILURES -ge 36 ] # 6*6*10 minutes = 6 hours
	then # give up and try rebooting...
	    reboot
	    exit
	fi
    fi

    sleep 60
done
