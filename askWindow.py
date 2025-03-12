import tkinter as tk
from tkinter import Toplevel

class AskWindow:
    def __init__(self, root, operation): #operation=True, ask codename, operation=False, ask hardwareid
        if operation:
            title = "Code Name Prompt"
            titleFrameText = "Code ID not found in database\nPlease enter Code Name below"
            entryText = "Code Name:"
        else:
            titleFrameText = "Please enter Hardware ID for player below"
            title = "Hardware ID Prompt"
            entryText = "Hardware ID:"
        
        self.top = Toplevel(root)  # dont rlly know why but I'm not asking
        self.top.title(title)
        self.top.configure(bg="black")
        self.top.transient(root)  
        self.top.grab_set() #I think it makes you not click out of window unless you complete task

        self.result = None

        # you can also press the enter key to close window
        self.top.bind("<Return>", self.onKeyPress)

        #title that tells you what to do
        titleFrame = tk.Frame(self.top, bg="black")
        titleLabel = tk.Label(titleFrame, text=titleFrameText, font=("Arial", 16), fg="blue", bg="black")
        titleLabel.pack(pady=5)
        titleFrame.pack(pady=5, padx=5)

        #the frame that houses all the stuff like label, entry, and button
        changeFrame = tk.Frame(self.top, bg="grey")
        changeFrame.pack(pady=5, padx=5)

        #what the changeFrame houses
        changeLabel = tk.Label(changeFrame, text=entryText, bg="grey", fg="black")
        changeLabel.pack(side=tk.LEFT) 
        self.changeEntry = tk.Entry(changeFrame, width=15) #need self. to get ip from text entry in the changeIP func
        self.changeEntry.pack(side=tk.LEFT)
        changeSubmit = tk.Button(changeFrame, text="Confirm", command=self.closeWindow, bg="grey")
        changeSubmit.pack(side=tk.LEFT, padx=3, pady=2)
        self.changeEntry.focus_set()

        #lets center window so ppl see this pop up
        self.centerWindow()

        self.top.wait_window(self.top)

    def onKeyPress(self, event):
        self.closeWindow()

    def closeWindow(self):
        self.result = self.changeEntry.get()
        self.top.destroy()

    def getResult(self):
        return self.result

    def centerWindow(self): #acually kinda neat, but yes, it centers the window
        self.top.update_idletasks()  
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.top.geometry(f"+{x}+{y}")