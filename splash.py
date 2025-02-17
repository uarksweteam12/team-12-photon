import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import playerEntryScreen

# Splash Screen
class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hides main window (for now)

        self.splash = Toplevel() # Creates a window on top basically
        self.splash.overrideredirect(True)  # Removes window borders

        # Load and display the logo
        self.logo = Image.open("logo.png")
        self.logo = ImageTk.PhotoImage(self.logo)

        self.splash_label = tk.Label(self.splash, image=self.logo, borderwidth=0)
        self.splash_label.pack()

        # Position splash screen in the center
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f"+{x}+{y}")

        # Closes splash screen and after 2 seconds, opens playerEntry
        self.splash.after(2000, self.showApp)

    # Destroys splash screen and shows player entry
    def showApp(self):
        self.splash.destroy()
        self.root.deiconify()
        playerEntryScreen.PlayerEntryScreen(self.root) #opens the playerEntryScreen

# Main App
class MainApp:
    def __init__(self, root):
        pass

root = tk.Tk()
SplashScreen(root)
MainApp(root)
root.mainloop()