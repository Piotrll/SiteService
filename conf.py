import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os, sys, shutil, time
import configparser as cp
import winLib

class ConfigHandle:
    def __init__(self, controler):
        self.controler = controler
        self.configWriter = cWriter(self)
        self.configReader = cReader(self)
        self.configChecker = cChecker(self)
        self.noConfigData = False

    def startupSequence(self):
        match self.configChecker.initCheck():
            case 0:
                pass
            case 1:
                self.noConfigData = True
            case 2:
                print("Error initializing configuration.")
                return False
        if self.noConfigData:
            winLib.askInitImport(self, self.controler)

class cWriter:
    def __init__(self, configHandle):
        self.configHandle = configHandle

    def writeInitConfig(self):
        initialConfigStructure = {
            "General": {
                "globalCwd": self.configHandle.controler.globalCwd
            },
            "DataInfo": {
                "dataPath": "",
                "issueFolderName": "Usterki",
                "issueArchiveFolderName": "ArchiwumUsterek",
            }
        }

        tempHandle = cp.ConfigParser()
        tempHandle.read_dict(initialConfigStructure)
        os.chdir(os.path.join(self.configHandle.controler.globalCwd, "config"))
        with open("config.ini", "w") as configFile:
            tempHandle.write(configFile)
        return True


class cReader:
    def __init__(self, configHandle):
        self.configHandle = configHandle

    def readConfig(self):
        pass

class cChecker:
    def __init__(self, configHandle):
        self.configHandle = configHandle
        self.res = True
    def initCheck(self): # returns 0 if config directory exists, 1 if config file exists, 2 if error

        os.chdir(self.configHandle.controler.globalCwd)
        if os.path.exists("config"):
            print("Config directory exists.")
            return 0
        else:
            print("Config directory does not exist.")
            os.mkdir("config")
            print("Config directory created.")
        os.chdir("config")
        if os.path.exists("config.ini"):
            print("Config file exists.")
        else:
            print("Config file does not exist.")
            self.res = self.configHandle.configWriter.writeInitConfig()
            if self.res:
                print("Config file created.")
            else:
                print("Error creating config file.")
                return 2
            print("Config file created.")
        return 1