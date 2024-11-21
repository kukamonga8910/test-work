
#!/bin/bash

# directory path

path_backup="/opt/backups"

# data db

db_name="test_db"
db_user="root"
db_password="QAZqaz123"

# check root

if [ $(id -u) -ne 0  ]; then
        echo "run the script with root privileges"
        exit 0
fi

# directory check

if [ -d "$path_backup" ]; then

	echo "directory found"

else
	mkdir "$path_backup"
	echo "directory created"

fi

#backup OS

tar -cvpzf "$path_backup"/backup_$(date +\%d-\%m-\%Y_\%H-\%M-\%S).tar.gz \
	--exclude="$path_backup" \
	--exclude="/proc" \
	--exclude="/mnt" \
	--exclude="/run" \
	--exclude="/dev" \
	--exclude="/sys" \
	--exclude="/lost+found" \
	--exclude="/boot" \
	--exclude="/tmp" --one-file-system / > "$path_backup"/backup_system.log

# check backup OS

if [ "$?" -eq 0 ]; then

	echo "Backup OS Created"
else
	echo "something went wrong. Look at the log. /opt/backups/backup_system.log"
fi

# backup DB

sudo mysqldump -u "$db_user" -p"$db_password" "$db_name" | sudo tee "$path_backup"/test_db_backup_$(date +\%d-\%m-\%Y_\%H-\%M-\%S).sql > /dev/null

# check backup DB

if [ "$?" -eq 0 ]; then

        echo "Backup DB Created"
else
        echo "something went wrong. Look at the log. /opt/backups/backup_db.log"
fi

# deleting backups older than 3 days
find "$path_backup" -type f -name "*.tar.gz" -mtime +3 -exec rm {} \;


