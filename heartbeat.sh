
while [ "$xbee_id" == "" ]; do
    python3 -m hub.reset_xbee_id  # note this clears any previous id, in case the xbee was changed
    echo 'waiting for xbee id to appear in db...'
    sleep 10
    xbee_id=$(python3 -m hub.get_xbee_id)
done
echo "xbee id is $xbee_id"

pi_id=$(awk '/^Serial\t/ { print $3 }' /proc/cpuinfo)
echo "π id is $pi_id"

while true; do
    for _ in $(seq 10); do  # watch for new tunnel port every minute for up to 10 minutes
        port=$(supervisorctl tail ssh | awk '/^Allocated port / { print $3 }' | tail -1)
	if [ "$port" != "$old_port" ]; then
            echo "port changed to $port from $old_port"
	    break
	fi
	sleep 60
    done

    # TODO also send $(vnstat -i ppp0 --oneline)

    # port has changed or 10 minutes have passed, so time to send a heartbeat:
    # TODO this should be a PUT or PATCH to /hubs/$xbee_id
    data="hub=$xbee_id&pi=$pi_id&port=$port"
    echo "posting $data"
    if curl -sS -d "$data" http://relay.heatseeknyc.com/hubs; then
        echo  # server response often has no newline
	old_port="$port"
    else
	echo 'failed to post. waiting to retry...'
        sleep 60
    fi
done
