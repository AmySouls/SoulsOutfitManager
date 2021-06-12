import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import shutil
import time
import psutil
import pymem

class DS3ModelMaskPatcher:
    """Patches Params in DARK SOULS III's memory for part model masks"""

    def __init__(self):
        self.__process = None
        self.__paramOffset = None
        self.__paramTable = {}

    def __accessMultilevelPointer(self, cTypeName, offsets):
        if len(offsets) == 0:
            return None
        
        baseAddress = offsets[0]
        address = None

        if len(offsets) == 1:
            if cTypeName == 'int8':
                try:
                    return pymem.read_bytes(baseAddress, 1)[0]
                except MemoryReadError as error:
                    return None
            elif cTypeName == 'int16':
                try:
                    return pymem.read_short(baseAddress)
                except MemoryReadError as error:
                    return None
            elif cTypeName == 'int32':
                try:
                    return pymem.read_int(baseAddress)
                except MemoryReadError as error:
                    return None
            elif cTypeName == 'uint64':
                try:
                    return pymem.read_ulonglong(baseAddress)
                except MemoryReadError as error:
                    return None
            elif cTypeName == 'float':
                try:
                    return pymem.read_float(baseAddress)
                except MemoryReadError as error:
                    return None

        
        try:
            address = pymem.read_ulonglong(baseAddress)
        except MemoryReadError as error:
            return None

        offsets.pop(0)
        offset = offsets[0]
        offsets.pop(0)
        offsets[0] = address + offset
        return self.__accessMultilevelPointer(self, cTypeName, offsets)

    def __loadEquipParamProtector(self):
        self.__paramOffset = __accessMultilevelPointer('uint64', [0x144782838, 0xB8, 0x68, 0x68])
        tableSize = accessMultilevelPointer('int16', __paramOffset + 0xA)

        for i in range(tableSize):
            paramId = __accessMultilevelPointer('uint64', [__paramOffset + 0x40 + 0x18 * i])
		    idOffset = __accessMultilevelPointer('uint64', [__paramOffset + 0x48 + 0x18 * i])
		    __paramTable[paramId] = __paramOffset + idOffset

    def readModelMask(self, id, maskOffset):
        try:
            return pymem.read_bytes(__paramTable[paramId] + 0x12E + maskOffset, 1)[0]
        except MemoryReadError as error:
            return None

    def attach(self):
        try:
            self.__process = pymem.open_process_from_name('DarkSoulsIII')
        except ProcessNotFound as error:
            messagebox.showerror('DS3ModelMaskPatcher Python Error', 
                + str(error)
                + "Cannot find the DarkSoulsIII process.")
            return
        except CouldNotOpenProcess as error:
            messagebox.showerror('DS3ModelMaskPatcher Python Error', 
                + str(error)
                + "Could not open the DarkSoulsIII process.")
            return

        self.__loadEquipParamProtector()
        print(self.readModelMask(29500000, 30))

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
        self.__window = None
        self.__gameDirectory = ''
        self.__moddedPartFiles = []
        self.__gamePartFiles = {}
        self.__replacedPartFiles = {}
        self.__partNames = {}
        self.__widgets = {}
        self.__selectedModdedPart = None

    def __getSelectedModdedPart(self):
        return self.__selectedModdedPart

    def __selectModdedPart(self, __selectedModdedPart):
        self.__selectedModdedPart = __selectedModdedPart

    def __getPartNameFromPartFileName(self, partFileName):
        name = 'Unknown'

        if len(partFileName.split('.')) == 0:
            return name

        partNameSections = partFileName.split('.')[0].split('_')

        for partNameKey in self.__partNames:
            if len(partNameKey.split('.')) == 0:
                continue

            itrPartNameSections = partNameKey.split('.')[0].split('_')

            if len(partNameSections) >= 3 and len(itrPartNameSections) == 2 and itrPartNameSections[0].lower() == partNameSections[0].lower() and itrPartNameSections[1] == partNameSections[2]:
                name = self.__partNames[partNameKey]

                if partNameSections[1] == 'm':
                    name += ' [Male]'
                elif partNameSections[1] == 'f':
                    name += ' [Female]'

                if len(partNameSections) == 4 and partNameSections[3] == 'l':
                    name += ' [Lower Detail]'
        
        return name

    def __loadPartNames(self):
        try:
            self.__partNames = json.load(open(SoulsOutfitManager.assetsDirectory + os.path.sep + SoulsOutfitManager.partNamesFileName))
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Python Error', str(error) 
                + "\n\nPlease assure you don't move SoulsOufitManager outside the same folder where \"assets\" is contained.")
            exit()

    def __initUI(self):
        self.__window = tk.Tk()
        self.__window.geometry('1200x550')
        self.__window.title('SoulsOutfitManager')
        self.__window.iconbitmap('assets' + os.path.sep + 'smouldering-gs.ico')
        self.gameDirVariable = tk.StringVar()
        self.__widgets['game_dir_browse_button'] = tk.Button(
            self.__window,
            text='Browse',
            width=8,
            height=1,
            relief=tk.RAISED,
            command=SoulsOutfitManager.openBrowseMenu)
        self.__widgets['game_dir_browse_button'].grid(
            row=0, 
            column=0,
            padx=5,
            pady=5)
        self.__widgets['game_dir_entry'] = tk.Entry(
            self.__window,
            width=100)
        self.__widgets['game_dir_entry'].grid(
            row=0,
            column=1,
            columnspan=4,
            padx=5,
            pady=5)
        self.__widgets['modded_part_list_label'] = tk.Label(
            self.__window,
            text='Your Prepared Mods',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.__widgets['modded_part_list_label'].grid(
            row=1,
            column=0,
            padx=1,
            pady=5)
        self.__widgets['modded_part_list_search_box'] = tk.Entry(
            self.__window,
            width=50)
        self.__widgets['modded_part_list_search_box'].grid(
            row=2,
            column=0,
            padx=5,
            pady=0)
        self.__widgets['modded_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.moddedPartsSearchUpdate)
        self.__widgets['modded_part_list'] = tk.Listbox(
            self.__window,
            width=50,
            height=25,
            relief=tk.SUNKEN,
            bd=5)
        self.__widgets['modded_part_list'].grid(
            row=3,
            column=0,
            padx=5,
            pady=5)
        self.__widgets['modded_part_list'].bind('<<ListboxSelect>>',
            SoulsOutfitManager.selectModdedPart)
        self.__widgets['game_part_list_label'] = tk.Label(
            self.__window,
            text='Parts in your Game',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.__widgets['game_part_list_label'].grid(
            row=1,
            column=1,
            padx=5,
            pady=5)
        self.__widgets['game_part_list_search_box'] = tk.Entry(
            self.__window,
            width=50)
        self.__widgets['game_part_list_search_box'].grid(
            row=2,
            column=1,
            padx=5,
            pady=0)
        self.__widgets['game_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.gamePartsSearchUpdate)
        self.__widgets['game_part_list'] = tk.Listbox(
            self.__window,
            width=50,
            height=25,
            relief=tk.SUNKEN,
            bd=3)
        self.__widgets['game_part_list'].grid(
            row=3,
            column=1,
            padx=5,
            pady=5)
        self.__widgets['game_part_list'].bind('<Double-Button-1>',
            SoulsOutfitManager.tryReplaceGamePart)
        self.__widgets['game_part_list'].bind('<Delete>',
            SoulsOutfitManager.tryDeleteGamePart)
        self.__widgets['replaced_part_list_label'] = tk.Label(
            self.__window,
            text='Installed Modded Parts',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.__widgets['replaced_part_list_label'].grid(
            row=1,
            column=2,
            padx=5,
            pady=5)
        self.__widgets['replaced_part_list_search_box'] = tk.Entry(
            self.__window,
            width=50)
        self.__widgets['replaced_part_list_search_box'].grid(
            row=2,
            column=2,
            padx=5,
            pady=0)
        self.__widgets['replaced_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.replacedPartsSearchUpdate)
        self.__widgets['replaced_part_list'] = tk.Listbox(
            self.__window,
            width=50,
            height=25,
            relief=tk.SUNKEN,
            bd=3)
        self.__widgets['replaced_part_list'].grid(
            row=3,
            column=2,
            padx=5,
            pady=5)
        self.__widgets['replaced_part_list'].bind('<Double-Button-1>',
            SoulsOutfitManager.tryRestorePart)
        self.__widgets['refresh_button'] = tk.Button(
            self.__window,
            text='Refresh',
            width=6,
            height=1,
            relief=tk.RAISED)
        self.__widgets['refresh_button'].bind('<Button-1>',
            SoulsOutfitManager.refresh)
        self.__widgets['refresh_button'].grid(
            row=1, 
            column=3,
            padx=5,
            pady=5,
            sticky='W')

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

    def __loadPartLists(self):
        self.__moddedPartFiles = []
        self.__gamePartFiles = {}
        self.__replacedPartFiles = {}
        __gameDirectory = soulsOutfitManager_global.getWidgets()['game_dir_entry'].get()

        if os.path.isdir(__gameDirectory) and os.path.isdir(__gameDirectory + os.path.sep + 'parts'):
            partsDir = __gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2:
                    continue
                elif os.path.splitext(entry.name)[1] == '.dcx':
                    self.__gamePartFiles[entry.name] = self.__getPartNameFromPartFileName(entry.name)
                elif os.path.splitext(entry.name)[1] == '.sombak':
                    self.__replacedPartFiles[entry.name] = self.__getPartNameFromPartFileName(entry.name)

        if os.path.isdir(SoulsOutfitManager.modsDirectory):
            for entry in os.scandir(SoulsOutfitManager.modsDirectory):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                self.__moddedPartFiles.append(entry.name)

    def __updateModdedPartList(self):
        self.__widgets['modded_part_list'].delete(0, self.__widgets['modded_part_list'].size())
        searchTerm = soulsOutfitManager_global.__widgets['modded_part_list_search_box'].get()

        for moddedPartFile in self.__moddedPartFiles:
            fullName = os.path.splitext(moddedPartFile)[0]
            
            if searchTerm == '' or searchTerm.lower() in fullName.lower():
                self.__widgets['modded_part_list'].insert(0, fullName)

    def __updateGamePartList(self):
        self.__widgets['game_part_list'].delete(0, self.__widgets['game_part_list'].size())
        searchTerm = soulsOutfitManager_global.__widgets['game_part_list_search_box'].get()

        for gamePartFile in self.__gamePartFiles:
            partName = self.__gamePartFiles[gamePartFile]

            if partName != 'Unknown' and (searchTerm == '' or searchTerm.lower() in partName.lower()):
                self.__widgets['game_part_list'].insert(0, partName)

    def __updateReplacedPartList(self):
        self.__widgets['replaced_part_list'].delete(0, self.__widgets['replaced_part_list'].size())
        searchTerm = soulsOutfitManager_global.__widgets['replaced_part_list_search_box'].get()

        for replacedPartFile in self.__replacedPartFiles:
            partName = self.__replacedPartFiles[replacedPartFile]

            if partName != 'Unknown' and (searchTerm == '' or searchTerm.lower() in partName.lower()):
                self.__widgets['replaced_part_list'].insert(0, partName)
                
    def __replaceGamePart(self, moddedPart, gamePart):
        __gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        gamePartFileName = None
        moddedPartFileName = None

        if os.path.isdir(__gameDirectory) and os.path.isdir(__gameDirectory + os.path.sep + 'parts'):
            partsDir = __gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                partName = self.__getPartNameFromPartFileName(entry.name)

                if partName == gamePart:
                    gamePartFileName = entry.name
                    break
        
        if os.path.isdir(SoulsOutfitManager.modsDirectory):
            for entry in os.scandir(SoulsOutfitManager.modsDirectory):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                print(moddedPart)
                partName = os.path.splitext(entry.name)[0]

                if partName == moddedPart:
                    moddedPartFileName = entry.name
                    break

        if moddedPartFileName == None:
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to replace game part with modded part: \n\n'
                + 'File \"'
                + moddedPart
                + '\" does not exist.\n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return

        if gamePartFileName == None:
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to replace game part with modded part: \n\n'
                + 'File \"'
                + gamePart
                + '\" does not exist.\n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return
        
        if os.path.isdir(__gameDirectory) and os.path.isdir(__gameDirectory + os.path.sep + 'parts'):
            partsDirectory = __gameDirectory + os.path.sep + 'parts' + os.path.sep

            try:
                if not os.path.isfile(partsDirectory + os.path.sep + gamePartFileName + '.sombak'):
                    shutil.copyfile(partsDirectory + os.path.sep + gamePartFileName,
                        partsDirectory + os.path.sep + gamePartFileName + '.sombak')
                    
                shutil.copyfile(SoulsOutfitManager.modsDirectory + os.path.sep + moddedPartFileName,
                    partsDirectory + os.path.sep + gamePartFileName)
            except FileNotFoundError as error:
                print(error)
                messagebox.showerror('SoulsOutfitManager Python Error',
                str(error)
                + '\n\nUnable to replace game part with modded part. \n\n'
                + 'You may have deleted or moved the files. Please refresh.')
                return
            self.__loadPartLists()
            self.__updateModdedPartList()
            self.__updateGamePartList()
            self.__updateReplacedPartList()

    def __deleteGamePart(self, gamePart):
        __gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        gamePartFileName = None

        if os.path.isdir(__gameDirectory) and os.path.isdir(__gameDirectory + os.path.sep + 'parts'):
            partsDir = __gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                partName = self.__getPartNameFromPartFileName(entry.name)

                if partName == gamePart:
                    gamePartFileName = entry.name
                    break
            
            if gamePartFileName == None:
                messagebox.showerror('SoulsOutfitManager Python Error',
                    + 'Unable to delete game part. \n\n'
                    + 'You may have deleted or moved the file. Please refresh.')
                return

            try:
                if not os.path.isfile(partsDir + os.path.sep + gamePartFileName + '.sombak'):
                    os.rename(partsDir + os.path.sep + gamePartFileName,
                        partsDir + os.path.sep + gamePartFileName + '.sombak')
            except FileNotFoundError as error:
                print(error)
                messagebox.showerror('SoulsOutfitManager Python Error',
                    str(error)
                    + '\n\nUnable to delete game part. \n\n'
                    + 'You may have deleted or moved the file. Please refresh.')
                return

            self.__loadPartLists()
            self.__updateModdedPartList()
            self.__updateGamePartList()
            self.__updateReplacedPartList()

    def __restoreReplacedPart(self, replacedPart):
        __gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        replacedPartFileName = None

        if os.path.isdir(__gameDirectory) and os.path.isdir(__gameDirectory + os.path.sep + 'parts'):
            partsDir = __gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.sombak':
                    continue
                partName = self.__getPartNameFromPartFileName(entry.name)

                if partName == replacedPart:
                    replacedPartFileName = entry.name
                    break
            
            if replacedPartFileName == None:
                messagebox.showerror('SoulsOutfitManager Python Error',
                    'Unable to restore part. \n\n'
                    + 'You may have deleted or moved the file. Please refresh.')
                return

            try:
                if os.path.isfile(partsDir + os.path.sep + replacedPartFileName[:-6]):
                    os.remove(partsDir + os.path.sep + replacedPartFileName[:-6])

                os.rename(partsDir + os.path.sep + replacedPartFileName,
                    partsDir + os.path.sep + replacedPartFileName[:-6])
            except FileNotFoundError as error:
                print(error)
                messagebox.showerror('SoulsOutfitManager Python Error',
                    str(error)
                    + '\n\nUnable to restore part. \n\n'
                    + 'You may have deleted or moved the file. Please refresh.')
                return

            self.__loadPartLists()
            self.__updateModdedPartList()
            self.__updateGamePartList()
            self.__updateReplacedPartList()

    def start(self):
        self.__loadPartNames()
        self.__initUI()
        programDataFile = self.__tryLoadProgramData()

        if '__gameDirectory' in programDataFile and any(os.path.isfile(programDataFile['__gameDirectory'] + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            currentText = self.__widgets['game_dir_entry'].get()
            self.__widgets['game_dir_entry'].delete(0, len(currentText))
            self.__widgets['game_dir_entry'].insert(0, programDataFile['__gameDirectory'])
        self.__loadPartLists()
        self.__updateModdedPartList()
        self.__updateGamePartList()
        self.__updateReplacedPartList()
        self.__window.mainloop()

    def getWidgets(self):
        return self.__widgets

    @staticmethod
    def selectModdedPart(event):
        selection = soulsOutfitManager_global.getWidgets()['modded_part_list'].curselection()
        partName = None
        
        if len(selection) == 1:
            partName = soulsOutfitManager_global.getWidgets()['modded_part_list'].get(selection[0], None)

        if partName != None:
            soulsOutfitManager_global.__selectModdedPart(partName)

    @staticmethod
    def tryReplaceGamePart(event):
        selection = soulsOutfitManager_global.getWidgets()['game_part_list'].curselection()
        partName = None
        
        if len(selection) == 1:
            partName = soulsOutfitManager_global.getWidgets()['game_part_list'].get(selection[0], None)

        if partName != None:
            moddedPartName = soulsOutfitManager_global.__getSelectedModdedPart()
            
            if moddedPartName == None:
                return

            result = messagebox.askokcancel('Replace game part with modded part?',
                'Are you sure you want to replace \"' 
                + str(partName) + '\" with \"' 
                + str(moddedPartName) + '\"?'
                + '\nA backup will be created for you.')
            
            if result:
                soulsOutfitManager_global.__replaceGamePart(moddedPartName, partName)

    @staticmethod
    def tryDeleteGamePart(event):
        selection = soulsOutfitManager_global.getWidgets()['game_part_list'].curselection()
        partName = None
        
        if len(selection) == 1:
            partName = soulsOutfitManager_global.getWidgets()['game_part_list'].get(selection[0], None)

        if partName != None:
            result = messagebox.askokcancel('Replace this game part with nothing?',
                'Are you you want to replace this game part with nothing?'
                + '\nA backup will be created for you.')
            
            if result:
                soulsOutfitManager_global.__deleteGamePart(partName)

    @staticmethod
    def tryRestorePart(event):
        selection = soulsOutfitManager_global.__widgets['replaced_part_list'].curselection()
        partName = None
        
        if len(selection) == 1:
            partName = soulsOutfitManager_global.__widgets['replaced_part_list'].get(selection[0], None)

        if partName != None:
            result = messagebox.askokcancel('Restore this backup?',
                'Are you sure you want to restore this part to it\'s original?'
                + '\nAny file currently replacing it will be deleted.')
            
            if result:
                soulsOutfitManager_global.__restoreReplacedPart(partName)

    @staticmethod
    def openBrowseMenu():
        directory = filedialog.askdirectory(mustexist=True)

        if any(os.path.isfile(directory + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            programDataFile = soulsOutfitManager_global.__tryLoadProgramData()
            programDataFile['__gameDirectory'] = directory
            soulsOutfitManager_global.__saveProgramData(programDataFile)
            currentText = soulsOutfitManager_global.getWidgets()['game_dir_entry'].get()
            soulsOutfitManager_global.getWidgets()['game_dir_entry'].delete(0, len(currentText))
            soulsOutfitManager_global.getWidgets()['game_dir_entry'].insert(0, directory)
            soulsOutfitManager_global.__updateModdedPartList()
            soulsOutfitManager_global.__updateGamePartList()
        elif len(directory) != 0:
            messagebox.showerror('Invalid Directory Given',
                'Could not find a valid EXE in the specified directory.'
                + '\nYou should select the directory containing the game EXE eg. steamapps\common\DARK SOULS III\Game')

    @staticmethod
    def refresh(event):
        soulsOutfitManager_global.__loadPartLists()
        soulsOutfitManager_global.__updateModdedPartList()
        soulsOutfitManager_global.__updateGamePartList()
        soulsOutfitManager_global.__updateReplacedPartList()

    @staticmethod
    def moddedPartsSearchUpdate(event):
        soulsOutfitManager_global.__updateModdedPartList()

    @staticmethod
    def gamePartsSearchUpdate(event):
        soulsOutfitManager_global.__updateGamePartList()

    @staticmethod
    def replacedPartsSearchUpdate(event):
        soulsOutfitManager_global.__updateReplacedPartList()

global soulsOutfitManager_Global
soulsOutfitManager_global = SoulsOutfitManager()

modelMaskPatcher = DS3ModelMaskPatcher()
modelMaskPatcher.attach()

soulsOutfitManager_global.start()