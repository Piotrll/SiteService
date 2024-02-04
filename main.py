import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os, sys, shutil, time
import winLib, conf

class Controler:
    def __init__(self):
        self.globalCwd = os.getcwd()
        self.configHandle = None
        self.initWindow = None

        if not self.startup():
            print("Startup failed.")
            sys.exit()

    def startup(self):

        # Initialize configuration
        print("Initializing configuration...")
        configHandle = conf.ConfigHandle(self)
        if not configHandle.startupSequence():
            return False
        print("Configuration initialized.")

        # Initialize main window
        print("Initializing main window...")
        initWindow = winLib.initWindow(controler = self, configHandle = configHandle)

if __name__ == "__main__":
    controler = Controler()