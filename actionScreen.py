import tkinter as tk
from tkinter import Toplevel
from pathlib import Path
from PIL import Image, ImageTk
import os
import time


class ActionScreen:
    def __init__(self, root, redPlayers, greenPlayers):
        self.top = Toplevel(root)  # dont rlly know why but I'm not asking
        self.top.title("Play Action Screen")
        self.top.configure(bg="black")
        self.top.transient(root)  
        self.top.grab_set() #I think it makes you not click out of window unless you complete task

        self.redPlayers = redPlayers
        self.greenPlayers = greenPlayers

        # 0=score, 1=B (sprint 4 thing...but I'm not doing that rn...)
        self.redScores = {str(i): [tk.IntVar()] for i in range(15)}
        self.greenScores = {str(i): [tk.IntVar()] for i in range(15)}

        self.redTotalScore = tk.IntVar()
        self.greenTotalScore = tk.IntVar()

        # 30 second timer starts here

        self.background = Image.open("countdown_images/background.tif")
        self.background_img = ImageTk.PhotoImage(self.background)

        self.background_label = tk.Label(self.top, image=self.background_img)
        self.background_label.place(relx=0.5, rely=0.5, anchor='center') # positioning for background_label

        # access images folder
        self.countdown_images = os.path.join(os.path.dirname(os.path.abspath(__file__)), "countdown_images")

        # find images and store in list
        self.image_paths = []
        for i in range(30, -1, -1):
            image_path= os.path.join(self.countdown_images, f"{i}.tif")
            self.image_paths.append(image_path)

        self.index = 0
        # self.timer_frame = tk.Frame(self.top, bg="black")
        # self.timer_frame.pack()
        self.timer_label = tk.Label(self.top, bg="black")
        self.timer_label.place(relx=0.5, rely=0.55, anchor='center') # positioning for timer_label
        # self.timer_label.pack()
        self.updateImage() # self.frame.destroy() and self.makePlayActionScreen() are called in this function


        # ****
        # PUT ALL THE CODE FOR THE PLAY ACTION SCREEN HERE!!!
        # ****



        # This must be at the end of the __init__ function, don't move!
        self.centerWindow()
        self.top.wait_window(self.top)

    def updateImage(self):

        if self.index < len(self.image_paths):
            image_path = self.image_paths[self.index]
            img = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(img)

            self.timer_label.config(image=self.photo)  # update existing label
            self.index += 1

            # schedule the next image update after 1 second
            self.top.after(1000, self.updateImage)

        else:
            # self.timer_frame.destroy()
            self.makePlayActionScreen(self.redPlayers, self.greenPlayers)


    def makePlayActionScreen(self, redPlayers, greenPlayers): #call this func to make the rest of play action screen after 30 sec timer
        #title that tells you what to do
        titleFrame = tk.Frame(self.top, bg="black")
        titleLabel = tk.Label(titleFrame, text="Play Action Screen", font=("Arial", 16), fg="blue", bg="black")
        titleLabel.pack(pady=5)
        titleFrame.pack(pady=5, padx=50)

        # teams Frame that both teams go into
        teamsFrame = tk.Frame(self.top, bg="black")
        teamsFrame.pack(fill="both", expand=True, side=tk.TOP)

        # need to center redTeam, and greenTeam frame
        teamsFrameCenter = tk.Frame(teamsFrame, bg="black")
        teamsFrameCenter.pack(padx=5, pady=5, expand=True)

        # Red Team
        redTeam = tk.Frame(teamsFrameCenter, bg="red")
        tk.Label(redTeam, text="Red Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        redTeam.pack(padx=50, pady=0, side=tk.LEFT, fill="y")

        # Green Team
        greenTeam = tk.Frame(teamsFrameCenter, bg="green")
        tk.Label(greenTeam, text="Green Team", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        greenTeam.pack(padx=50, pady=0, side=tk.LEFT, fill="y")

        # lets make the teams appear on screen
        self.makeScoreboard(redTeam, redPlayers, True)
        self.makeScoreboard(greenTeam, greenPlayers, False)

        # lets add total for red team at the bottom
        redTotalFrame = tk.Frame(redTeam, bg="white")
        redTotalFrame.pack(pady=5, padx=5, side=tk.BOTTOM)

        #what the redTotalFrame houses
        redTotalLabel = tk.Label(redTotalFrame, text="Team Total:", bg="white", fg="black")
        redTotalLabel.pack(side=tk.LEFT) 
        self.redTotalEntry = tk.Entry(redTotalFrame, width=15, state=tk.DISABLED, textvariable=self.redTotalScore) 
        self.redTotalEntry.pack(side=tk.LEFT)

        # lets add total for green team at the bottom
        greenTotalFrame = tk.Frame(greenTeam, bg="white")
        greenTotalFrame.pack(pady=5, padx=5, side=tk.BOTTOM)

        #what the greenTotalFrame houses
        greenTotalLabel = tk.Label(greenTotalFrame, text="Team Total:", bg="white", fg="black")
        greenTotalLabel.pack(side=tk.LEFT) 
        self.redTotalEntry = tk.Entry(greenTotalFrame, width=15, state=tk.DISABLED, textvariable=self.greenTotalScore) 
        self.redTotalEntry.pack(side=tk.LEFT)

        # lets create the current action frame
        currentAction = tk.Frame(self.top, bg="black")
        currentAction.pack(padx=10, pady=20, fill="both")

        #TODO make it where it reports game action, (game hits, etc) (LATER SPRINT!!!!)
        
        
        #TODO make a frame for time remaining, don't have to code anything... (SPRINT 3!!!)

    def makeScoreboard(self, teamFrame, team, teamTF):
        for i in range(15):
            if(team[str(i)][1].get() != ""):
                self.playerScoreSlot(teamFrame, team[str(i)][1].get(), i, teamTF)

    def playerScoreSlot(self, teamFrame, playerCodename, playerNum, teamTF): #gotta work on this
        frame = tk.Frame(teamFrame, bg=teamFrame["bg"]) #creats the player lines in the team...
        frame.pack(pady=2, fill="both")                              #arrow, number, text, text longer

        name = tk.Label(frame, text=playerCodename, bg=teamFrame["bg"], fg="white")
        name.pack(side=tk.LEFT, padx=2)

        if(teamTF): 
            tk.Entry(frame, width=5, state=tk.DISABLED, textvariable=self.redScores[str(playerNum)][0]).pack(side=tk.RIGHT, padx=2)
        else:
            tk.Entry(frame, width=5, state=tk.DISABLED, textvariable=self.greenScores[str(playerNum)][0]).pack(side=tk.RIGHT, padx=2)

    def closeWindow(self):
        self.result = self.changeEntry.get()
        self.top.destroy()

    def centerWindow(self): #acually kinda neat, but yes, it centers the window
        self.top.update_idletasks()  
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.top.geometry(f"+{x}+{y}")


