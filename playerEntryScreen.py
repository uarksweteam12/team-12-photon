import tkinter as tk
from tkinter import Toplevel

gameMode = "Standard public mode"

redPlayers = {str(i): ['', ''] for i in range(20)} #makes obj from 0 to 19 (players) that has a list with 2 strings
greenPlayers = {str(i): ['', ''] for i in range(20)}
# ^^^ need to move to member var, but thats for another time...

class PlayerEntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Terminal")
        self.root.geometry("1000x750")
        self.root.configure(bg="black")

        self.currentPlayerNum = 0
        self.currentTeamNum = 0
        self.player_labels = []

        # arrow keys function
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)

        # title
        titleFrame = tk.Frame(root, bg="black")
        titleLabel = tk.Label(titleFrame, text="Edit Current Game", font=("Arial", 16), fg="blue", bg="black")
        titleLabel.pack(pady=0)
        titleFrame.pack(pady=0, fill="x")

        # teams Frame that both teams go into
        teamsFrame = tk.Frame(root, bg="black")
        teamsFrame.pack(fill="x", expand=True, side=tk.TOP)

        # Red Team
        redTeam = tk.Frame(teamsFrame, bg="red")
        tk.Label(redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        redTeam.pack(padx=100, pady=0, side=tk.LEFT)

        # Green Team
        greenTeam = tk.Frame(teamsFrame, bg="green")
        tk.Label(greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        greenTeam.pack(padx=100, pady=0, side=tk.RIGHT)

        # lets make 20 players for each team
        self.createPlayerSlots(redTeam, 0)
        self.createPlayerSlots(greenTeam, 1)

        # game mode frame with button that doesn't work right now
        gameModeFrame = tk.Frame(root, bg="black")
        gameModeFrame.pack(pady=2)
        gameModeButton = tk.Button(gameModeFrame, text=f"Game Mode: {gameMode}", command=self.changeGameMode, bg="grey")
        gameModeButton.pack(padx=10, pady=1)

        # Command Line what has all the f1, f2, f3, etc
        commandLineFrame = tk.Frame(root, bg="black")
        commandLineFrame.pack(fill="x", pady=2)

        # I want it to looke somewhat nice, so center this thing
        commandLineCenterFrame = tk.Frame(commandLineFrame, bg="black")
        commandLineCenterFrame.pack(padx=5, pady=5)

        #alright, lets add all the commands for the command line
        self.addCommandToLine(commandLineCenterFrame, "F1", "Edit\nGame", False)
        self.addCommandToLine(commandLineCenterFrame, "F2", "Game\nParameters", False)
        self.addCommandToLine(commandLineCenterFrame, "F3", "Start\nGame", False)
        self.addCommandToLine(commandLineCenterFrame, "F4", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F5", "PreEntered\nGames", False)
        self.addCommandToLine(commandLineCenterFrame, "F6", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F7", "\t\n\t", False)
        self.addCommandToLine(commandLineCenterFrame, "F8", "View\nGame", False)
        self.addCommandToLine(commandLineCenterFrame, "F9", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F10", "Flick\nSync", False)
        self.addCommandToLine(commandLineCenterFrame, "F11", "", True)
        self.addCommandToLine(commandLineCenterFrame, "F12", "Clear\nGame", False)

        # lets put some instructions at the bottom and show that we can do stuff...
        instructionLineFrame = tk.Frame(root, bg="grey", height=50)
        instructionLineFrame.pack(fill="x", pady=10)
        instructionLineLabel = tk.Label(instructionLineFrame, text="<Del> to Delete Player, <Ins> to Manually Insert, or edit codename", fg="black", bg="grey")
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
        print("changing mode, idk what to do rn...") #for the future

    def createPlayerSlots(self, teamFrame, teamNum): #lets do a loop and create playerSlots
        for i in range(20): 
            self.playerSlot(teamFrame, i, teamNum)

    def playerSlot(self, teamFrame, playerNum, teamNum):
        frame = tk.Frame(teamFrame, bg=teamFrame["bg"]) #creats the player lines in the team...
        frame.pack(pady=2)                              #arrow, number, text, text longer

        arrow_label = tk.Label(frame, text=">" if (playerNum == self.currentPlayerNum and teamNum == self.currentTeamNum) else " ", bg=teamFrame["bg"], fg="white")
        arrow_label.pack(side=tk.LEFT, padx=2)

        tk.Label(frame, text=str(playerNum), width=3, bg=teamFrame["bg"], fg="white").pack(side=tk.LEFT, padx=2)

        tk.Entry(frame, width=15).pack(side=tk.LEFT, padx=2)
        tk.Entry(frame, width=20).pack(side=tk.LEFT, padx=2)

        # Store reference to arrow labels for easy updates
        self.player_labels.append((arrow_label, playerNum, teamNum))


