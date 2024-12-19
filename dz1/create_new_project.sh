#!/bin/bash

# check if arguments have been entered

if [ "$#" -eq 0 ]; then

	echo "enter a project name"
	exit 0 

fi

# check root

if [ $(id -u) -ne 0  ]; then
        echo "run the script with root privileges"
        exit 0
fi

# create new project

function create_new_project {

	for name_project in $@; do

		path="/opt/$name_project"

		if [ -d "$path" ]; then

			echo "catalog already exists"

		else

			mkdir -p /opt/$name_project/{src,docs,tests,resources}
			echo -e "src/: исходный код\ndocs/: документация\ntests/: тесты\nresources/: ресурсы проекта" > /opt/$name_project/readme.md
			tree -l /opt/$name_project
		fi

	done


}

# Start function create new project

create_new_project "$@"

