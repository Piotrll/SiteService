import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter import filedialog
import os, sys, shutil, time

class MainWin:
    def __init__(self, controler, configHandle, memory):
        self.controler = controler
        self.configHandle = configHandle
        self.memory = memory
        
        self.dataDirPath = self.configHandle.dataDirPath
        self.dataDir = self.configHandle.dataDir

    def buildWindow(self):
        # Main window
        # Background is gray, writing cursor is white

        self.root = tk.Tk()
        self.root.title("Serwis")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg = "gray")

        self.mainFrame = tk.Frame(self.root, bg = "gray")
        self.mainFrame.pack()
        self.label1 = tk.Label(self.mainFrame, text="Serwis", bg = "gray", fg = "white", font = ("Arial", 24))
        self.label1.grid(column=0, row=0, columnspan=3, pady=10)
    
    def startup(self):
        self.root.mainloop()

    def drawActionButtons(self):
        self.button1 = tk.Button(self.mainFrame, text="Import", command=self.runtimeImport, bg = "gray", fg = "white", font = ("Arial", 16))
        self.button1.grid(column=0, row=1, padx=10, pady=10)
        self.button2 = tk.Button(self.mainFrame, text="Excel", command=self.makeExcel, bg = "gray", fg = "white", font = ("Arial", 16))
        self.button2.grid(column=1, row=1, padx=10, pady=10)
        self.button3 = tk.Button(self.mainFrame, text="Odśwież", command=self.refreshData, bg = "gray", fg = "white", font = ("Arial", 16))
        self.button3.grid(column=2, row=1, padx=10, pady=10)

    def buildTreeView(self):
        self.treeView = ttk.Treeview(self.mainFrame)
        self.treeView.grid(column=0, row=2, columnspan=3, padx=10, pady=10)
        self.treeView["columns"] = ("Serwis", "Obiekt", "Usterki")

    def insertDataToTreeView(self):
        for item in self.memory.mainDataList:
            
            if len(item) == 1:
                issueCount = len(self.memory.issuesDict[item[0]])
                self.treeView.insert("", "end", text=item, values=("", item[0], issueCount))
            else:
                issueCount = len(self.memory.issuesDict[item[0]+"."+item[1]])
                self.treeView.insert("", "end", text=item[0], values=(item[0], item[1], issueCount))
    def runtimeImport(self):
        self.configHandle.dataDirPath = filedialog.askdirectory()

    def makeExcel(self):
        pass

    def refreshData(self):
        pass

class askInitImport:
    def __init__(self, configHandle, controler):
        self.configHandle = configHandle
        self.controler = controler
        self.root = None
        self.buildWindow()

    def buildWindow(self):
        self.root = tk.Tk()
        self.root.title("Importowanie danych")
        self.root.resizable(False, False)
        self.label1 = tk.Label(self.root, text="Pierwsze importowanie danych obiektów.")
        self.label1.pack()
        self.button1 = tk.Button(self.root, text="Importuj", command=self.importData)
        self.button1.pack()
        self.root.mainloop()

    def importData(self):
        self.root.destroy()
        self.configHandle.dataDirPath = filedialog.askdirectory()
        self.configHandle.saveDataDirectory()
