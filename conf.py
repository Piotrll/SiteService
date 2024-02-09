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
        self.dataDir = None
        self.dataDirPath = None
        self.issueFolderName = None
        self.issueArchiveFolderName = None
    def startupSequence(self):
        match self.configChecker.initCheck():
            case 0:
                pass
            case 1 | 2:
                self.noConfigData = True
            case 3:
                print("Error initializing configuration.")
                return False
        if self.noConfigData:
            winLib.askInitImport(self, self.controler)
        self.loadDataDirectory()
        self.noConfigData = False
        print("Configuration startup sequence completed.")
        return True
    
    def saveDataDirectory(self):
        self.configWriter.writeConfig("DataInfo", "dataPath", self.dataDirPath)
    def loadDataDirectory(self):
        self.dataDirPath = self.configReader.readConfig("DataInfo", "dataPath")
        self.dataDir = os.path.basename(self.dataDirPath)
        self.issueFolderName = self.configReader.readConfig("DataInfo", "issuefoldername")
        self.issueArchiveFolderName = self.configReader.readConfig("DataInfo", "issuearchivefoldername")


class cWriter:
    def __init__(self, configHandle):
        self.configHandle = configHandle

    def writeConfig(self, section, option, value):
        os.chdir(os.path.join(self.configHandle.controler.globalCwd, "config"))
        configHandle = cp.ConfigParser()
        configHandle.read("config.ini")
        configHandle[section][option] = value
        with open("config.ini", "w") as configFile:
            configHandle.write(configFile)
        return True

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

    def readConfig(self, section, option):
        os.chdir(os.path.join(self.configHandle.controler.globalCwd, "config"))
        tempHandle = cp.ConfigParser()
        tempHandle.read("config.ini")
        return tempHandle[section][option]

class cChecker:
    def __init__(self, configHandle):
        self.configHandle = configHandle
        self.res = True
    def initCheck(self): # returns 0 if config exists, 1 if config exist but have no data, 2 if config was created, 3 if error

        os.chdir(self.configHandle.controler.globalCwd)
        if os.path.exists("config"):
            print("Config directory exists.")
            if not os.path.exists(self.configHandle.configReader.readConfig("DataInfo", "dataPath")):
                print("Data directory does not exist.")
                return 1
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
                return 3
            print("Config file created.")
        return 2