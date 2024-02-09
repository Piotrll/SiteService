import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter import filedialog
import os, sys, shutil, time

class Memory:
    def __init__(self, controler, configHandle):
        self.controler = controler
        self.configHandle = configHandle
        self.loadWin = None
        self.mainDataList = []
        self.issuesDict = {}
        self.actualDataView = []
        self.rawSiteNames = []
        self.mainWin = None
    
    def setMainWin(self, mainWin):
        self.mainWin = mainWin

    def loadData(self):
        self.flushData()
        
        dataList = os.listdir(self.configHandle.dataDirPath)
        tempList = []

        for item in dataList:

            if not os.path.isdir(os.path.join(self.configHandle.dataDirPath, item)):
                continue
            self.rawSiteNames.append(item)
            
            if not "." in item:
                tempList.append(item)
            elif item.index(".") > 5:
                temp = item
                tempList.append(temp)
            else:
                temp = item.split(".", 1)
                tempList.append(temp[0])
                tempList.append(temp[1])
            self.mainDataList.append(tempList)
            print(f"Loading object - {tempList}")
            tempList = []

        print("Data loaded.")

    def loadIssues(self):
        os.chdir(self.controler.globalCwd)

        issuesFolder = self.configHandle.issueFolderName

        for i, item in enumerate(self.rawSiteNames):
            if not os.path.exists(self.configHandle.dataDirPath + '/' + item + '/' + issuesFolder):
                os.mkdir(issuesFolder)
                self.issuesDict[item] = []
                print(f"Loading issues for {item}")
                continue
            else:
                issuesHere = os.listdir(self.configHandle.dataDirPath + '/' + item + '/' + issuesFolder)
            path = self.configHandle.dataDirPath + '/' + item + '/' + issuesFolder
            

            if len(issuesHere) == 0:
                self.issuesDict[item] = []
                print(f"Loading issues for {item}")
                continue
            tempList = []

            for issue in issuesHere:
                if os.path.isfile(path + '/' + issue):
                    tempList.append(issue)
            self.issuesDict[item] = tempList
            print(f"Loading issues for {item} - {tempList}")
        print("Issues loaded.")

    def solidifyData(self):
        os.chdir(self.controler.globalCwd)
        if not os.path.exists("backup"):
            os.mkdir("backup")
        os.chdir("backup")
        
        with open("dataBackup.txt", "w") as backupFile:
            for item in self.rawSiteNames:
                backupFile.write(f"Obiekt {item}\n")
                backupFile.write(f"Usterki {self.issuesDict[item]}\n")
        print("Backup created.")

    def flushData(self):
        self.mainDataList = []
        self.issuesDict = {}
        self.rawSiteNames = []

