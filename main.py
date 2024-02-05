import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os, sys, shutil, time
import winLib, conf, tmpMem

class Controler:
    def __init__(self):
        self.globalCwd = os.getcwd()
        self.configHandle = None
        self.initWindow = None
        self.issueWindow = None
        self.memory = None

        if not self.startup():
            print("Startup failed.")
            sys.exit()

    def startup(self):

        # Initialize configuration
        print("Initializing configuration...")
        self.configHandle = conf.ConfigHandle(self)
        if not self.configHandle.startupSequence():
            return False
        print("Configuration initialized.")

        # Initialize memory
        self.memory = tmpMem.Memory(self, self.configHandle)
        self.memory.loadData()
        self.memory.loadIssues()
        self.memory.solidifyData()

        # Initialize main window
        print("Initializing main window...")
        self.initWindow = winLib.MainWin(controler = self, configHandle = self.configHandle, memory = self.memory)
        self.initWindow.buildWindow()
        self.initWindow.drawActionButtons()
        self.initWindow.buildTreeView()
        self.initWindow.drawSearchBar()
        self.initWindow.insertDataToTreeView()
        self.initWindow.buildContextMenu()
        self.initWindow.binder()

        # Initialize issue window
        self.issueWindow = winLib.IssueWin(controler = self, configHandle = self.configHandle, memory = self.memory, mainWin = self.initWindow)

        self.initWindow.startup()
        return True

if __name__ == "__main__":
    controler = Controler()