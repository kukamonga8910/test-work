#!/bin/bash

# check root

if [ $(id -u) -ne 0  ]; then
	echo "run the script with root privileges"
	exit 0
fi

# COLOR

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
COLOR_RESET='\033[0m'

function install_app {

	local array=("$@")

	for packages in "${array[@]}"; do

		echo -en "Install Package ${packages} - "
		
		if ! apt list --installed 2>/dev/null | grep -q "${packages}"; then
		
			apt install -y "$packages" > /dev/null 2>&1
			
			if [ "$?" -eq 0  ]; then

				VERSION_PACKAGE=$(apt show "${packages}"  2>&1 | grep "Version" | grep -oP '\d+\.\d+\.\d+-\d+|\d+\.\d+' | head -n 1)

				if [[ "$VERSION_PACKAGE" == "" ]]; then

					echo -e "${GREEN}DONE${COLOR_RESET}"

				else

					echo -e "${GREEN}DONE - VERSION: ${VERSION_PACKAGE}${COLOR_RESET}"

				fi
				echo -e "\nDate Installed: $(date '+%Y-%m-%d %H:%M:%S')\nInstall Package: ${packages}\n${VERSION_PACKAGE}"  >> /var/log/auto_install.log
				echo "" >> /var/log/auto_install.log
        
			else

				echo -e "${RED}FAILED${COLOR_RESET}"
				echo -e "-->> ${packages} <<--" >> /var/log/error_auto_install.log
				echo "" >> /var/log/error_auto_install.log
				apt-get install -y ${packages} >> /var/log/error_auto_install.log 2>>/var/log/error_auto_install.log
				echo "" >> /var/log/error_auto_install.log
				echo "-->> END <<--" >> /var/log/error_auto_install.log
				echo "" >> /var/log/error_auto_install.log
			fi
		else
			echo -e "${YELLOW}Package Installed${COLOR_RESET}"
		fi

	done

	rsync -avz simple_app linux_app /var/www/ > /dev/null

	if [ -f  /etc/nginx/sites-enabled/default ]; then

		rm /etc/nginx/sites-enabled/default
	fi

	chown -R www-data:www-data /var/www/simple_app /var/www/linux_app
	cp simple_app/simple_app.conf /etc/nginx/sites-available/simple_app.conf
	cp linux_app/conf/app.conf /etc/nginx/sites-available/linux_app.conf
	ln -s /etc/nginx/sites-available/simple_app.conf /etc/nginx/sites-available/linux_app.conf /etc/nginx/sites-enabled/
	mysql < simple_data.sql
	mysql < init_db.sql
	nginx -t > /dev/null

	if [ "$?" -eq 0  ]; then

		nginx -s reload > /dev/null
	else
		echo "NGINX ERROR READ LOG"
		exit 0
	fi
}

array_app=(nginx php8.3-fpm php8.3-mysql php8.3-gd mariadb-server)

install_app "${array_app[@]}"
