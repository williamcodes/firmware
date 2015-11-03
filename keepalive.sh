
while true; do
    if ! ping -c 1 relay.heatseeknyc.com; then
        if ! ping -c 1 google.com; then
            if (( ++failures >= 1000 )); then  # every 17 hours
                echo "$failures failures, rebooting."
                shutdown -r now
            elif (( ++failures % 10  == 0 )); then  # every 10 minutes
                echo "$failures failures, killing wvdial."
                killall wvdial
