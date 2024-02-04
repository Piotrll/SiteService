import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter import filedialog
import os, sys, shutil, time

class initWindow:
    def __init__(self, controler, configHandle):
        self.controler = controler
        self.configHandle = configHandle
        
        self.dataDirPath = self.configHandle.dataDirPath
        self.dataDir = self.configHandle.dataDir

        """self.startup()
        self.buildWindow()
    
    def startup(self):
        self.root = tk.Tk()
        self.root.title("Serwis")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#003333")
        self.root.mainloop()"""

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
