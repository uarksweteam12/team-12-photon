import socket

UDP_IP = "127.0.0.1" 
UDP_PORT = 7500

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
buffer = 1024
sock.bind(("127.0.0.1", 7501))


#serverAddressPort   = ("127.0.0.1", 7500)
#serverSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#serverSock.bind(serverAddressPort)

_actionScreen = None

def setActionScreen(screenInstance):
    global _actionScreen
    _actionScreen = screenInstance

def startGame():
    msg = "202"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("STARTING GAME")
    # send start game signal to UDP server
    gameOnline = True
    while gameOnline:
        #receivedData, address = serverSock.recvfrom(buffer)
        #receivedData = receivedData.decode('utf-8')
        print("LISTENING...")
        msgFromServer = sock.recvfrom(buffer)
        msg = "Message from Server {}".format(msgFromServer[0])
        data = msgFromServer[0].decode('utf-8')
        splitThemUp = data.split(":")

        if data != "221": #need to find another way...
            sock.sendto(splitThemUp[0].encode(), (UDP_IP, UDP_PORT))
            _actionScreen.top.after(0, lambda: (_actionScreen.redScores[str(0)][0].set(300), _actionScreen.top.update_idletasks(), _actionScreen.top.update()))
        else:
            gameOnline = False #ends game loop
        print(f'client received: {msg}')



def endGame():
    msg = "221"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("ENDING GAME")
    # send end game signal

def send_equipment_code(hardwareid) -> bool:
    """
    Sends a player's ID, codename, and team to the UDP server
    """

    message = f"{hardwareid}" # We can change this later if we want

    try:
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent: {message} to {UDP_IP}:{UDP_PORT}") # Same here
        return True

    except Exception as e:
        print(f"Error sending UDP packet: {e}")
        return False

def set_server_ip(newip):
    """
    Sets UDP_IP to newip only if in correct format
    """
    global UDP_IP
    UDP_IP = newip



    




