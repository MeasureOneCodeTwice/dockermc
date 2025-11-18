#!/bin/bash

#don't try to set things up after /server exists (happens after conatiner restart)
if [[ -d  /server ]]; then
	cd /server
	/server/runserver.sh
	exit 1
fi 


mkdir /server


if [[ "$POPULATE_VOLUMES" = true ]]; then 
	echo "Populating volumes"
	if [[ ! -d /persistent-server-files/world ]]; then
		mkdir /persistent-server-files/world 
	fi
	if [[ ! -d /persistent-server-files/mods ]]; then
		mkdir /persistent-server-files/mods
	fi
	touch persistent-server-files/whitelist.json
	touch persistent-server-files/ops.json
	touch persistent-server-files/banned-players.json
	touch persistent-server-files/banned-ips.json

	touch config/server.properties
fi

#copy config and persistent server files
dirsToLink=(/config /persistent-server-files /scripts)
for path in ${dirsToLink[@]}; do
	if [[ -d $path ]]; then
		ln -s $path/* /server
	fi
done

cd /server
/server/runserver.sh
exit 1
