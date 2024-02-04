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
        self.root.title("Kapeo Serwis")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.config(bg="#333333")

        self.label1 = tk.LabelFrame(self.root, text="Serwis", bg="#333333", fg="#ffffff", font=("Arial", 16, "bold"), bd=5, relief=tk.FLAT)
        self.label1.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=10)
        self.treeFrame = tk.Frame(self.root, bg = "gray")
        self.treeFrame.pack(fill=tk.BOTH, expand=True)
    
    def startup(self):
        self.root.mainloop()

    def drawActionButtons(self):
        self.button1 = tk.Button(self.label1,command=self.runtimeImport, text="Import",
                                 activebackground="red", bg="#993333", fg="#ffffff", 
                                 font=("Arial", 16, "bold"), bd=5, relief=tk.FLAT,)
        self.button1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        self.button2 = tk.Button(self.label1,command=self.makeExcel, text="Excel",
                                 activebackground="red", bg="#993333", fg="#ffffff",
                                 font=("Arial", 16, "bold"), bd=5, relief=tk.FLAT,)
        self.button2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        self.button3 = tk.Button(self.label1, text="Odśwież",activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.refreshData)
        self.button3.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

    def buildTreeView(self):
        self.treeView = ttk.Treeview(self.treeFrame, selectmode="browse", columns=("Serwis", "Obiekt", "Usterki"))
        self.treeView.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.treeView["columns"] = ("Serwis", "Obiekt", "Usterki")
        self.treeView['show'] = 'headings'
        self.treeView.column("Serwis", width=10, anchor="center")
        self.treeView.column("Obiekt", width=100, anchor="center")
        self.treeView.column("Usterki", width=100, anchor="center")
        self.treeView.heading("Serwis", text="Serwis")
        self.treeView.heading("Obiekt", text="Obiekt")
        self.treeView.heading("Usterki", text="Usterki")

    def insertDataToTreeView(self):
        for item in self.memory.mainDataList:
            
            if len(item) == 1:
                issueCount = len(self.memory.issuesDict[item[0]])
                self.treeView.insert("", "end", text=item, values=("", item[0], issueCount))
            else:
                issueCount = len(self.memory.issuesDict[item[0]+"."+item[1]])
                self.treeView.insert("", "end", text=item[0], values=(item[0], item[1], issueCount))

    def flushTreeView(self):
        for item in self.treeView.get_children():
            self.treeView.delete(item)

    def runtimeImport(self):
        self.configHandle.dataDirPath = filedialog.askdirectory()
        self.configHandle.saveDataDirectory()
        self.memory.loadData()
        self.memory.loadIssues()
        self.flushTreeView()
        self.insertDataToTreeView()

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
