
while true; do
    if ! ping -c 1 relay.heatseeknyc.com; then
        if ! ping -c 1 google.com; then
            if (( ++failures >= 10 )); then
                echo "$failures failures, killing wvdial."
                failures=0  # wait 10 minutes until we try again
                killall wvdial
            fi
        fi
    else
        failures=0  # all is well
    fi
    sleep 60
done
