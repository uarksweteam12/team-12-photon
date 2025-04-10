import asyncio
import socket
import tkinter as tk

UDP_IP = "127.0.0.1" 
UDP_PORT = 7500

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
buffer = 1024
sock.bind(("127.0.0.1", 7501))

_actionScreen = None

def setActionScreen(screenInstance):
    global _actionScreen
    _actionScreen = screenInstance

async def startGame():
    msg = "202"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("STARTING GAME")
    gameOnline = True
    while gameOnline:
        print("LISTENING...")
        msgFromServer = await asyncio.to_thread(sock.recvfrom, buffer)  # Use asyncio.to_thread for blocking socket
        data = msgFromServer[0].decode('utf-8')
        splitThemUp = data.split(":")
        
        if data != "221":
            sock.sendto(splitThemUp[0].encode(), (UDP_IP, UDP_PORT))

            # Trigger UI update
            if _actionScreen is not None:
                _actionScreen.top.after(10, lambda: updateUI())  # Use after to safely update UI from main thread
        else:
            gameOnline = False
        print(f'client received: {data}')

def updateUI():
    # Make sure this function updates the relevant UI components.
    if _actionScreen:
        _actionScreen.redScores[str(0)][0].set(300)  # Example: Update player 0 score
        _actionScreen.top.update_idletasks()  # Ensure UI updates properly
        _actionScreen.top.update()  # Force a full window refresh

def endGame():
    msg = "221"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print("ENDING GAME")
    # send end game signal

def send_equipment_code(hardwareid) -> bool:
    """
    Sends a player's ID, codename, and team to the UDP server
    """
    message = f"{hardwareid}"  # Example message
    
    try:
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent: {message} to {UDP_IP}:{UDP_PORT}")
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

# Integrate with Tkinter main loop
def start_async_game():
    # Start the asyncio event loop in a separate thread, then run Tkinter's mainloop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(startGame())
    loop.run_forever()

# Assuming _actionScreen is an instance of a Tkinter-based screen, set it up in your main program
