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
                temp = item.split(".")
                tempList.append(temp[0])
                tempList.append(temp[1])
            self.mainDataList.append(tempList)
            print(f"Loading object - {tempList}")
            tempList = []

        print("Data loaded.")

    def loadIssues(self):
        os.chdir(self.controler.globalCwd)

        issuesFolder = self.configHandle.configReader.readConfig("DataInfo", "issueFolderName")

        for i, item in enumerate(self.rawSiteNames):


            os.chdir(self.configHandle.dataDirPath + '/' + item)
            if not os.path.exists(issuesFolder):
                os.mkdir(issuesFolder)

            os.chdir(self.configHandle.dataDirPath + '/' + item )
            issuesHere = os.listdir(self.configHandle.dataDirPath + '/' + item + '/' + issuesFolder)
            path = self.configHandle.dataDirPath + '/' + item + '/' + issuesFolder
            tempList = []
            for issue in issuesHere:
                if os.path.isfile(path + '/' + issue):
                    tempList.append(issue)
            self.issuesDict[item] = tempList
            print(f"Loading issues for {item} - {tempList}")
            os.chdir(self.controler.globalCwd)
        print("Issues loaded.")

    def solidifyData(self):
        os.chdir(self.controler.globalCwd)
        if not os.path.exists("backup"):
            os.mkdir("backup")
        os.chdir("backup")
        
        with open("dataBackup.txt", "w") as backupFile:
            for item in self.rawSiteNames:
                backupFile.write(f"{item}\n")
                backupFile.write(f"{self.issuesDict[item]}\n")
        print("Backup created.")

    def flushData(self):
        self.mainDataList = []
        self.issuesDict = {}

    def solidifyData(self):
        pass

