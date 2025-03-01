import socket

localIP = "127.0.0.1"
localPort = 7501
sbuffer = 1024

msgFromServer = "hello this is stupid"
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

while(True):
    bytesAddPair = UDPServerSocket.recvfrom(sbuffer)
    message = bytesAddPair[0]
    address = bytesAddPair[1]
    clientMsg = "client msg:{}".format(message)
    clientIP = "client ip:{}".format(address)

    print(1)

    print(clientMsg)
    print(clientIP)

    UDPServerSocket.sendto(bytesToSend, address)