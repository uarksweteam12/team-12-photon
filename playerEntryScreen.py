import tkinter as tk
from tkinter import Toplevel

debugMode = False
# ^^^ disables database to code will function on windows/mac without VM. 
# WARNING: stuff may not function correctly so be careful!

import database
import udpClient
#import udpServer
import ipaddress
import askWindow
import actionScreen

gameMode = "Standard Public Mode"
game = None

class PlayerEntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Terminal")
        #self.root.geometry("1000x750") #dont need this becuase we using pack and stuff below (auto resize)
        self.root.configure(bg="black")

        self.currentPlayerNum = 0
        self.currentTeamNum = 0
        self.player_labels = []

        # 0=id, 1=codename, 2=hardwareid
        self.redPlayers = {str(i): [tk.StringVar(), tk.StringVar(), tk.IntVar()] for i in range(15)}
        
        #makes obj from 0 to 19 (players) that has a list with 2 strings
        self.greenPlayers = {str(i): [tk.StringVar(), tk.StringVar(), tk.IntVar()] for i in range(15)}

        # key function
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)
        self.root.bind("<Return>", self.on_key_press)
        self.root.bind("<F12>", self.on_key_press)
        self.root.bind("<F5>", self.on_key_press)
        self.root.bind("<F11>", self.debugMode)

        # title
        self.titleFrame = tk.Frame(root, bg="black")
        self.titleLabel = tk.Label(self.titleFrame, text="Edit Current Game", font=("Arial", 16), fg="blue", bg="black")
        self.titleLabel.pack(pady=0)
        self.titleFrame.pack(pady=0, fill="x")

        # teams Frame that both teams go into
        self.teamsFrame = tk.Frame(self.root, bg="black")
        self.teamsFrame.pack(fill="both", expand=True, side=tk.TOP)

        # need to center redTeam, InstructMiddle, and greenTeam frame
        self.teamsFrameCenter = tk.Frame(self.teamsFrame, bg="black")
        self.teamsFrameCenter.pack(padx=5, pady=5, expand=True)

        # Red Team
        self.redTeam = tk.Frame(self.teamsFrameCenter, bg="red")
        tk.Label(self.redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        self.redTeam.pack(padx=10, pady=0, side=tk.LEFT, fill="y")

        # instructions for controls, adding players, etc.
        self.instructMiddleFrame = tk.Frame(self.teamsFrameCenter, bg="grey")
        tk.Label(self.instructMiddleFrame, text="Press the <ENTER> key to add player\nEnsure player is selected by using arrow keys").pack(padx=10, pady=5)
        self.instructMiddleFrame.pack(side=tk.LEFT, fill="x")

        # Green Team
        self.greenTeam = tk.Frame(self.teamsFrameCenter, bg="green")
        tk.Label(self.greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        self.greenTeam.pack(padx=10, pady=0, side=tk.LEFT, fill="y")

        # lets make 20 players for each team
        self.createPlayerSlots(self.redTeam, 0)
        self.createPlayerSlots(self.greenTeam, 1)

        # game mode frame with button that doesn't work right now
        self.gameModeFrame = tk.Frame(self.root, bg="grey")
        self.gameModeFrame.pack(pady=2)
        self.gameModeButton = tk.Button(self.gameModeFrame, text=f"Game Mode: {gameMode}", command=self.changeGameMode, bg="grey")
        self.gameModeButton.pack(padx=3, pady=2, side=tk.LEFT)

        #adds a way to change ip from entry screen
        self.ipChangeFrame = tk.Frame(self.gameModeFrame, bg="grey")
        self.ipChangeFrame.pack(side=tk.LEFT)

        self.ipChangeLabel = tk.Label(self.ipChangeFrame, text="Change IP:", bg="grey", fg="black")
        self.ipChangeLabel.pack(side=tk.LEFT) 
        self.ipChangeEntry = tk.Entry(self.ipChangeFrame, width=15) #need self. to get ip from text entry in the changeIP func
        self.ipChangeEntry.pack(side=tk.LEFT)
        self.ipChangeSubmit = tk.Button(self.ipChangeFrame, text="Confirm", command=self.changeIP, bg="grey")
        self.ipChangeSubmit.pack(side=tk.LEFT, padx=3, pady=2)


        # Command Line what has all the f1, f2, f3, etc
        self.commandLineFrame = tk.Frame(self.root, bg="black")
        self.commandLineFrame.pack(fill="x", pady=2)

        # I want it to look somewhat nice, so center this thing
        self.commandLineCenterFrame = tk.Frame(self.commandLineFrame, bg="black")
        self.commandLineCenterFrame.pack(padx=5, pady=5)

        #alright, lets add all the commands for the command line
        #blacking out everything right now since we don't need it for sprint 2
        self.addCommandToLine(self.commandLineCenterFrame, "F1", "Edit\nGame", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F2", "Game\nParameters", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F3", "Start\nGame", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F4", "", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F5", "Start\nGame", False)
        self.addCommandToLine(self.commandLineCenterFrame, "F6", "", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F7", "\t\n\t", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F8", "View\nGame", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F9", "", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F10", "Flick\nSync", True)
        self.addCommandToLine(self.commandLineCenterFrame, "F11", "Toggle\nDebug Mode", False)
        self.addCommandToLine(self.commandLineCenterFrame, "F12", "Clear\nGame", False)

        # lets put some instructions at the bottom and show that we can do stuff...
        self.instructionLineFrame = tk.Frame(self.root, bg="grey", height=50)
        self.instructionLineFrame.pack(fill="x", pady=10)
        self.instructionLineLabel = tk.Label(self.instructionLineFrame, text="Press the <ENTER> key to add player", fg="black", bg="grey")
        self.instructionLineLabel.pack(padx=5, pady=5)

        self.root.update_idletasks()
        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}") #makes sure the window size is correct and not wrong... don't worry this code is perfect

    def refresh_display(self):
        for label, playerNum, teamNum in self.player_labels:
            if playerNum == self.currentPlayerNum and teamNum == self.currentTeamNum:
                label.config(text=">")
            else:
                label.config(text="\u00A0\u00A0")

    def on_key_press(self, event):
        if event.keysym == "Up": # probably a better way to toggle all this stuff, but I'm kinda dumb,
            if self.currentPlayerNum != 0:  #if you know a better way, feel free to simplify this code
                self.currentPlayerNum = self.currentPlayerNum - 1
            else:
                self.currentPlayerNum = 14
        elif event.keysym == "Down":
            if self.currentPlayerNum != 14:
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
            
            # Add the variable values into dababase file
            if self.currentTeamNum == 0:
                idvar = str(self.redPlayers[str(self.currentPlayerNum)][0].get())
                team = "Red"
                result = None

                if(not debugMode):
                    result = database.playerIdExist(idvar)
                if result == None: #ask for codename if it isn't in database
                    window = askWindow.AskWindow(self.root, True) 

                    codenameRtn = window.getResult() 
                    self.redPlayers[str(self.currentPlayerNum)][1].set(str(codenameRtn))

                    if(not debugMode):
                        database.insert_player(idvar, codenameRtn) #add to database so that they exist now
                else:
                    self.redPlayers[str(self.currentPlayerNum)][1].set(str(result)) #populate codename text entry on screen

                #ask for hardwareID
                window = askWindow.AskWindow(self.root, False) 

                hardwareidRtn = window.getResult() 
                self.redPlayers[str(self.currentPlayerNum)][2].set(int(hardwareidRtn))
            else:
                idvar = str(self.greenPlayers[str(self.currentPlayerNum)][0].get())
                team = "Green"
                result = None

                if(not debugMode):
                    result = database.playerIdExist(idvar)
                if result == None: #ask for codename if it isn't in database
                    window = askWindow.AskWindow(self.root, True) 

                    codenameRtn = window.getResult() 
                    self.greenPlayers[str(self.currentPlayerNum)][1].set(str(codenameRtn))
                    
                    if(not debugMode):
                        database.insert_player(idvar, codenameRtn) #add to database so that they exist now
                else:
                    self.greenPlayers[str(self.currentPlayerNum)][1].set(str(result)) #populate codename text entry on screen

                #ask for hardwareID
                window = askWindow.AskWindow(self.root, False) 

                hardwareidRtn = window.getResult() 
                self.greenPlayers[str(self.currentPlayerNum)][2].set(int(hardwareidRtn))
            
            if(not debugMode):
                database.fetch_players()
            # Send player info via UDP
            udpClient.send_equipment_code(hardwareidRtn)
        elif event.keysym == "F12": #<F12> key to remove player entries
            print("F12 pressed")
            for x in range(15):
                self.redPlayers[str(x)][0].set("")
                self.redPlayers[str(x)][1].set("")
                self.redPlayers[str(x)][2].set(-1)
                self.greenPlayers[str(x)][0].set("")
                self.greenPlayers[str(x)][1].set("")
                self.greenPlayers[str(x)][2].set(-1)
        elif event.keysym == "F5": #<F5> key to switch to play action screen
            actionScreen.ActionScreen(self.root, self.redPlayers, self.greenPlayers, debugMode)




        self.refresh_display()
        #print(f"player={self.currentPlayerNum}, team={self.currentTeamNum}") to make sure it is changing correctly

    def debugMode(self, event):
        global debugMode
        debugMode = not debugMode
        print(f"Debug: {debugMode}")

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
            udpClient.set_server_ip(newip) # update network for udp sockets
            print(f"Server IP updated to: {newip}")
        
        except Exception as e:
            print(f"Invalid IP address: {e}")
            

    def createPlayerSlots(self, teamFrame, teamNum): #lets do a loop and create playerSlots
        for i in range(15): 
            self.playerSlot(teamFrame, i, teamNum)

    def playerSlot(self, teamFrame, playerNum, teamNum):
        frame = tk.Frame(teamFrame, bg=teamFrame["bg"]) #creats the player lines in the team...
        frame.pack(pady=2)                              #arrow, number, text, text longer

        arrow_label = tk.Label(frame, text=">" if (playerNum == self.currentPlayerNum and teamNum == self.currentTeamNum) else "\u00A0\u00A0", bg=teamFrame["bg"], fg="white")
        arrow_label.pack(side=tk.LEFT, padx=2)

        tk.Label(frame, text=str(playerNum), width=3, bg=teamFrame["bg"], fg="white").pack(side=tk.LEFT, padx=2)

        if teamNum == 0:
            tk.Entry(frame, width=15, textvariable=self.redPlayers[str(playerNum)][0]).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, width=20, state=tk.DISABLED, textvariable=self.redPlayers[str(playerNum)][1]).pack(side=tk.LEFT, padx=2)
            #self.redPlayers[str(self.currentPlayerNum)][0] = idvar
            #self.redPlayers[str(self.currentPlayerNum)][1] = codenamevar
        else:
            tk.Entry(frame, width=15, textvariable=self.greenPlayers[str(playerNum)][0]).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, width=20, state=tk.DISABLED, textvariable=self.greenPlayers[str(playerNum)][1]).pack(side=tk.LEFT, padx=2)

        # Store reference to arrow labels for easy updates
        self.player_labels.append((arrow_label, playerNum, teamNum))
        #print(self.redPlayers)


