import tkinter as tk
from tkinter import Toplevel
import udp_handler
import ipaddress

gameMode = "Standard Public Mode"


class PlayerEntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Terminal")
        self.root.geometry("1000x750")
        self.root.configure(bg="black")

        self.currentPlayerNum = 0
        self.currentTeamNum = 0
        self.player_labels = []

        #self.redPlayers = {str(i): [tk.StringVar(), tk.StringVar()] for i in range(20)}
        self.redPlayers = {
            '0': [tk.StringVar(), tk.StringVar()],
            '1': [tk.StringVar(), tk.StringVar()],
            '2': [tk.StringVar(), tk.StringVar()],
            '3': [tk.StringVar(), tk.StringVar()],
            '4': [tk.StringVar(), tk.StringVar()],
            '5': [tk.StringVar(), tk.StringVar()],
            '6': [tk.StringVar(), tk.StringVar()],
            '7': [tk.StringVar(), tk.StringVar()],
            '8': [tk.StringVar(), tk.StringVar()],
            '9': [tk.StringVar(), tk.StringVar()],
            '10': [tk.StringVar(), tk.StringVar()],
            '11': [tk.StringVar(), tk.StringVar()],
            '12': [tk.StringVar(), tk.StringVar()],
            '13': [tk.StringVar(), tk.StringVar()],
            '14': [tk.StringVar(), tk.StringVar()],
            '15': [tk.StringVar(), tk.StringVar()],
            '16': [tk.StringVar(), tk.StringVar()],
            '17': [tk.StringVar(), tk.StringVar()],
            '18': [tk.StringVar(), tk.StringVar()],
            '19': [tk.StringVar(), tk.StringVar()]
        }
        
        
         #makes obj from 0 to 19 (players) that has a list with 2 strings
        self.greenPlayers = {str(i): [tk.StringVar(), tk.StringVar()] for i in range(20)}

        # arrow keys function
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)
        self.root.bind("<Return>", self.on_key_press)

        # title
        titleFrame = tk.Frame(root, bg="black")
        titleLabel = tk.Label(titleFrame, text="Edit Current Game", font=("Arial", 16), fg="blue", bg="black")
        titleLabel.pack(pady=0)
        titleFrame.pack(pady=0, fill="x")

        # teams Frame that both teams go into
        teamsFrame = tk.Frame(root, bg="black")
        teamsFrame.pack(fill="x", expand=True, side=tk.TOP)

        # need to center redTeam, InstructMiddle, and greenTeam frame
        teamsFrameCenter = tk.Frame(teamsFrame, bg="black")
        teamsFrameCenter.pack(padx=5, pady=5)

        # Red Team
        redTeam = tk.Frame(teamsFrameCenter, bg="red")
        tk.Label(redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        redTeam.pack(padx=10, pady=0, side=tk.LEFT)

        # instructions for controls, adding players, etc.
        instructMiddleFrame = tk.Frame(teamsFrameCenter, bg="grey")
        tk.Label(instructMiddleFrame, text="Press the <ENTER> key to add player\nEnsure player is selected by using arrow keys").pack(padx=10, pady=5)
        instructMiddleFrame.pack(side=tk.LEFT)

        # Green Team
        greenTeam = tk.Frame(teamsFrameCenter, bg="green")
        tk.Label(greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        greenTeam.pack(padx=10, pady=0, side=tk.LEFT)

        # lets make 20 players for each team
        self.createPlayerSlots(redTeam, 0)
        self.createPlayerSlots(greenTeam, 1)

        # game mode frame with button that doesn't work right now
        gameModeFrame = tk.Frame(root, bg="grey")
        gameModeFrame.pack(pady=2)
        gameModeButton = tk.Button(gameModeFrame, text=f"Game Mode: {gameMode}", command=self.changeGameMode, bg="grey")
        gameModeButton.pack(padx=3, pady=2, side=tk.LEFT)

        #adds a way to change ip from entry screen
        ipChangeFrame = tk.Frame(gameModeFrame, bg="grey")
        ipChangeFrame.pack(side=tk.LEFT)

        ipChangeLabel = tk.Label(ipChangeFrame, text="Change IP:", bg="grey", fg="black")
        ipChangeLabel.pack(side=tk.LEFT) 
        self.ipChangeEntry = tk.Entry(ipChangeFrame, width=15) #need self. to get ip from text entry in the changeIP func
        self.ipChangeEntry.pack(side=tk.LEFT)
        ipChangeSubmit = tk.Button(ipChangeFrame, text="Confirm", command=self.changeIP, bg="grey")
        ipChangeSubmit.pack(side=tk.LEFT, padx=3, pady=2)


        # Command Line what has all the f1, f2, f3, etc
        commandLineFrame = tk.Frame(root, bg="black")
        commandLineFrame.pack(fill="x", pady=2)

        # I want it to look somewhat nice, so center this thing
        commandLineCenterFrame = tk.Frame(commandLineFrame, bg="black")
        commandLineCenterFrame.pack(padx=5, pady=5)

        #alright, lets add all the commands for the command line
        #blacking out everything right now since we don't need it for sprint 2
        self.addCommandToLine(commandLineCenterFrame, "F1", "Edit\nGame", True)
        self.addCommandToLine(commandLineCenterFrame, "F2", "Game\nParameters", True)
        self.addCommandToLine(commandLineCenterFrame, "F3", "Start\nGame", True)
        self.addCommandToLine(commandLineCenterFrame, "F4", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F5", "PreEntered\nGames", True)
        self.addCommandToLine(commandLineCenterFrame, "F6", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F7", "\t\n\t", True)
        self.addCommandToLine(commandLineCenterFrame, "F8", "View\nGame", True)
        self.addCommandToLine(commandLineCenterFrame, "F9", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F10", "Flick\nSync", True)
        self.addCommandToLine(commandLineCenterFrame, "F11", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F12", "Clear\nGame", True)

        # lets put some instructions at the bottom and show that we can do stuff...
        instructionLineFrame = tk.Frame(root, bg="grey", height=50)
        instructionLineFrame.pack(fill="x", pady=10)
        instructionLineLabel = tk.Label(instructionLineFrame, text="Press the <ENTER> key to add player", fg="black", bg="grey")
        instructionLineLabel.pack(padx=5, pady=5)

    def refresh_display(self):
        for label, playerNum, teamNum in self.player_labels:
            if playerNum == self.currentPlayerNum and teamNum == self.currentTeamNum:
                label.config(text=">")
            else:
                label.config(text=" ")

    def on_key_press(self, event):
        if event.keysym == "Up": # probably a better way to toggle all this stuff, but I'm kinda dumb,
            if self.currentPlayerNum != 0:  #if you know a better way, feel free to simplify this code
                self.currentPlayerNum = self.currentPlayerNum - 1
            else:
                self.currentPlayerNum = 19
        elif event.keysym == "Down":
            if self.currentPlayerNum != 19:
                self.currentPlayerNum = self.currentPlayerNum + 1
            else:
                self.currentPlayerNum = 0
        elif event.keysym == "Left": #toggle teams
            if self.currentTeamNum == 0:
                self.currentTeamNum = 1
            else:
                self.currentTeamNum = 0
        elif event.keysym == "Right": #toggle teams
            if self.currentTeamNum == 1:
                self.currentTeamNum = 0
            else:
                self.currentTeamNum = 1
        elif event.keysym == "Return": #<ENTER> key to add player
            #print(self.currentPlayerNum)
            if self.currentTeamNum == 0:
                idvar = self.redPlayers[str(self.currentPlayerNum)][0].get()
                codenamevar = self.redPlayers[str(self.currentPlayerNum)][1].get()
                team = "Red"
            else:
                idvar = self.greenPlayers[str(self.currentPlayerNum)][0].get()
                codenamevar = self.greenPlayers[str(self.currentPlayerNum)][1].get()
                team = "Green"
            
            # Send player info via UDP
            if idvar and codenamevar:
                udp_handler.send_equipment_code(idvar, codenamevar, team)
            #print(idvar)


        self.refresh_display()
        #print(f"player={self.currentPlayerNum}, team={self.currentTeamNum}") to make sure it is changing correctly

    def addCommandToLine(self, frame, cmd, action, blackout):
        if not blackout: 
            command = tk.Frame(frame, borderwidth=1, relief="solid", bg="grey")
            command.pack(padx=10, pady=2, side=tk.LEFT)
            label = tk.Label(command, text=f"{cmd}\n{action}", fg="#32CD32", bg="black")
            label.pack(padx=2, pady=2)
        else: #ngl, I got lazy and changed the stuff to black that we dont use, lol, sorry for the pain this causes
            command = tk.Frame(frame, borderwidth=1, relief="solid", bg="black")
            command.pack(padx=10, pady=2, side=tk.LEFT)
            label = tk.Label(command, text=f"{cmd}\n{action}", fg="black", bg="black")
            label.pack(padx=2, pady=2)

    def changeGameMode(self):
        print("todo in future sprint") #for the future

    def changeIP(self):
        newip = self.ipChangeEntry.get().strip() #already gets you the ip to change somehow, good luck!

        try:
            ipaddress.IPv4Address(newip) # raises a value error if invalid IPv4 address
            udp_handler.set_server_ip(newip) # update network for udp sockets
            print(f"Server IP updated to: {newip}")
        
        except Exception as e:
            print(f"Invalid IP address: {e}")
            

    def createPlayerSlots(self, teamFrame, teamNum): #lets do a loop and create playerSlots
        for i in range(20): 
            self.playerSlot(teamFrame, i, teamNum)

    def playerSlot(self, teamFrame, playerNum, teamNum):
        frame = tk.Frame(teamFrame, bg=teamFrame["bg"]) #creats the player lines in the team...
        frame.pack(pady=2)                              #arrow, number, text, text longer

        arrow_label = tk.Label(frame, text=">" if (playerNum == self.currentPlayerNum and teamNum == self.currentTeamNum) else " ", bg=teamFrame["bg"], fg="white")
        arrow_label.pack(side=tk.LEFT, padx=2)

        tk.Label(frame, text=str(playerNum), width=3, bg=teamFrame["bg"], fg="white").pack(side=tk.LEFT, padx=2)

        if teamNum == 0:
            tk.Entry(frame, width=15, textvariable=self.redPlayers[str(playerNum)][0]).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, width=20, textvariable=self.redPlayers[str(playerNum)][1]).pack(side=tk.LEFT, padx=2)
            #self.redPlayers[str(self.currentPlayerNum)][0] = idvar
            #self.redPlayers[str(self.currentPlayerNum)][1] = codenamevar
        else:
            tk.Entry(frame, width=15, textvariable=self.greenPlayers[str(playerNum)][0]).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, width=20, textvariable=self.greenPlayers[str(playerNum)][1]).pack(side=tk.LEFT, padx=2)

        # Store reference to arrow labels for easy updates
        self.player_labels.append((arrow_label, playerNum, teamNum))
        #print(self.redPlayers)


