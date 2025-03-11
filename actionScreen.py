import tkinter as tk
from tkinter import Toplevel


class ActionScreen:
    def __init__(self, root, redPlayers, greenPlayers):
        self.top = Toplevel(root)  # dont rlly know why but I'm not asking
        self.top.title("Play Action Screen")
        self.top.configure(bg="black")
        self.top.transient(root)  
        self.top.grab_set() #I think it makes you not click out of window unless you complete task

        #title that tells you what to do
        titleFrame = tk.Frame(self.top, bg="black")
        titleLabel = tk.Label(titleFrame, text="Play Action Screen", font=("Arial", 16), fg="blue", bg="black")
        titleLabel.pack(pady=5)
        titleFrame.pack(pady=5, padx=5)


        # ****
        # PUT ALL THE CODE FOR THE PLAY ACTION SCREEN HERE!!!
        # ****





        # This must be at the end of the __init__ function, don't move!
        self.centerWindow()
        self.top.wait_window(self.top)

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


