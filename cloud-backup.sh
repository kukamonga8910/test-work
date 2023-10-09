#!/bin/bash
#sed -i "s/  'maintenance' => false,/  'maintenance' => true,/" /var/www/html/config/config.php
sudo -u apache php /var/www/html/occ maintenance:mode --on
#systemctl restart httpd
rsync -Aavx /var/www/html/ /home/mount/Backup/nextcloud_backup/nextcloud-dirbkp_`date +"%Y%m%d"`
mysqldump --single-transaction -u root -pNomer3403632393 nextcloud > /home/mount/Backup/nextcloud_db/nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
mysqldump --single-transaction --default-character-set=utf8mb4 -u root -pNomer3403632393 nextcloud > /home/mount/Backup/nextcloud_db/nextcloud-sqlbkp_UTF8_`date +"%Y%m%d"`.bak
find /home/mount/Backup/nextcloud_db/ -maxdepth 1 -type f -mtime +5 -delete
rsync -Aavx /home/data/ /home/mount/Backup/nextcloud_data_backup/nextcloud-data_`date +"%Y%m%d"`
tar -cvf httpd_`date +"%Y%m%d"`.tar.gz /etc/httpd/
mv /root/httpd_*.tar.gz /home/mount/Backup/httpd
find /home/mount/Backup/httpd/ -maxdepth 1 -type f -mtime +5 -delete
sudo -u apache php /var/www/html/occ maintenance:mode --off
#sed -i "s/  'maintenance' => true,/  'maintenance' => false,/" /var/www/html/config/config.php
#systemctl restart httpd
