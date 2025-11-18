#!/bin/bash
#don't try to set things up after /server exists (happens after conatiner restart)
echo "testinwg"
if [[ ! -d  /server ]]; then
	mkdir /server

	#copy config and persistent server files
	dirsToLink=(/config /persistent-server-files /scripts)
	for path in ${dirsToLink[@]}; do
		if [[ -d $path ]]; then
			ln -s $path/* /server
		fi
	done
fi



cd /server
/server/runserver.sh
