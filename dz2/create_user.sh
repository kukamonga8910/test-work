#!/bin/bash

USERNAME="$1"
GROUP_ADD="$2"
SHELLS="$3"
UIDS="$4"


if [ $(id -u) -ne 0  ]; then
        echo "run the script with root privileges"
        exit 0
fi

if id "$USERNAME" &>/dev/null; then

	echo "user has already been created"
	exit 0
fi


if [ -z "$SHELLS" ]; then

	SHELLS=/bin/bash
fi

if [ -n "$USERNAME" ]; then

	if [ -z "$UIDS" ]; then

		useradd -m -s "$SHELLS" "$USERNAME"
	else
		useradd -m -s "$SHELLS" -u "$UIDS" "$USERNAME"
	fi
fi

if [ -n "$GROUP_ADD" ]; then

	if getent group "$GROUP_ADD" &>/dev/null; then

		usermod -aG "$GROUP_ADD" "$USERNAME"
	else
		echo "There's no such group."
	fi
else
	echo "unspecified group"

fi

PASSWORD=$(openssl rand -base64 12 | head -c 8)
echo "$USERNAME":"$PASSWORD" | chpasswd

echo -e "$0: created user $USERNAME with id $(id $USERNAME | awk -F'[=()]' '{print $2}') and groups $GROUP_ADD password: $PASSWORD" > /var/log/create_user.log
