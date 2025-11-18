# Dockermc
Dockermc is a simple docker conatiner that runs a minecraft server as well as exposes a port from which you can write to and read from the server console.

## Usage
To run dockermc simply run `docker compose up`.

You can write your own program to interact with the server console or run
`./echo-input.sh | nc localhost 25500`

### Config
The minecraft server is exposed on port `25565`.

The console is exposed on port `25500`.

You can change which server the image downloads by changing `SERVER_DOWNLOAD_URL` in `compose.yml`

## Dev
### Server console
Using the console port is quite simple. Anything you write to the port is forwarded to the console. 
All output from the console, including all the output between the time the client was connected and when you connect is forwarded to the socket. 

### Volumes
Dockermc looks for volumes in 2 places:
`/config` and `/persistent-server-files` it will link any contents from those volumes to the directory the minecraft server is running in.

The server will populate the files/folders you link if they are empty. 
e.g. if you have an empty `server.properties` file in `/config` the server will write default properties to `server.properties` in the `/config` volume.
