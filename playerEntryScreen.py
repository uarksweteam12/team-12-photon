import tkinter as tk
from tkinter import Toplevel

gameMode = "Standard public mode"

class PlayerEntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Terminal") # Window Title
        self.root.geometry("1000x850") # Window Size
        self.root.configure(bg="black") # Background Color

        # title
        tk.Label(self.root, text="Edit Current Game", font=("Arial", 16), fg="blue", bg="black").pack(pady=5) #title

        teamsFrame = tk.Frame(root, bg="black")
        teamsFrame.pack(fill=tk.BOTH, expand=True)

        #redTeam box
        redTeam = tk.Frame(teamsFrame, bg="red") 
        redLabel = tk.Label(redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        redTeam.pack(padx=100, pady=5, side=tk.LEFT) #puts red team to the right

        #greenTeam box
        greenTeam = tk.Frame(teamsFrame, bg="green") 
        greenLabel = tk.Label(greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        greenTeam.pack(padx=100, pady=5, side=tk.RIGHT) #puts green team to the right

        #now lets make 20 things for each team.... yay
        createPlayerSlots(self, redTeam, "red")
        createPlayerSlots(self, greenTeam, "green")

        #gameMode stuff
        gameModeFrame = tk.Frame(root, bg="black", width=500)
        gameModeFrame.pack(pady=10)
        gameModeButton = tk.Button(gameModeFrame, text=f"Game Mode: {gameMode}", command=changeGameMode, bg="grey")
        gameModeButton.pack(padx=10, pady=1)

        #command line frame (f1 = edit game, f2 = game params, etc...)
        commandLineFrame = tk.Frame(root, bg="black", height=80)
        commandLineFrame.pack(fill="x", pady=10)

        #lets add the commands to the command line now
        commandLineCenterFrame = tk.Frame(commandLineFrame, bg="black")
        commandLineCenterFrame.pack(padx=5, pady=5) #need these to add commands and center them on screen
        addCommandToLine(self, commandLineCenterFrame, "F1", "Edit\nGame", False)
        addCommandToLine(self, commandLineCenterFrame, "F2", "Game\nParameters", False)
        addCommandToLine(self, commandLineCenterFrame, "F3", "Start\nGame", False)
        addCommandToLine(self, commandLineCenterFrame, "F4", "", True)
        addCommandToLine(self, commandLineCenterFrame, "F5", "PreEntered\nGames", False)
        addCommandToLine(self, commandLineCenterFrame, "F6", "", True)
        addCommandToLine(self, commandLineCenterFrame, "F7", "\t\n\t", False)
        addCommandToLine(self, commandLineCenterFrame, "F8", "View\nGame", False)
        addCommandToLine(self, commandLineCenterFrame, "F9", "", True)
        addCommandToLine(self, commandLineCenterFrame, "F10", "Flick\nSync", False)
        addCommandToLine(self, commandLineCenterFrame, "F11", "", True)
        addCommandToLine(self, commandLineCenterFrame, "F12", "Clear\nGame", False)

        #lets add a instruction line at the bottom
        instructionLineFrame = tk.Frame(root, bg="grey", height=50)
        instructionLineFrame.pack(fill="x", pady=10)
        instructionLineLabel = tk.Label(instructionLineFrame, text="<Del> to Delete Player, <Ins> to Manually Insert, or edit codename", fg="black", bg="grey")
        instructionLineLabel.pack(padx=5, pady=5)



def addCommandToLine(self, frame, cmd, action, blackout):
    if not blackout:
        command = tk.Frame(frame, borderwidth=1, relief="solid", bg="grey")
        command.pack(padx=10, pady=2, side=tk.LEFT)
        label = tk.Label(command, text=f"{cmd}\n{action}", fg="#32CD32", bg="black")
        label.pack(padx=2, pady=2)
    else:
        command = tk.Frame(frame, borderwidth=1, relief="solid", bg="black")
        command.pack(padx=10, pady=2, side=tk.LEFT)
        label = tk.Label(command, text=f"{cmd}\n{action}", fg="black", bg="black")
        label.pack(padx=2, pady=2)


def changeGameMode():
    print("changing mode, idk what to do rn...")

def createPlayerSlots(self, teamFrame, teamColor):
    for i in range(20):
        playerSlot(self, teamFrame, i)

def playerSlot(self, teamFrame, playerNum):
    frame = tk.Frame(teamFrame, bg=teamFrame["bg"])
    frame.pack(pady=2)

    tk.Label(frame, text=str(playerNum), width=3, bg=teamFrame["bg"], fg="white").pack(side=tk.LEFT, padx=2)

    tk.Entry(frame, width=15).pack(side=tk.LEFT, padx=2)
    tk.Entry(frame, width=20).pack(side=tk.LEFT, padx=2)
