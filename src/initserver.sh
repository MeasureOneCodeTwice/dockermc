#!/bin/bash
if [[ ! -f server.jar ]]; then
       wget $(printenv SERVER_DOWNLOAD_URL) -O server.jar
fi

#this creates all the files and then exits because eula isn't accepted
if [[ ! -f eula.txt ]]; then
       java -jar server.jar
fi

sed -i 's/eula=false/eula=true/' eula.txt
