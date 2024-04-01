import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os, sys, shutil, time, io
import winLib, conf, tmpMem

class Controler:
    def __init__(self):
        self.globalCwd = os.getcwd()
        self.globalCwd = self.globalCwd.replace("\\", "/")
        self.configHandle = None
        self.initWindow = None
        self.issueWindow = None
        self.memory = None

        try:
            self.startup()
        except Exception as e:
            print(f"Startup failed.{e}")
            # Wait with closing the program, paste all lines into error log
            self.raiseError()
            sys.exit()
        self.closeSession()
        sys.exit()

    def startup(self):
        # Initialize log buffer
        self.startLog()
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

    def startLog(self):
        # Get all printed lines and paste them into error log
        self.LogBuffer = io.StringIO()
        self.ErrorBuffer = io.StringIO()
        sys.stdout = self.LogBuffer
        sys.stderr = self.ErrorBuffer
        print("Log buffer started.")

    def raiseError(self):
        # Get all printed lines and paste them into error log
        timeNow = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        if not os.path.exists(self.globalCwd + "/bledy"):
            os.mkdir(self.globalCwd + "/bledy")
        os.chdir(self.globalCwd + "/bledy")
        with open("logi " + timeNow +".txt", "w+", encoding="utf-8") as file:
            if self.LogBuffer.getvalue() == "":
                file.write("Log: \n\n")
                file.write("No log lines.")
            else:
                file.write("Log: \n\n")
                file.write(self.LogBuffer.getvalue())
            if self.ErrorBuffer.getvalue() == "":
                file.write("\n\n Error log: \n\n")
                file.write("No error lines.")
            else:
                file.write("\n\n Error log: \n\n")
                file.write(self.ErrorBuffer.getvalue())
            file.close()
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        self.LogBuffer.close()
        self.ErrorBuffer.close()
        os.chdir(self.globalCwd)
    
    def closeSession(self):
        timeNow = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        if not os.path.exists(self.globalCwd + "/logi"):
            os.mkdir(self.globalCwd + "/logi")
        os.chdir(self.globalCwd + "/logi")
        with open("logi " + timeNow +".txt", "w+", encoding="utf-8") as file:
            if self.LogBuffer.getvalue() == "":
                file.write("Log: \n\n")
                file.write("No log lines.")
            else:
                file.write("Log: \n\n")
                file.write(self.LogBuffer.getvalue())
            if self.ErrorBuffer.getvalue() == "":
                file.write("\n\n Error log: \n\n")
                file.write("No error lines.")
            else:
                file.write("\n\n Error log: \n\n")
                file.write(self.ErrorBuffer.getvalue())
            file.close()
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        self.LogBuffer.close()
        self.ErrorBuffer.close()
        os.chdir(self.globalCwd)

if __name__ == "__main__":
    controler = Controler()
    

