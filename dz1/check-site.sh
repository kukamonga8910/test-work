#!/bin/bash

# check if arguments have been entered

if [ "$#" -eq 0 ]; then
	echo "please enter the url to check the availability of the site"
	exit 0
fi


# site availability check function

function site_availability_check {

	for url in $@; do

		code=$(curl -L -s -o /dev/null -w "%{http_code}\n" $url)

		if [ "$code" -eq 200 ]; then

			echo -e "$url - site available"
		else
			echo -e "$url - site unavailable - Status Code: $code"
		fi
	done

}


# start function site availability check

site_availability_check "$@"
