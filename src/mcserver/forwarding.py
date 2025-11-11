import os
import socket
import select 

#todo try catch in all sending and recving 
IN_FIFO_NAME = 'infifo'
OUT_FIFO_NAME = 'outfifo'
PORT = 25500

SERVER_SOCK = 'server_sock'
OUT_FIFO = 'out_fifo'
CLIENT_SOCK = 'client_sock'

CONNECTION_SUCCESS_MSG = int.to_bytes(1)
CONNECTION_BUSY_MSG = int.to_bytes(0)

MAX_CONTENT_BUFFER_LEN = 65536
content_buffer = bytearray()

def main():
    print('opening FIFOs (waiting for other side to be opened)')
    infifo: file = open(IN_FIFO_NAME, 'w')
    print("opened input FIFO")
    outfifo: file = open(OUT_FIFO_NAME, 'rb')
    setNonBlock(outfifo)
    print('successfuly opened FIFOs')

    serverSock: socket = createServerSocket(PORT)
    if not serverSock:
        return 1

    fileDescriptors = { SERVER_SOCK: serverSock, OUT_FIFO: outfifo }
    while True:
        ready = select.select(list(fileDescriptors.values()), [], list(fileDescriptors.values()))

        exceptional = ready[2]
        if fileDescriptors[OUT_FIFO]    in exceptional:
            print("Fifo broken. Shit's fucked")
        if fileDescriptors[SERVER_SOCK] in exceptional:
            print("Server socket broken?")
        clientConnected = CLIENT_SOCK in fileDescriptors
        if clientConnected and fileDescriptors[CLIENT_SOCK] in exceptional:
            disconnectClient(fileDescriptors)

        readable = ready[0]
        #read from client
        clientConnected = CLIENT_SOCK in fileDescriptors
        clientReady = clientConnected and fileDescriptors[CLIENT_SOCK] in readable
        if clientReady:
            content = fileDescriptors[CLIENT_SOCK].recv(1024) 
            if not content:
                disconnectClient(fileDescriptors)
            else:
                infifo.write(bytes.decode(content, 'utf8'))
                infifo.flush()
        clientConnected = CLIENT_SOCK in fileDescriptors


        #new conn
        newConnection = fileDescriptors[SERVER_SOCK] in readable
        if newConnection:
            newClientSock = fileDescriptors[SERVER_SOCK].accept()[0]
            if not clientConnected:
                setNonBlock(newClientSock)
                fileDescriptors[CLIENT_SOCK] = newClientSock
                newClientSock.send(CONNECTION_SUCCESS_MSG)
                writeBufferedDataToClient(fileDescriptors) 
            else:
                newClientSock.send(CONNECTION_BUSY_MSG)
                newClientSock.close()
        clientConnected = CLIENT_SOCK in fileDescriptors

        fifoReady = fileDescriptors[OUT_FIFO] in readable
        #read from fifo
        if fifoReady:
            global content_buffer
            content = outfifo.read()
            print(content.decode('utf-8'), end='')
            content_buffer.extend(content)
            if(CLIENT_SOCK in fileDescriptors):
                writeBufferedDataToClient(fileDescriptors) 
                
            if len(content_buffer) > MAX_CONTENT_BUFFER_LEN:
                content_buffer = bytearray()

def disconnectClient(fileDescriptors):
    clientSock = fileDescriptors[CLIENT_SOCK].close()
    fileDescriptors.pop(CLIENT_SOCK)
    console.log("Client disconnected")

def writeBufferedDataToClient(fileDescriptors):
    global content_buffer
    isSuccess = True
    try:
        fileDescriptors[CLIENT_SOCK].send(content_buffer)
        content_buffer = bytearray()
    except:
        disconnectClient(fileDescriptors)
        isSuccess = False

    return isSuccess

def setNonBlock(file):
    os.set_blocking(file.fileno(), False)

def createServerSocket(port): 
    try:
        return socket.create_server(("", port)) 
    except Exception as e:
        print("VERY BAD: failed to bind to port {}".format(port))
        return None


main()
