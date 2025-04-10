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
                _actionScreen.top.after(10, lambda: updateUI(splitThemUp[0], splitThemUp[1]))

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
            shooterID = None
            hitID = None
            redShooter = False
            redHit = False

            shooterID, redShooter = findPlayerByHardwareID(player1)
            hitID, redHit = findPlayerByHardwareID(player2)

            #find which team
            if redShooter: #player who shot in redPlayers
                print('shooter is red player')
                if redHit: #friendly fire
                    updateScore(shooterID, hitID, False, -10)
                else: # red hit green
                    updateScore(shooterID, hitID, False, 10)
            else: #greenPlayer shot redPlayer
                print('shooter is green')
                if not redHit: #friendly fire
                    updateScore(shooterID, hitID, True, -10)
                else: # green hit red
                    updateScore(shooterID, hitID, True, 10)

def updateScore(shooter, hit, teamBool, points): #teamBool = False, red : teamBool = True, green
    if not teamBool: #shooter is red player
        if points < 0: # friendly fire, hit is red player, take points away from both players
            _actionScreen.redScores[str(shooter)][0].set(_actionScreen.redScores[str(shooter)][0].get() + points)
            _actionScreen.redScores[str(hit)][0].set(_actionScreen.redScores[str(hit)][0].get() + points)
            _actionScreen.redTotalScore.set(_actionScreen.redTotalScore.get() + points*2)
        else: # red hit green player
            _actionScreen.redScores[str(shooter)][0].set(_actionScreen.redScores[str(shooter)][0].get() + points)
            _actionScreen.redTotalScore.set(_actionScreen.redTotalScore.get() + points)
    else:
        if points < 0: # friendly fire, hit is red player, take points away from both players
            _actionScreen.greenScores[str(shooter)][0].set(_actionScreen.greenScores[str(shooter)][0].get() + points)
            _actionScreen.greenScores[str(hit)][0].set(_actionScreen.greenScores[str(hit)][0].get() + points)
            _actionScreen.greenTotalScore.set(_actionScreen.greenTotalScore.get() + points*2)
        else: # red hit green player
            _actionScreen.greenScores[str(shooter)][0].set(_actionScreen.greenScores[str(shooter)][0].get() + points)
            _actionScreen.greenTotalScore.set(_actionScreen.greenTotalScore.get() + points)
    
    #_actionScreen.redScores[str(0)][0].set(300)
    _actionScreen.top.update_idletasks()

def findPlayerByHardwareID(hwid):
    rtnID = None
    red = False
    found = False

    for id, data in _actionScreen.redScores.items():
        if data[1].get() == hwid:
            rtnID = id
            red = True
            found = True
            break

    if not found:
        for id, data in _actionScreen.greenScores.items():
            if data[1].get() == hwid:
                rtnID = id
                break
    
    return rtnID, red

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
