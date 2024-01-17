#!/bin/bash

set -e

DBS=( $( mysql -e "SHOW DATABASES" | grep -vE '(Database|performance_schema|information_schema|sys|mysql)' ) )


for DB in "${DBS[@]}"; do 
	echo " - $DB"
done

read -p "Drop all dbs?" YN
case $YN in 
	y|Y|yes|Yes)
		for DB in "${DBS[@]}"; do
			mysql -e "DROP DATABASE $DB;"
			echo DROPPED $DB
		done
		;;
	*)
		echo No action taken
		;;
esac
