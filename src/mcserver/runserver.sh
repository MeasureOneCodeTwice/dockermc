#!/bin/bash
./initserver.sh
python3 setupFIFOs.py
if [ ! $? -eq 0 ]; then 
	exit 1
fi
python3 forwarding.py & 
cat infifo | java -Xmx1024M -Xms1024M -jar server.jar nogui > outfifo
kill %%
exit 1
