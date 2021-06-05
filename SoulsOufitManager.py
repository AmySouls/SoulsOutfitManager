import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json

global soulsOutfitManager_Global

class SoulsOutfitManager:
    """Main class of SoulsOufitManager"""

    supportedGameEXENames = [
        'DarkSoulsIII.exe',
    ]

    programDataFileName = 'SoulsOutfitManager_Data.json'

    partNamesFileName = 'part_names.json'

    assetsDirectory = 'assets'

    modsDirectory = 'mods'

    def __init__(self):
        self.window = None
        self.gameDirectory = ''
        self.moddedParts = []
        self.gameParts = []
        self.partNames = {}
        self.widgets = {}

    def __getPartNameFromPartFileName(self, partFileName):
        name = 'Unknown'

        if len(partFileName.split('.')) == 0:
            return name

        partNameSections = partFileName.split('.')[0].split('_')

        for partNameKey in self.partNames:
            if len(partNameKey.split('.')) == 0:
                continue

            itrPartNameSections = partNameKey.split('.')[0].split('_')

            if len(partNameSections) >= 3 and len(itrPartNameSections) == 2 and itrPartNameSections[0].lower() == partNameSections[0].lower() and itrPartNameSections[1] == partNameSections[2]:
                name = self.partNames[partNameKey]

                if partNameSections[1] == 'm':
                    name += ' [Male]'
                elif partNameSections[1] == 'f':
                    name += ' [Female]'

                if len(partNameSections) == 4 and partNameSections[3] == 'l':
                    name += ' [Lower Detail]'
        
        return name

    def __savePartNames(self):
        json.dump(self.partNames, open(SoulsOutfitManager.assetsDirectory + os.path.sep + SoulsOutfitManager.partNamesFileName, 'w'))

    def __loadPartNames(self):
        try:
            self.partNames = json.load(open(SoulsOutfitManager.assetsDirectory + os.path.sep + SoulsOutfitManager.partNamesFileName))
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Python Error', str(error) 
                + "\n\nPlease assure you don't move SoulsOufitManager outside the same folder where \"assets\" is contained.")
            exit()

    def __initUI(self):
        self.window = tk.Tk()
        self.window.geometry('600x500')
        self.window.title('SoulsOutfitManager')
        self.window.iconbitmap('assets' + os.path.sep + 'smouldering-gs.ico')
        self.gameDirVariable = tk.StringVar()
        self.widgets['game_dir_browse_button'] = tk.Button(
            self.window,
            text='Browse',
            width=8,
            height=1,
            relief=tk.RAISED)
        self.widgets['game_dir_browse_button'].bind('<Button-1>',
            SoulsOutfitManager.openBrowseMenu)
        self.widgets['game_dir_browse_button'].grid(
            row=0, 
            column=0,
            padx=5,
            pady=5)
        self.widgets['game_dir_entry'] = tk.Entry(
            self.window,
            width=100)
        self.widgets['game_dir_entry'].grid(
            row=0,
            column=1,
            padx=5,
            pady=5)
        self.widgets['modded_part_list_label'] = tk.Label(
            self.window,
            text='Your Modded Parts',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.widgets['modded_part_list_label'].grid(
            row=1,
            column=0,
            padx=5,
            pady=5)
        self.widgets['refresh_button'] = tk.Button(
            self.window,
            text='Refresh',
            width=6,
            height=1,
            relief=tk.RAISED)
        self.widgets['refresh_button'].bind('<Button-1>',
            SoulsOutfitManager.refresh)
        self.widgets['refresh_button'].grid(
            row=1, 
            column=1,
            padx=5,
            pady=5)
        self.widgets['modded_part_list'] = tk.Listbox(
            self.window,
            width=50,
            height=80,
            relief=tk.SUNKEN,
            bd=5
            xview=False)
        self.widgets['modded_part_list'].grid(
            row=2,
            column=0,
            padx=5,
            pady=5)
        self.widgets['game_part_list_label'] = tk.Label(
            self.window,
            text='Parts in your Game',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.widgets['game_part_list_label'].grid(
            row=1,
            column=2,
            padx=5,
            pady=5)
        self.widgets['game_part_list'] = tk.Listbox(
            self.window,
            width=50,
            height=80,
            relief=tk.SUNKEN,
            bd=3
            xview=False)
        self.widgets['game_part_list'].grid(
            row=2,
            column=2,
            padx=5,
            pady=5)

    def __tryLoadProgramData(self):
        try:
            return json.load(open(SoulsOutfitManager.programDataFileName))
        except FileNotFoundError as error:
            json.dump({}, open(SoulsOutfitManager.programDataFileName, 'w'))

            try:
                return json.load(open(SoulsOutfitManager.programDataFileName))
            except FileNotFoundError as error:
                print(error)
                messagebox.showerror('SoulsOutfitManager Python Error', str(error) 
                    + '\n\nUnable to create program data file.')
                exit()
    
    def __saveProgramData(self, programData):
        json.dump(programData, open(SoulsOutfitManager.programDataFileName, 'w'))

    def __loadDataIntoUI(self):
        self.widgets['modded_part_list'].delete(0, self.widgets['modded_part_list'].size())
        self.widgets['game_part_list'].delete(0, self.widgets['game_part_list'].size())
        gameDirectory = soulsOutfitManager_global.widgets['game_dir_entry'].get()

        if os.path.isdir(gameDirectory) and os.path.isdir(gameDirectory + os.path.sep + 'parts'):
            partsDir = gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                partName = self.__getPartNameFromPartFileName(entry.name)
                if partName != 'Unknown':
                    self.widgets['game_part_list'].insert(0, partName)

        if os.path.isdir(SoulsOutfitManager.modsDirectory):
            for entry in os.scandir(SoulsOutfitManager.modsDirectory):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                fullName = os.path.splitext(entry.name)[0]

                if fullName.endswith('.partsbnd'):
                    fullName = fullName[:-9]

                partName = self.__getPartNameFromPartFileName(entry.name)

                if partName != 'Unknown':
                    fullName += " (" + partName + ")"

                self.widgets['modded_part_list'].insert(0, fullName)
                

    def start(self):
        self.__loadPartNames()
        self.__initUI()
        programDataFile = self.__tryLoadProgramData()

        if 'gameDirectory' in programDataFile and any(os.path.isfile(programDataFile['gameDirectory'] + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            currentText = soulsOutfitManager_global.widgets['game_dir_entry'].get()
            soulsOutfitManager_global.widgets['game_dir_entry'].delete(0, len(currentText))
            soulsOutfitManager_global.widgets['game_dir_entry'].insert(0, programDataFile['gameDirectory'])
        self.__loadDataIntoUI()
        self.window.mainloop()

    def getWidgets(self):
        return self.widgets

    @staticmethod
    def openBrowseMenu(event):
        event.widget.config(relief=tk.RAISED)
        directory = filedialog.askdirectory(mustexist=True)

        if any(os.path.isfile(directory + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            programDataFile = soulsOutfitManager_global.__tryLoadProgramData()
            programDataFile['gameDirectory'] = directory
            soulsOutfitManager_global.__saveProgramData(programDataFile)
            currentText = soulsOutfitManager_global.widgets['game_dir_entry'].get()
            soulsOutfitManager_global.widgets['game_dir_entry'].delete(0, len(currentText))
            soulsOutfitManager_global.widgets['game_dir_entry'].insert(0, directory)
            soulsOutfitManager_global.__loadDataIntoUI()
        else:
            messagebox.showerror('Invalid Directory Given',
                'Could not find a valid EXE in the specified directory.'
                + '\nYou should select the directory containing the game EXE eg. steamapps\common\DARK SOULS III\Game')

    @staticmethod
    def refresh(event):
        soulsOutfitManager_global.__loadDataIntoUI()

soulsOutfitManager_global = SoulsOutfitManager()
soulsOutfitManager_global.start()