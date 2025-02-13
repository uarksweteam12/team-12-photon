import tkinter as tk
from tkinter import Toplevel


class PlayerEntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Terminal") # Window Title
        self.root.geometry("1000x750") # Window Size
        self.root.configure(bg="black") # Background Color

        # title
        tk.Label(self.root, text="Edit Current Game", font=("Arial", 16), fg="blue", bg="black").pack(pady=5) #title

        #redTeam box
        redTeam = tk.Frame(root, bg="red") 
        redLabel = tk.Label(redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        redTeam.pack(padx=100, pady=5, side=tk.LEFT) #puts red team to the right

        #greenTeam box
        greenTeam = tk.Frame(root, bg="green") 
        greenLabel = tk.Label(greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        greenTeam.pack(padx=100, pady=5, side=tk.RIGHT) #puts green team to the right

        #now lets make 20 things for each team.... yay
        createPlayerSlots(self, redTeam, "red")
        createPlayerSlots(self, greenTeam, "green")




def createPlayerSlots(self, teamFrame, teamColor):
    for i in range(20):
        playerSlot(self, teamFrame, i)

def playerSlot(self, teamFrame, playerNum):
    frame = tk.Frame(teamFrame, bg=teamFrame["bg"])
    frame.pack(pady=2)

    tk.Label(frame, text=str(playerNum), width=3, bg=teamFrame["bg"], fg="white").pack(side=tk.LEFT, padx=2)

    tk.Entry(frame, width=15).pack(side=tk.LEFT, padx=2)
    tk.Entry(frame, width=20).pack(side=tk.LEFT, padx=2)
