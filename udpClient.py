import socket

UDP_IP = "127.0.0.1" 
UDP_PORT = 7500

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
buffer = 1024
sock.bind(("127.0.0.1", 7501))
sock.setblocking(False)  # Make socket non-blocking

_actionScreen = None
_gameOnline = False  # internal flag to stop polling when game ends

def setActionScreen(screenInstance):
    global _actionScreen
    _actionScreen = screenInstance

def startGame():
    global _gameOnline
    msg = "202"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("STARTING GAME")
    _gameOnline = True
    if _actionScreen:
        _actionScreen.top.after(100, poll_udp_socket)

def poll_udp_socket():
    global _gameOnline

    if not _gameOnline or not _actionScreen or not _actionScreen.top.winfo_exists():
        return

    try:
        msgFromServer = sock.recvfrom(buffer)
        data = msgFromServer[0].decode('utf-8')
        splitThemUp = data.split(":")

        print(f"Client received: {data}")

        if data == "221":
            endGame()
            return  # Stop polling
        else:
            sock.sendto(splitThemUp[0].encode(), (UDP_IP, UDP_PORT))

            if _actionScreen is not None:
                print("test")
                _actionScreen.top.after(10, updateUI(splitThemUp[0], splitThemUp[1]))

    except BlockingIOError:
        # No data to receive, continue polling
        pass

    # Schedule next check
    _actionScreen.top.after(100, poll_udp_socket)

def updateUI(player1, player2):
    print('in update UI')
    if _actionScreen:
        if player2 == "53": # red base
            pass
        elif player2 == "43": #green base
            pass
        else: #player hit player
            playerID = None
            red = False
            found = False
            for playerId, playerData in _actionScreen.redPlayers.items():
                if playerData[2].get() == player1:  # Check if the hardwareId matches
                    playerID = playerId  # Found the player in the red team
                    found = True
                    red = True
                    print(f'red id: {playerID}')
                    break
            
            if not found:
                for playerId, playerData in _actionScreen.greenPlayers.items():
                    if playerData[2].get() == player1:  # Check if the hardwareId matches
                        playerID = playerId  # Found the player in the red team
                        found = True
                        print(f'green id: {playerID}')
                        break

            #find which team
            if red: #player who shot in redPlayers
                print('shooter is red player')
                updateScore(player1, player2, False, 10)
            else: #greenPlayer shot redPlayer
                print('shooter is green')
                updateScore(player1, player2, True, 10)


        _actionScreen.redScores[str(0)][0].set(300)
        _actionScreen.top.update_idletasks()

def findPlayerByHardwareId(self, hardwareId):
    # Check redPlayers first
    for playerId, playerData in self.redPlayers.items():
        if playerData[2].get() == hardwareId:  # Check if the hardwareId matches
            return "Red Team", playerId  # Found the player in the red team
    
    # Check greenPlayers
    for playerId, playerData in self.greenPlayers.items():
        if playerData[2].get() == hardwareId:  # Check if the hardwareId matches
            return "Green Team", playerId  # Found the player in the green team

def updateScore(player1, player2, teamBool, points): #teamBool = False, red : teamBool = True, green
    pass

def endGame():
    global _gameOnline
    _gameOnline = False
    msg = "221"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("ENDING GAME")

def send_equipment_code(hardwareid) -> bool:
    message = f"{hardwareid}"
    try:
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent: {message} to {UDP_IP}:{UDP_PORT}")
        return True
    except Exception as e:
        print(f"Error sending UDP packet: {e}")
        return False

def set_server_ip(newip):
    global UDP_IP
    UDP_IP = newip
