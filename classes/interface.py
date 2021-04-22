import os, shutil, webbrowser
from pathlib import Path
from zipfile import ZipFile
import tkinter as tk 
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox
from classes.simpledropdown import SimpleDropDown
from classes.chatline import ChatLine
from classes.htmlgenerator import HtmlGenerator, LineType
from classes.converter import Converter

class Interface:
    tmpFolder = os.path.join(Path().absolute(), 'temp')
    templateFolder = os.path.join(Path().absolute(), 'template')
    statusColor = '#777'
    grayColor = '#eee'

    inputPath = ''
    outputPath = ''

    chatOwner = ''
    attachedFilePaths = []
    chatLines = []
    chatUsers = []

    def __init__(self):
        self.window = tk.Tk()
        self.configureWindow()
        self.window.mainloop()

    def configureWindow(self):
        self.window.iconbitmap(os.path.join(Path().absolute(), 'assets', 'logo.ico'))
        self.window.title('WhatsApp Chat Converter 🚀')
        self.window.geometry('600x500')
        self.window.minsize(600, 500)
        self.window.maxsize(800, 700)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.drawInputSection()
        self.drawOutputSection()
        self.drawExportSection()

    def onClosing(self):
        print('Closing window...')
        if (os.path.isdir(self.tmpFolder)):
            shutil.rmtree(self.tmpFolder)

        self.window.destroy()


    def drawInputSection(self):
        self.frameInput = ttk.LabelFrame(self.window, text='Input')
        self.frameInput.grid(column=0, row=0, padx=5, pady=10, sticky='NSEW')
        self.frameInput.columnconfigure(1, weight=1)
        self.frameInput.rowconfigure(2, weight=1)

        self.lblInfo = tk.Label(self.frameInput, text='You must select a folder contains conversation with attached files')
        self.lblInfo.config(fg=self.statusColor)
        self.lblInfo.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky='W')

        self.btnInput = ttk.Button(self.frameInput, text='Select Input', command=self.selectInput)
        self.btnInput.grid(column=0, row=1, padx=5, pady=5, sticky='W')
        
        self.lblIn = tk.Label(self.frameInput, text='No selection')
        self.lblIn.grid(column=1, row=1, padx=5, pady=5, sticky='W')

        self.listUsers = tk.Listbox(self.frameInput, exportselection=False, selectbackground='green')
        self.listUsers.grid(column=0, row=2, padx=5, pady=5, sticky='NSWE')
        self.listUsers.bind('<<ListboxSelect>>', self.userSelected)

        self.conversation = tk.Listbox(self.frameInput, font=tkFont.Font(size=7), selectbackground=self.grayColor, selectforeground='black')
        self.conversation.grid(column=1, row=2, padx=5, pady=5, sticky='NSWE')

    def drawOutputSection(self):
        self.frameOutput = ttk.LabelFrame(self.window, text='Output')
        self.frameOutput.grid(column=0, row=1, padx=5, pady=10, sticky='NSEW')

        self.btnOutput = ttk.Button(self.frameOutput, text='Select Output', command=self.selectOutput)
        self.btnOutput.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        self.lblOut = ttk.Label(self.frameOutput, text='No selection')
        self.lblOut.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky='E')

    def drawExportSection(self):
        self.frameExport = ttk.LabelFrame(self.window, text='Convert Chat to HTHL')
        self.frameExport.grid(column=0, row=2, padx=5, pady=10, sticky='NSEW')

        self.lblStatus = tk.Label(self.frameExport, text='Firstly you must a conversation on your computer...')
        self.lblStatus.config(fg=self.statusColor)
        self.lblStatus.grid(column=0, row=0, padx=5, pady=10, sticky='NSEW')
        self.btnExport = ttk.Button(self.frameExport, text='Export', command=self.exportChat)
        self.btnExport.grid(column=0, row=1, padx=5, pady=10, sticky='W')


    # Events #
    def userSelected(self, event):
        index, = self.listUsers.curselection() 
        self.chatOwner = self.listUsers.get(index)
        self.lblStatus.config(text=f'Selected {self.chatOwner} how chat owner')


    # Button Actions #
    def selectInput(self):
        self.inputPath = filedialog.askopenfilename(initialdir='C:\\Users\\usuario\\Projects\\SCRIPTS\\python-whatsapp-converter', title='Select whatsapp conversation (only zip files)', filetypes=[('Zip Files', '*.zip')])
        if self.inputPath != '':
            self.lblIn.config(text=self.inputPath)
            self.analyzeConversation()

    def selectOutput(self):
        self.outputPath = filedialog.askdirectory(initialdir='C:\\Users\\usuario\\Desktop\\BORRAR')
        self.lblOut.config(text=self.outputPath)

    def exportChat(self):
        if self.inputPath == '':
            messagebox.showerror('No input', 'If you dont enter input path it is unable to parse conversation 😉')
            return
        if len(self.chatLines) == 0:
            messagebox.showerror('Invalid input', f'Unable to parse {self.inputPath}')
            return
        if self.chatOwner == '':
            messagebox.showerror('No chat owner', 'It is necessary you have to select an user on user list')
            return

        exportPath = os.path.join(self.outputPath, self.exportName())
        if os.path.isdir(exportPath):
            if messagebox.askyesno(message=f'{exportPath} exists. Do you want replace it?'):
                shutil.rmtree(exportPath)
        
        os.mkdir(exportPath)
        converter = Converter(self.inputPath, self.chatLines, self.chatOwner, exportPath)
        converter.parse()
        if converter.export() == True:
            if messagebox.askyesno(message='Do you want open the exported conversation on browser?') == True:
                webbrowser.open(os.path.join(exportPath, 'index.html'))
        else:
            messagebox.showerror('Export error', 'There was a problem exporting conversation 😫')
        

    # Functions #
    def exportName(self):
        users = self.chatUsers[:]
        users.remove(self.chatOwner)
        others = ','.join(users)
        return f'Chat of {self.chatOwner} with {others}'

    def analyzeConversation(self):
        if os.path.isdir(self.inputPath):
            self.parseChatFile(self.inputPath)
        elif os.path.isfile(self.inputPath):
            with ZipFile(self.inputPath, 'r') as zipObj:
                self.attachedFilePaths.clear()
                zipObj.extractall(self.tmpFolder)
                for name in zipObj.namelist():
                    fullPath = os.path.join(self.tmpFolder, name)
                    if (name.endswith('.txt')):
                        self.parseChatFile(fullPath)
                    else:
                        self.attachedFilePaths.append(fullPath)
            shutil.rmtree(self.tmpFolder)
        
        if len(self.chatLines) > 0:
            self.lblInfo.config(text=f'Parsed {len(self.chatLines)} lines and {len(self.chatUsers)} users was finded successfully', fg='green')
            self.lblStatus.config(text=f'You have to select an user from list before export conversation')            
            
            self.listUsers.delete(0, tk.END)
            for userName in self.chatUsers:
                self.listUsers.insert(tk.END, userName)

            self.conversation.delete(0, tk.END)
            index = 0
            for line in self.chatLines:
                self.conversation.insert(tk.END, line.getMessage())
                self.conversation.itemconfig(index, bg=self.grayColor)
                index += 1
            
        else:
            self.lblInfo.config(text='Opps!!! Conversation selected is not valid', fg='red')

    def parseChatFile(self, chatFilePath):
        self.chatOwner = ''
        self.chatUsers.clear()
        self.chatLines.clear()
        chatFile = open(chatFilePath, encoding="utf8")
        lines = chatFile.readlines()
        for line in lines:
            cl = ChatLine(line)
            if cl.user != '':
                self.chatLines.append(cl)
                if cl.user not in self.chatUsers:
                    self.chatUsers.append(cl.user)

        chatFile.close()




