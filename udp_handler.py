import socket

UDP_IP = "127.0.0.1" # I'm not entirely sure if this is the IP address we should be using
UDP_PORT = 7500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_equipment_code(player_id, codename, team) -> bool:
    """
    Sends a player's ID, codename, and team to the UDP server
    """

    message = f"{team}, {player_id}, {codename}" # We can change this later if we want

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



    




