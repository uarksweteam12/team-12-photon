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

def setFrameColor(frame, color):
    frame.config(bg=color)
    for child in frame.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg=color)
        elif isinstance(child, tk.Entry):
            # Update both normal and disabled backgrounds
            child.config(bg=color, disabledbackground=color)

def flash(frame, team, count=0):
    # Stop flashing after 10 iterations
    #if count >= 10:
    #    setFrameColor(frame, "white")
    #    return

    # Alternate the color of the frame between yellow and white
    currentColor = frame.cget("bg")
    newColor = "yellow" if currentColor == "white" else "white"
    setFrameColor(frame, newColor)
    _actionScreen.top.update()

    # Check team condition to continue flashing
    if team == "green":
        if _actionScreen.redTotalScore.get() < _actionScreen.greenTotalScore.get():
            _actionScreen.top.after(300, lambda: flash(frame, team, count + 1))
        else:
            setFrameColor(frame, "white")  # Stop flashing if team changed
    else:
        if _actionScreen.greenTotalScore.get() < _actionScreen.redTotalScore.get():
            _actionScreen.top.after(300, lambda: flash(frame, team, count + 1))
        else:
            setFrameColor(frame, "white")  # Stop flashing if team changed




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

    flash(_actionScreen.greenTotalFrame, "green")  
    flash(_actionScreen.redTotalFrame, "red") 

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
    
    sort_teams()
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

def sort_team_by_score(team_color):
    if not _actionScreen:
        print("Action screen not initialized")
        return
    
    if team_color.lower() == "red":
        team_frame = None
        for widget in _actionScreen.top.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget("bg") == "red":
                                team_frame = grandchild
                                break
        
        team_scores = _actionScreen.redScores
        players = _actionScreen.redPlayers
    elif team_color.lower() == "green":
        team_frame = None
        for widget in _actionScreen.top.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.cget("bg") == "green":
                                team_frame = grandchild
                                break
        
        team_scores = _actionScreen.greenScores
        players = _actionScreen.greenPlayers
    else:
        print(f"Invalid team color: {team_color}")
        return
    
    if not team_frame:
        print(f"Could not find {team_color} team frame")
        return
    
    team_label = None
    for child in team_frame.winfo_children():
        if isinstance(child, tk.Label) and child.cget("text") in ["Red Team", "Green Team"]:
            team_label = child
            break
    
    if not team_label and team_frame.winfo_children():
        first_child = team_frame.winfo_children()[0]
        if isinstance(first_child, tk.Label):
            team_label = first_child
    
    total_frame = None
    for child in reversed(team_frame.winfo_children()):
        if isinstance(child, tk.Frame) and "Total" in str(child):
            total_frame = child
            break
    
    if not total_frame and team_frame.winfo_children():
        total_frame = team_frame.winfo_children()[-1]
    
    player_frames = []
    for child in team_frame.winfo_children():
        if child != team_label and child != total_frame and isinstance(child, tk.Frame):
            player_frames.append(child)
    
    player_data = []
    for player_id in team_scores:
        if players.get(player_id) and players[player_id][1].get() != "":
            score = team_scores[player_id][0].get()
            for frame in player_frames:
                player_found = False
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("text") == players[player_id][1].get():
                        player_data.append((player_id, score, frame))
                        player_found = True
                        break
                if player_found:
                    break
    
    player_data.sort(key=lambda x: x[1], reverse=True)
    
    for _, _, frame in player_data:
        frame.pack_forget()
    
    if team_label:
        team_label.pack_forget()
        team_label.pack(padx=10, pady=5)
    
    for _, _, frame in player_data:
        frame.pack(pady=2, fill="both")
    
    if total_frame:
        total_frame.pack_forget()
        total_frame.pack(pady=5, padx=5, side=tk.BOTTOM)
    
    _actionScreen.top.update_idletasks()

def sort_teams():
    sort_team_by_score("red")
    sort_team_by_score("green")