import socket
import tkinter as tk


UDP_IP = "127.0.0.1" 
UDP_PORT = 7500

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
buffer = 1024
sock.bind(("127.0.0.1", 7501))
sock.setblocking(False)  # Make socket non-blocking

_actionScreen = None
_gameOnline = False  # internal flag to stop polling when game ends
_lastRedBase = -1
_lastGreenBase = -1
_recentAction = []


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

def flash(frame, team, count=0):
    if count >= 10:
        setFrameColor(frame, "white")
        return

    currentColor = frame.cget("bg")
    newColor = "yellow" if currentColor == "white" else "white"
    print(f"Flashing {frame} to {newColor}")
    setFrameColor(frame, newColor)
    _actionScreen.top.update()

    if team == "green":
        if _actionScreen.redTotalScore.get() < _actionScreen.greenTotalScore.get():
            _actionScreen.top.after(300, lambda: flash(frame, team, count + 1))
        else:
            setFrameColor(frame, "white")  # team changed, stop flashing
    else:
        if _actionScreen.greenTotalScore.get() < _actionScreen.redTotalScore.get():
            _actionScreen.top.after(300, lambda: flash(frame, team, count + 1))
        else:
            setFrameColor(frame, "white")  # team changed, stop flashing

    def setFrameColor(frame, color):
        frame.config(bg=color)
        for child in frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=color)
            elif isinstance(child, tk.Entry):
                # Update both normal and disabled backgrounds
                child.config(bg=color, disabledbackground=color)

    # Removed the `if winningTeam == "green":` block, as it is handled by dynamic conditions
    flash(_actionScreen.greenTotalFrame, "green")  # Flash based on current winning conditions
    setFrameColor(_actionScreen.redTotalFrame, "white")  # Reset the other team's frame to white



def poll_udp_socket():
    global _gameOnline

    if not _gameOnline or not _actionScreen or not _actionScreen.top.winfo_exists():
        return

    try:
        msgFromServer = sock.recvfrom(buffer)
        data = msgFromServer[0].decode('utf-8')
        splitThemUp = data.split(":")

        print(f"Client received: {data}")

        if data == "221":  #why did I do this????
            endGame()
            return  # Stop polling
        else:
            sock.sendto(splitThemUp[1].encode(), (UDP_IP, UDP_PORT)) #should send hit player now...

            if _actionScreen is not None:
                flash()
                print("test")
                _actionScreen.top.after(10, lambda: updateUI(splitThemUp[0], splitThemUp[1]))

    except BlockingIOError:
        # No data to receive, continue polling
        pass

    # Schedule next check
    _actionScreen.top.after(100, poll_udp_socket)

def updateUI(player1, player2):
    if _actionScreen:
        if player2 == "53": # red base
            shooterID, redShooter = findPlayerByHardwareID(player1)

            if not redShooter:
                updateScore(shooterID, player2, False, 100)
                # do B here
        elif player2 == "43": #green base
            shooterID, redShooter = findPlayerByHardwareID(player1)

            if redShooter:
                updateScore(shooterID, player2, False, 100)
                # do B here
        else: #player hit player
            shooterID = None
            hitID = None
            redShooter = False
            redHit = False

            shooterID, redShooter = findPlayerByHardwareID(player1)
            hitID, redHit = findPlayerByHardwareID(player2)

            #find which team
            if redShooter: #player who shot in redPlayers
                if redHit: #friendly fire
                    updateScore(shooterID, hitID, False, -10)
                else: # red hit green
                    updateScore(shooterID, hitID, False, 10)
            else: #greenPlayer shot redPlayer
                if not redHit: #friendly fire
                    updateScore(shooterID, hitID, True, -10)
                else: # green hit red
                    updateScore(shooterID, hitID, True, 10)

def determineAction(shooter, hit, teamBool, points):
    if hit == "53": #green hit red base
        msg = f'{_actionScreen.greenPlayers[str(shooter)][1].get()} hit Red Base'
    elif hit == "43": #red hit green base
        msg = f'{_actionScreen.redPlayers[str(shooter)][1].get()} hit Green Base'
    elif not teamBool: #shooter is red player
        if points < 0: # friendly fire, hit is red player, take points away from both players
            msg = f'{_actionScreen.redPlayers[str(shooter)][1].get()} friendly fire on {_actionScreen.redPlayers[str(hit)][1].get()}'
        else: # red hit green player
            msg = f'{_actionScreen.redPlayers[str(shooter)][1].get()} hit {_actionScreen.greenPlayers[str(hit)][1].get()}'
    else:
        if points < 0: # friendly fire, hit is red player, take points away from both players
            msg = f'{_actionScreen.greenPlayers[str(shooter)][1].get()} friendly fire on {_actionScreen.greenPlayers[str(hit)][1].get()}'
        else: # red hit green player
            msg = f'{_actionScreen.greenPlayers[str(shooter)][1].get()} hit {_actionScreen.redPlayers[str(hit)][1].get()}'

    logAction(msg)
    
def logAction(msg):
    global _recentAction

    if len(_recentAction) >= 5:
        _recentAction.pop(0)
    _recentAction.append(msg)

    for i in range(5):
        if i < len(_recentAction):
            _actionScreen.eventsLabels[i].config(text=_recentAction[i])
        else:
            _actionScreen.eventsLabels[i].config(text="")



def updateScore(shooter, hit, teamBool, points): #teamBool = False, red : teamBool = True, green
    global _lastGreenBase, _lastRedBase

    determineAction(shooter, hit, teamBool, points)
    
    if hit == "53": #green hit red base
        _actionScreen.greenScores[str(shooter)][0].set(_actionScreen.greenScores[str(shooter)][0].get() + points)
        if not _lastGreenBase == -1:
            _actionScreen.greenScores[str(_lastGreenBase)][2].set("")
        _actionScreen.greenScores[str(shooter)][2].set("B")
        _lastGreenBase = shooter
        _actionScreen.greenTotalScore.set(_actionScreen.greenTotalScore.get() + points)
    elif hit == "43": #red hit green base
        _actionScreen.redScores[str(shooter)][0].set(_actionScreen.redScores[str(shooter)][0].get() + points)
        if not _lastRedBase == -1:
            _actionScreen.redScores[str(_lastRedBase)][2].set("")
        _actionScreen.redScores[str(shooter)][2].set("B")
        _lastRedBase = shooter
        _actionScreen.redTotalScore.set(_actionScreen.redTotalScore.get() + points)
    elif not teamBool: #shooter is red player
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
        if str(data[1].get()) == str(hwid):
            rtnID = id
            red = True
            found = True
            break

    if not found:
        for id, data in _actionScreen.greenScores.items():
            if str(data[1].get()) == str(hwid):
                rtnID = id
                break
    
    return rtnID, red

def endGame():
    global _gameOnline
    _gameOnline = False
    msg = "221"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
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
