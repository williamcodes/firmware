
while [ "$XBEE_ID" == "" ]
do
    # note this clears any previous id, in case the xbee was changed:
    python3 -m hub.reset_xbee_id
    echo "waiting for xbee id to appear in db..."
    sleep 10
    XBEE_ID=$(python3 -m hub.get_xbee_id)
done
echo "xbee id is $XBEE_ID"

PI_ID=$(awk '/^Serial\t/ { print $3 }' /proc/cpuinfo)

PORT=""
while true
do
    for _ in $(seq 10)  # watch for new tunnel port every minute for up to 10 minutes
    do
        NEWPORT=$(supervisorctl tail ssh | awk '/^Allocated port / { print $3 }' | tail -1)
	if [ "$NEWPORT" != "$PORT" ]
	then
            echo "port changed from $PORT to $NEWPORT"
	    break
	fi
	sleep 60
    done

    # TODO also send $(vnstat -i ppp0 --oneline)

    # port has changed or 10 minutes have passed, so time to send a heartbeat:
    # TODO this should be a PUT or PATCH to /hubs/$XBEE_ID
    echo "posting hub=$XBEE_ID&pi=$PI_ID&port=$NEWPORT..."
    if curl -sS -d "hub=$XBEE_ID" -d "pi=$PI_ID" -d "port=$NEWPORT" http://relay.heatseeknyc.com/hubs
    then
        echo # server response often has no newline
	PORT="$NEWPORT"
    else
	echo "failed to post."
    fi

    sleep 60
done
