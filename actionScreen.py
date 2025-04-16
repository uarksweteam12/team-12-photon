import tkinter as tk
from tkinter import Toplevel
from pathlib import Path
from PIL import Image, ImageTk
import os
import time
import threading
import udpClient
import random
import pygame # audio playback



class ActionScreen:
    def __init__(self, root, redPlayers, greenPlayers, debug):
        self.top = Toplevel(root)  # dont rlly know why but I'm not asking
        self.top.title("Play Action Screen")
        self.top.configure(bg="black")
        self.top.transient(root)  
        self.top.grab_set() #I think it makes you not click out of window unless you complete task

        # Set pygame mixer for audio playback
        pygame.mixer.init()

        # Set the folder path
        self.tracks = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photon_tracks")

        # Keep track if music playing
        self.music_playing = False

        self.redPlayers = redPlayers
        self.greenPlayers = greenPlayers

        # 0=score, 1=hardWareID (sprint 4 thing...but I'm not doing that rn...)
        self.redScores = {str(i): [tk.IntVar(), tk.IntVar(), tk.StringVar()] for i in range(15)}
        self.greenScores = {str(i): [tk.IntVar(), tk.IntVar(), tk.StringVar()] for i in range(15)}

        self.redTotalScore = tk.IntVar()
        self.greenTotalScore = tk.IntVar()

        # For countdownTimer
        self.remaining_seconds = 6 * 60
        
        # 30 second timer starts here
        if(not debug): #if debug=false, act normal
            self.createCountdown()
        else: #if debug=true, skip countdown to speed up development (or else we have to wait 30s to text screen)
            self.makePlayActionScreen(self.redPlayers, self.greenPlayers)

        udpClient.setActionScreen(self)

        # this must be at the end of the __init__ function, don't move!
        self.centerWindow()
        self.top.wait_window(self.top)

    def play_random_track(self):
        """Select and play random track from photon_tracks"""
        if not os.path.exists(self.tracks):
            print(f"Error: Tracks folder not found at {self.tracks}")
            return
        
        mp3_files = [f for f in os.listdir(self.tracks) if f.endswith ('.mp3')]

        if not mp3_files:
            print(f"No mp3 files found at {self.tracks}")
            return
        
        # Selec a random track
        random_track = random.choice(mp3_files)
        track_path = os.path.join(self.tracks, random_track)

        # Play the track
        try:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.music_playing = True
            print (f"Now Playing: {random_track}")

            # Set up a callback to play another random track when one finishes
            self.check_music_ended()
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def check_music_ended(self):
        """Check if the current track has ended and play another if it has"""
        #if self.music_playing and not pygame.mixer.music.get_busy():
        #    self.play_random_track()
        
        # Check again 1 sec intervals
        if self.music_playing:
            self.top.after(1000, self.check_music_ended)
    
    def stop_music(self):
        """Stop the currently playing music"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def on_close(self):
        """Handle actionScreen Closing"""
        self.stop_music()
        self.closeWindow()

    def createCountdown(self):
        self.background = Image.open("countdown_images/background.tif")
        self.background_img = ImageTk.PhotoImage(self.background)

        self.background_label = tk.Label(self.top, image=self.background_img)
        self.background_label.pack(fill="both") # positioning for background_label

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
        self.timer_label = tk.Label(self.top, bg="black", bd=0, highlightthickness=0)
        self.timer_label.place(relx=0.501, rely=0.581, anchor='center') # positioning for timer_label
        # self.timer_label.pack()
        self.updateImage() # self.frame.destroy() and self.makePlayActionScreen() are called in this function

    def updateImage(self):
        if self.index < len(self.image_paths):
            image_path = self.image_paths[self.index]
            img = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(img)

            self.timer_label.config(image=self.photo)  # update existing label
            self.index += 1

            print(self.index)
            if self.index == 14:
                self.play_random_track()

            # schedule the next image update after 1 second
            self.top.after(1000, self.updateImage)
        else:
            self.timer_label.destroy()
            self.background_label.destroy()
            self.makePlayActionScreen(self.redPlayers, self.greenPlayers)

    def countdownTimer(self):
        if self.remaining_seconds >= 0:
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            self.timeRemainText.config(text=f"Time Remaining: {minutes}:{seconds:02}")
            self.remaining_seconds -= 1
            self.top.after(1000, self.countdownTimer)
        else: #end the game
            udpClient.endGame()
            self.timeRemainText.config(text="Game Has Ended\nClose Window to Return to Entry Screen")

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

        totalScoreStyle = {
            "width": 8,
            "state": tk.DISABLED,
            "font": ("Arial", 14, "bold"),
            "justify": "center",
            "disabledbackground": "white",
            "disabledforeground": "black",
            "relief": tk.FLAT,
            "highlightthickness": 0,
            "bd": 0
        }

        # Red team total
        self.redTotalFrame = tk.Frame(redTeam, bg="white")
        self.redTotalFrame.pack(pady=5, padx=5, side=tk.BOTTOM)

        redTotalLabel = tk.Label(self.redTotalFrame, text="Team Total:", bg="white", fg="black", font=("Arial", 12))
        redTotalLabel.pack(side=tk.LEFT)
        self.redTotalEntry = tk.Entry(self.redTotalFrame, textvariable=self.redTotalScore, **totalScoreStyle)
        self.redTotalEntry.pack(side=tk.LEFT)

        # Green team total
        self.greenTotalFrame = tk.Frame(greenTeam, bg="white")
        self.greenTotalFrame.pack(pady=5, padx=5, side=tk.BOTTOM)

        greenTotalLabel = tk.Label(self.greenTotalFrame, text="Team Total:", bg="white", fg="black", font=("Arial", 12))
        greenTotalLabel.pack(side=tk.LEFT)
        self.greenTotalEntry = tk.Entry(self.greenTotalFrame, textvariable=self.greenTotalScore, **totalScoreStyle)
        self.greenTotalEntry.pack(side=tk.LEFT)

        # lets create the current action frame
        currentAction = tk.Frame(self.top, bg="#414141")
        currentAction.pack(padx=10, pady=20, fill="both")

        currentActionLabel = tk.Label(currentAction, text="Current Game Action:", font=("Arial", 14), fg="white", bg="#414141")
        currentActionLabel.pack(padx=10, pady=10, side=tk.TOP)

        currentActionEvents = tk.Frame(currentAction, bg="grey", width=200, height=150)
        currentActionEvents.pack(fill="both")

        #TODO make it where it reports game action, (game hits, etc) (LATER SPRINT!!!!)
        self.eventsLabels = []
        for i in range(5):
            label = tk.Label(currentActionEvents, bg="grey", text='...', font=("Arial", 12), anchor="w")
            label.pack(fill="x", padx=2, pady=2)
            self.eventsLabels.append(label)
        
        #TODO make a frame for time remaining, don't have to code anything... (SPRINT 3!!!)
        self.timeRemainFrame = tk.Frame(self.top, bg="#414141")
        self.timeRemainFrame.pack(padx=10, pady=10, fill="both")
        self.timeRemainText = tk.Label(self.timeRemainFrame, text="Time Remaining: 6:00", font=("Arial", 14), fg="white", bg="#414141")
        self.timeRemainText.pack(padx=10, pady=10)

        self.countdownTimer()
        self.top.after(1000, udpClient.startGame)


    def makeScoreboard(self, teamFrame, team, teamTF):
        for i in range(15):
            if(team[str(i)][1].get() != ""):
                self.playerScoreSlot(teamFrame, team[str(i)][1].get(), i, teamTF, team[str(i)][2].get())

    def playerScoreSlot(self, teamFrame, playerCodename, playerNum, teamTF, playerHardwareID):
        frame = tk.Frame(teamFrame, bg=teamFrame["bg"])
        frame.pack(pady=2, fill="both")

        base_style = {
            "width": 5,
            "state": tk.DISABLED,
            "font": ("Arial", 18, "bold"),
            "justify": "center",
            "disabledbackground": teamFrame["bg"],
            "disabledforeground": "yellow",
            "relief": tk.FLAT,
            "highlightthickness": 0,
            "bd": 0
        }

        if teamTF:  # red team
            tk.Entry(frame, textvariable=self.redScores[str(playerNum)][2], **base_style).pack(side=tk.LEFT, padx=2)
        else:  # green team
            tk.Entry(frame, textvariable=self.greenScores[str(playerNum)][2], **base_style).pack(side=tk.LEFT, padx=2)

        name = tk.Label(frame, text=playerCodename, bg=teamFrame["bg"], fg="white", font=("Arial", 12))
        name.pack(side=tk.LEFT, padx=2)

        score_style = {
            "width": 5,
            "state": tk.DISABLED,
            "font": ("Arial", 14, "bold"),
            "justify": "center",
            "disabledbackground": teamFrame["bg"],
            "disabledforeground": "white",
            "relief": tk.FLAT,
            "highlightthickness": 0,
            "bd": 0
        }

        if teamTF:  # red team
            tk.Entry(frame, textvariable=self.redScores[str(playerNum)][0], **score_style).pack(side=tk.RIGHT, padx=2)
            self.redScores[str(playerNum)][1].set(playerHardwareID)
        else:  # green team
            tk.Entry(frame, textvariable=self.greenScores[str(playerNum)][0], **score_style).pack(side=tk.RIGHT, padx=2)
            self.greenScores[str(playerNum)][1].set(playerHardwareID)



    def closeWindow(self):
        self.result = self.changeEntry.get()
        self.top.destroy()
        global udpClient
        udpClient.endGame()

    def centerWindow(self): #acually kinda neat, but yes, it centers the window
        self.top.update_idletasks()  
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.top.geometry(f"+{x}+{y}")


