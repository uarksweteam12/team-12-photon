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
                _actionScreen.top.after(10, updateUI)

    except BlockingIOError:
        # No data to receive, continue polling
        pass

    # Schedule next check
    _actionScreen.top.after(100, poll_udp_socket)

def updateUI():
    if _actionScreen:
        # Update the red team's player 0 score as an example
        _actionScreen.redScores[str(0)][0].set(300)
        _actionScreen.top.update_idletasks()

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
