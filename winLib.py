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

    # Initialize methods
    #-------------------------------------------------------------------------
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
        self.searchFrame = tk.Frame(self.root, bg = "gray")
        self.searchFrame.pack(fill=tk.BOTH, expand=False)
    
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

    def binder(self):
        self.treeView.bind("<Double-Button-1>", self.enterIssues)
        self.treeView.bind("<Button-3>", self.highlightItem)
        self.treeView.bind("<Button-3>", self.postMenu)

        self.contextMenu.bind('<FocusOut>', self.unPostMenu)
        self.contextMenu.bind('<Leave>', self.unPostMenu)

    def buildTreeView(self):
        self.treeView = ttk.Treeview(self.treeFrame, selectmode="browse", columns=("Serwis", "Obiekt", "Usterki"))
        self.treeView.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.treescroll = ttk.Scrollbar(self.treeFrame, orient="vertical", command=self.treeView.yview)
        self.treescroll.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.treeView.config(yscrollcommand=self.treescroll.set)
        self.treeView["columns"] = ("Serwis", "Obiekt", "Usterki")
        self.treeView['show'] = 'headings'
        self.treeView.column("Serwis", width=100, anchor="center")
        self.treeView.column("Obiekt", width=1080)
        self.treeView.column("Usterki", width=100, anchor="center")
        self.treeView.heading("Serwis", text="Serwis")
        self.treeView.heading("Obiekt", text="Obiekt")
        self.treeView.heading("Usterki", text="Usterki")
        style = ttk.Style(self.root)
        style.map('Treeview',
                background=[('selected', 'red')],
                foreground=[('selected', 'white')])

    def insertDataToTreeView(self):
        for item in self.memory.mainDataList:
            
            if len(item) == 1:
                issueCount = len(self.memory.issuesDict[item[0]])
                self.treeView.insert("", "end", text=item, values=("", item[0], issueCount))
            else:
                issueCount = len(self.memory.issuesDict[item[0]+"."+item[1]])
                self.treeView.insert("", "end", text=item[0], values=(item[0], item[1], issueCount))

    def buildContextMenu(self):
        self.contextMenu = tk.Menu(self.root, tearoff=0)
        self.contextMenu.add_command(label="Edytuj Obiekt", command=self.editSite)
        self.contextMenu.add_command(label="Dodaj Obiekt do Bazy", command=self.addSite)
        self.contextMenu.add_command(label="Do folderu", command=self.openIssueFolder)    

    def drawSearchBar(self):
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.filterTree) 
        self.search_entry = tk.Entry(self.searchFrame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.BOTTOM, expand=False, padx=10, pady=10)

    # Local methods 
    #---------------------------------------------------------------------------
    def unPostMenu(self, event):
        self.context_menu.unpost()

    def postMenu(self, event):
        try:
            item_id = self.treeView.identify('item', event.x, event.y)

            if item_id:
                self.treeView.selection_set(item_id)
                self.contextMenu.post(event.x_root, event.y_root)
        finally:
            self.contextMenu.grab_release()

    def editSite(self):
        editWindow = EditWindow(self, self.configHandle, self.memory)

    def addSite(self):
        pass

    def openIssueFolder(self):
        pass

    # Import requested by button
    def runtimeImport(self):
        self.configHandle.dataDirPath = filedialog.askdirectory()
        self.configHandle.saveDataDirectory()
        self.memory.loadData()
        self.memory.loadIssues()
        self.flushTreeView()
        self.insertDataToTreeView()

    # Highlight item on right click
    def highlightItem(self, event):
        iid = self.treeView.identify_row(event.y)
        if iid:
            self.treeView.selection_set(iid)

    # Filter treeview (deserves its own class, but it's not worth it for now)
    def filterTree(self, *args):
        search = self.search_var.get()
        self.flushTreeView()
        if search == "":
            self.insertDataToTreeView()
        else:
            if search[0] == "=" and len(search) > 1: # Search for exact match in serwis column
                search = search[1:]
                for i, d in enumerate(self.memory.mainDataList):
                    if len(d) == 1:
                        continue
                    else:
                        if search.lower() == d[0].lower():
                            issuecount = len(self.memory.issuesDict[d[0]+"."+d[1]])
                            self.treeView.insert(parent='', index='end', 
                                                iid=i, 
                                                values=(d[0], d[1], issuecount))
                return
            elif search[0] == "!" and len(search) > 1: # Search for issues count
                search = search[1:]
                issuecount = {}
                for i, d in enumerate(self.memory.mainDataList):
                    if len(d) > 1:
                        issuecount[d[0] + "." + d[1]] = len(self.memory.issuesDict[d[0]+"."+d[1]])
                    elif len(d) == 1:
                        issuecount[d[0]] = len(self.memory.issuesDict[d[0]])
                if search.isdigit():
                    search = int(search)
                    for i, d in enumerate(self.memory.mainDataList):
                        if len(d) > 1:
                            if issuecount[d[0] + "." + d[1]] >= search:
                                self.treeView.insert(parent='', index='end', 
                                                iid=i, 
                                                values=(d[0], d[1], issuecount[d[0] + "." + d[1]]))
                        elif len(d) == 1:
                            if issuecount[d[0]] >= search:
                                self.treeView.insert(parent='', index='end', 
                                                iid=i, 
                                                values=("", d[0], issuecount[d[0]]))
            else: # Standard search
                for i, d in enumerate(self.memory.mainDataList):
                    if len(d) == 1:
                        if search.lower() in d[0].lower():
                            issuecount = len(self.memory.issuesDict[d[0]])
                            self.treeView.insert(parent='', index='end', 
                                            iid=i, 
                                            values=("", d[0], issuecount))
                    else:
                        if search.lower() in d[1].lower():
                            issuecount = len(self.memory.issuesDict[d[0]+"."+d[1]])
                            self.treeView.insert(parent='', index='end', 
                                            iid=i, 
                                            values=(d[0], d[1], issuecount))

    def enterIssues(self, event):
        self.controler.issueWindow.startup()

    def makeExcel(self):
        pass

    def refreshData(self):
        self.memory.flushData()
        self.memory.loadData()
        self.memory.loadIssues()
        self.flushTreeView()
        self.insertDataToTreeView()

    # Deep private methods -------------------------------------------------------------
    
    def flushTreeView(self):
        for item in self.treeView.get_children():
            self.treeView.delete(item)


class IssueWin:
    def __init__(self, controler, configHandle, memory, mainWin):
        self.controler = controler
        self.configHandle = configHandle
        self.memory = memory
        self.mainWin = mainWin
        self.addingWindow = None
        self.siteName = None

    def startup(self):
        self.prepareSiteName()
        self.buildWindow()
        self.drawWidgets()
        self.binder()
        self.prepareIssueView()
    
    def buildWindow(self):
        self.root = tk.Toplevel()
        self.root.title("Usterki")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.config(bg="#333333")

    def drawWidgets(self):
        self.label1 = tk.LabelFrame(self.root, text="Usterki", bg="#333333", 
                                    fg="#ffffff", font=("Arial", 16, "bold"), bd=5, 
                                    relief=tk.FLAT)
        self.label1.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=10)

        self.listBox = tk.Listbox(self.root, bg="#333333", fg="#ffffff", 
                                  font=("Arial", 16, "bold"), bd=5, relief=tk.FLAT)
        self.listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.button1 = tk.Button(self.label1, text="Dodaj", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.addIssue)
        self.button1.pack(side=tk.RIGHT, fill=tk.X, expand=False, padx=10, pady=10)

        self.button2 = tk.Button(self.label1, text="Odśwież i zamknij", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.closeWindow)
        self.button2.pack(side=tk.RIGHT, fill=tk.X, expand=False, padx=10, pady=10)

    def binder(self):
        self.root.bind("WM_DELETE_WINDOW", self.closeWindow)

        self.listBox.bind("<Double-Button-1>", self.toIssue)
        self.listBox.bind("<Delete>", self.deleteIssue)

    # Local methods ------------------------------------------------------------
    def closeWindow(self):
        self.mainWin.refreshData()
        self.root.destroy()

    def flushListBox(self):
        self.listBox.delete(0, tk.END)

    def prepareSiteName(self):
        selected = self.mainWin.treeView.selection()[0]
        item = self.mainWin.treeView.item(selected)
        if len(item['values']) < 3:
            value = str(item['values'][0])
        elif len(item['values']) == 3:
            value = str(item['values'][0]) + "." + str(item['values'][1])
        self.siteName = value

    def prepareIssueView(self):
        self.flushListBox()
        if len(self.memory.issuesDict[self.siteName]) == 0:
            self.listBox.insert(tk.END, "Brak usterek.")
        else:
            for issue in self.memory.issuesDict[self.siteName]:
                self.listBox.insert(tk.END, issue)

    def addIssue(self):
        self.addingWindow = NewIssueWin(self.controler, self.configHandle, self.memory, self, self.siteName)
        self.addingWindow.buildWindow()
        self.addingWindow.drawWidgets()
        self.addingWindow.binder()
        self.addingWindow.startup()

    def toIssue(self, event):
        os.chdir(self.configHandle.dataDirPath + '/' + self.siteName + '/' + self.configHandle.issueFolderName)
        path = str(os.getcwd()).replace("\\", "/")
        selected = self.listBox.curselection()[0]
        for issue in self.memory.issuesDict[self.siteName]:
            selected_text = self.listBox.get(selected)
            if selected_text in issue:
                issueName = issue
                os.startfile(path + '/' + issueName)
                break
        os.chdir(self.controler.globalCwd)

    def deleteIssue(self, event):
        self.checkArchiveFolder()
        selected = self.listBox.curselection()[0]
        issueName = self.listBox.get(selected)
        print(f"Commanded deleting issue in {self.siteName} - {issueName}.")

        self.memory.issuesDict[self.siteName].remove(issueName)
        self.listBox.delete(selected)

        os.chdir(os.path.join(self.configHandle.dataDirPath, self.siteName, self.configHandle.issueFolderName))
        print("Current dir: ", os.getcwd())
        print("Archiving: ", issueName)
        shutil.move(self.configHandle.dataDirPath + '/' + self.siteName + '/' + self.configHandle.issueFolderName + '/' + issueName, 
                    self.configHandle.dataDirPath + '/' + self.siteName + '/' + self.configHandle.issueArchiveFolderName)
        os.chdir(self.controler.globalCwd)

    def checkArchiveFolder(self):
        os.chdir(os.path.join(self.configHandle.dataDirPath, self.siteName))
        if not os.path.exists(self.configHandle.issueArchiveFolderName):
            print(f"Creating {self.configHandle.issueArchiveFolderName} in {self.siteName}.")
            os.mkdir(self.configHandle.issueArchiveFolderName)
        os.chdir(self.controler.globalCwd)

class NewIssueWin:
    def __init__(self, controler, configHandle, memory, issueWin, siteName):
        self.controler = controler
        self.configHandle = configHandle
        self.memory = memory
        self.issueWin = issueWin
        self.siteName = siteName
        self.issueName = tk.StringVar()

    def buildWindow(self):
        self.root = tk.Toplevel()
        self.root.title(self.siteName)
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.config(bg="#333333")

    def drawWidgets(self):
        self.label1 = tk.LabelFrame(self.root, text="Nowa Usterka", bg="#333333", 
                                    fg="#ffffff", font=("Arial", 16, "bold"), bd=5, 
                                    relief=tk.FLAT)
        self.label1.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=10)

        self.entry1 = tk.Entry(self.label1, bg="#333333", fg="#ffffff", 
                              font=("Arial", 16, "bold"), bd=5, 
                              relief=tk.FLAT, textvariable = self.issueName)
        self.entry1.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=10)

        self.entry2 = tk.Text(self.root, bg="#333333", fg="#ffffff", 
                             font=("Arial", 16, "bold"), bd=5, relief=tk.FLAT)
        self.entry2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.button1 = tk.Button(self.label1, text="Dodaj", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.addIssue)
        self.button1.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)

        self.button2 = tk.Button(self.label1, text="Zamknij", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.closeWindow)
        self.button2.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)

    def binder(self):
        self.root.bind("WM_DELETE_WINDOW", self.closeWindow)

    def startup(self):
        self.root.mainloop()

# Local methods ------------------------------------------------------------
    def closeWindow(self):
        self.root.destroy()

    def addIssue(self):
        self.issueName = self.issueName.get()
        self.timestamp = time.strftime("%Y-%m-%d %H-%M")
        self.issueName = self.issueName + " " + self.timestamp
        if self.regexIssueName():
            return
        self.addToMemory()
        self.addToListBox()
        self.addIssueToSite()
        print(f"Issue {self.issueName} added.")
        self.closeWindow()

# Deep private methods -----------------------------------------------------
    def addToMemory(self):
        self.memory.issuesDict[self.siteName].append(f"{self.issueName}.txt")
        print(self.memory.issuesDict[self.siteName])

    def addToListBox(self):
        self.issueWin.listBox.insert(tk.END, self.issueName+".txt")    

    def regexIssueName(self):
        res = [True, True]
        res[0] = self.charRegex()
        res[1] = self.wordRegex()
        if True in res:
            ttk.messagebox.showerror("Błąd", "Nazwa zawiera niedozwolone znaki lub słowa.")
            return True
        else:
            return False

    def charRegex(self):
        forbiddenChars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in self.issueName for char in forbiddenChars):
            print("Forbidden char in issue name.")
            return True
        return False

    def wordRegex(self):
        forbiddenWords = ['CON', 'PRN', 'AUX', 'NUL', 'COM0', 'COM1', 
                          'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 
                          'COM8', 'COM9', 'LPT0', 'LPT1', 'LPT2', 'LPT3', 
                          'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        for item in forbiddenWords:
            if item in self.issueName.upper():
                print("Forbidden word in issue name.")
                return True
        return False

    def addIssueToSite(self):
        if  not os.path.exists(os.path.join(self.configHandle.dataDirPath, self.siteName, self.configHandle.issueFolderName)):
            os.mkdir(os.path.join(self.configHandle.dataDirPath, self.siteName, self.configHandle.issueFolderName))
        os.chdir(self.configHandle.dataDirPath + "/" + self.siteName + "/" + self.configHandle.issueFolderName)

        print(f"Adding issue {self.issueName} to {self.siteName}.")
        print(f"Current dir: {os.getcwd()}")

        with open(f"{self.issueName}.txt", "w+") as file:
            file.write(self.entry2.get("1.0", "end-1c"))
            file.close()
        os.chdir(self.controler.globalCwd)


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


class EditWindow:
    def __init__(self, mainWin, configHandle, memory):
        self.mainWin = mainWin
        self.configHandle = configHandle
        self.memory = memory
        self.root = None
        self.siteName = None
        self.nameOnScreen = tk.StringVar()
        self.serviceNumOnScreen = tk.StringVar()

    def buildWindow(self):
        self.root = tk.Toplevel()
        self.root.title("Edytuj Obiekt")
        self.root.resizable(False, False)
        self.root.config(bg="#333333")

    def drawWidgets(self):
        self.label1 = tk.LabelFrame(self.root, text="Edytuj Obiekt", bg="#333333", 
                                    fg="#ffffff", font=("Arial", 16, "bold"), bd=5, 
                                    relief=tk.FLAT)
        self.label1.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=10)

        self.entry1 = tk.Entry(self.label1, bg="#000000", fg="#ffffff", 
                              font=("Arial", 16, "bold"), bd=5, 
                              relief=tk.FLAT, textvariable = self.nameOnScreen)
        self.entry1.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=10)

        self.entry2 = tk.Entry(self.label1, bg="#000000", fg="#ffffff", 
                              font=("Arial", 16, "bold"), bd=5, 
                              relief=tk.FLAT, textvariable = self.serviceNumOnScreen)
        self.entry2.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=10)

        self.button1 = tk.Button(self.label1, text="Zapisz", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.saveChanges)
        self.button1.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)

        self.button2 = tk.Button(self.label1, text="Anuluj", activebackground="red", 
                                 bg="#993333", fg="#ffffff", font=("Arial", 16, "bold"), 
                                 bd=5, relief=tk.FLAT, command=self.closeWindow)
        self.button2.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)

    def binder(self):
        self.root.bind("WM_DELETE_WINDOW", self.closeWindow)