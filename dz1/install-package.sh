#!/bin/bash

# empty argument check

if [ "$#" -eq 0 ]; then
        echo "Enter the packages you want to install"
        exit 0
fi

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


# Install Package Ubuntu

function install_package_ubuntu {

	for packages in $@; do

		echo -en "Install Package ${packages} - "
		
		if ! apt list --installed 2>/dev/null | grep -q "${packages}"; then
		
			apt install -y ${packages} > /dev/null 2>&1
			
			if [ "$?" -eq 0  ]; then

				VERSION_PACKAGE=$(apt show mariadb-server 2>/dev/null | grep "Version" | grep -oP '\d+\.\d+\.\d+-\d+|\d+\.\d+' | head -n 1)
				echo -e "${GREEN}DONE${COLOR_RESET}"
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

}

# Install Package AlmaLinux
function install_package_almalinux {

        for packages in $@; do

                echo -en "Install Package ${packages} - "

                if ! dnf list installed 2>/dev/null | grep -q "${packages}" ; then

                        dnf install -y ${packages} > /dev/null 2>&1

                        if [ "$?" -eq 0  ]; then

                                VERSION_PACKAGE=$(yum info $packages | grep "Version" | awk '{print $1":",$3}')
                                echo -e "${GREEN}DONE${COLOR_RESET}"
                                echo -e "\nDate Installed: $(date '+%Y-%m-%d %H:%M:%S')\nInstall Package: ${packages}\n${VERSION_PACKAGE}"  >> /var/log/auto_install.log
				echo "" >> /var/log/auto_install.log
                                                                                                               
                        else

                                echo -e "${RED}FAILED${COLOR_RESET}"
                                echo -e "-->> ${packages} <<--" >> /var/log/error_auto_install.log
                                echo "" >> /var/log/error_auto_install.log
                                dnf install -y ${packages} >> /var/log/error_auto_install.log 2>>/var/log/error_auto_install.log
                                echo "" >> /var/log/error_auto_install.log
                                echo "-->> END <<--" >> /var/log/error_auto_install.log
                                echo "" >> /var/log/error_auto_install.log
                        fi
                else
                        echo -e "${YELLOW}Package Installed${COLOR_RESET}"
                fi

        done

}



# operating system definition

if [ -f /etc/os-release ]; then
	. /etc/os-release
	case $ID in
		ubuntu)
			echo -e "operating system ${GREEN}detected${COLOR_RESET}: ${GREEN}${ID}${COLOR_RESET} - ${GREEN}${VERSION_ID}${COLOR_RESET}"
			install_package_ubuntu "$@"
			;;
		almalinux)
			echo -e "operating system ${GREEN}detected${COLOR_RESET}: ${GREEN}$ID${COLOR_RESET} - ${GREEN}$VERSION_ID${COLOR_RESET}"
			install_package_almalinux "$@"
			;;

		debian) 
			echo -e "operating system ${GREEN}detected${COLOR_RESET}: ${GREEN}${ID}${COLOR_RESET} - ${GREEN}${VERSION_ID}${COLOR_RESET}"
			install_package_ubuntu "$@"
			;;
		*)
			echo "Unknown operating system: $ID"
			;;
	esac
else
	echo "Unable to determine the operating system"
	exit 0
fi
