#!/bin/bash

# check root

if [ $(id -u) -ne 0  ]; then
        echo "run the script with root privileges"
        exit 0
fi

# array of services to be monitored

services=("nginx" "mariadb")

# check if the service is running

for service in ${services[@]}; do

	# check the service status if the service is running, print a message if not, try to start the service

	if systemctl is-active --quiet "$service"; then

		echo -e "service $service: is running"
	else

		echo -e "service $service: stopped attempting to start"

		systemctl restart $service

		# check if the service has started after restart

	        if systemctl is-active --quiet "$service"; then

	                echo -e "service $service: restarted successfully"
	        else

        	        echo -e "service $service: could not be restarted"

	        fi
	fi

done
