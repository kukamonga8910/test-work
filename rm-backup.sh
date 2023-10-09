#!/bin/bash

array_dirname=()
array_dirdate=()
array_data_dirname=()
array_data_dirdate=()
dirname=$( ls -d /home/mount/Backup/nextcloud_backup/* | cut -d'/' -f6 )
dirdate=$( ls -d /home/mount/Backup/nextcloud_backup/* | cut -d'_' -f3 )
dirname_data=$( ls -d /home/mount/Backup/Nextcloud_data_backup/* | cut -d'/' -f6 )
dirdate_data=$( ls -d /home/mount/Backup/Nextcloud_data_backup/* | cut -d'_' -f4 )
date=$( date +%Y%m%d  )
mapfile -t array_dirname <<< "$dirname"
mapfile -t array_dirdate <<< "$dirdate"
mapfile -t array_data_dirname <<< "$dirname_data"
mapfile -t array_data_dirdate <<< "$dirdate_data"
echo "-------------------------------------$( date  )----------------------------------" >> /home/rm-backup.sh.log
echo "" >> /home/rm-backup.sh.log
echo "Nextcloud_Backup" >> /home/rm-backup.sh.log
echo "" >> /home/rm-backup.sh.log
for (( i=0; i<${#array_dirname[@]} && i<${#array_dirdate[@]};  i++  )); do
	nomber_day="$(( $date - ${array_dirdate[$i]}  ))"
	if (( $nomber_day >= 4 )); then
		find /home/mount/Backup/nextcloud_backup/ -maxdepth 1 -name *${array_dirdate[$i]} -type d -exec rm -rf {} \;
		echo "За сегодня Были удалены бэкапы - ${array_dirname[$i]}" >> /home/rm-backup.sh.log
#		echo "" >> /home/rm-backup.sh.log
	else
		echo "Актуальные бекапы - ${array_dirname[$i]}" >> /home/rm-backup.sh.log
	fi
done

echo "" >> /home/rm-backup.sh.log
echo "Nextcloud_Backup_DATA" >> /home/rm-backup.sh.log
echo "" >> /home/rm-backup.sh.log
for (( i=0; i<${#array_data_dirname[@]} && i<${#array_data_dirdate[@]}; i++  )); do
	nomber_day_data="$(( $date - ${array_data_dirdate[$i]}  ))"
	if (( $nomber_day_data >= 4 )); then
		find /home/mount/Backup/Nextcloud_data_backup/ -maxdepth 1 -name *${array_data_dirdate[$i]} -type d -exec rm -rf {} \;
		echo "За сегодня Были удалены бэкапы - ${array_data_dirname[$i]}" >> /home/rm-backup.sh.log
#		echo "" >> /home/rm-backup.sh.log
	else
		echo "Актуальные бекапы - ${array_data_dirname[$i]}" >> /home/rm-backup.sh.log
	
	fi

done

echo "" >> /home/rm-backup.sh.log
echo "---------------------------------------------------------------------------------------------------" >> /home/rm-backup.sh.log
echo "" >> /home/rm-backup.sh.log
