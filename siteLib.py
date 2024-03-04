import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os, sys, shutil, time, io
import winLib, conf, tmpMem

class Site:
    def __init__(self, snum, name, issues, controler):
        self.snum = snum
        self.name = name
        self.issues = issues
        self.controler = controler

    def edit(self, name, snum, issues):
        self.snum = snum
        self.name = name
        self.issues = issues
        self.controler.applyChanges(self)

class Issue:
    def __init__(self, )