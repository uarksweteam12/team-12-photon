from tkinter import *
from PIL import Image, ImageTk
import playerEntryScreen

splash_root = Tk()
imgSize = (300,300) ### Change size
imageSelected = 'logo.png' ### Change image

splash_root.overrideredirect(True)
splash_root.wm_attributes('-transparentcolor', 'black')

# Load and display the logo
logo = Image.open(imageSelected)
logoSize = logo.resize(imgSize)
logo = ImageTk.PhotoImage(logoSize)
splash_label = Label(splash_root, image=logo, bg='black')
splash_label.pack()

# Center window
appWidth = 300
appHeight = 300
screenWidth = splash_root.winfo_screenwidth()
screenHeight = splash_root.winfo_screenheight()
trueX = (screenWidth/2) - (appWidth/2)
trueY = (screenHeight/2) - (appHeight/2)

splash_root.geometry(f'{appWidth}x{appHeight}+{int(trueX)}+{int(trueY)}')

# Function to destroy splash and open player entry screen
def showApp():
    splash_root.destroy()
    root = Tk()
    # Center window
    appWidth = 1000
    appHeight = 750
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    trueX = (screenWidth/2) - (appWidth/2)
    trueY = (screenHeight/2) - (appHeight/2)

    root.geometry(f'{appWidth}x{appHeight}+{int(trueX)}+{int(trueY)}')
    playerEntryScreen.PlayerEntryScreen(root)  # Opens the playerEntryScreen

# Call showApp after 2 seconds
splash_root.after(2000, showApp)
mainloop()
