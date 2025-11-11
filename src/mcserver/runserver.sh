#!/bin/bash
./initserver.sh
java -Xmx1024M -Xms1024M -jar server.jar nogui
return 1
