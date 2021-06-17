import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import shutil
import time
from ChecklistBox import ScrollableChecklist
from DS3ModelMaskPatcher import DS3ModelMaskPatcher
from DS3PartInfo import DS3PartInfo
from DS3PartUtil import DS3PartUtil
from DS3PartUtil import EquipModelCategory
from DS3PartUtil import EquipModelGender
from DS3PartListbox import DS3PartListbox

class SoulsOutfitManager:
    """Main class of SoulsOutfitManager"""

    supportedGameEXENames = [
        'DarkSoulsIII.exe',
    ]

    programDataFileName = 'SoulsOutfitManager_Data.json'

    partNamesFileName = 'part_names.json'

    assetsDirectory = 'assets'

    modsDirectory = 'mods'

    def __init__(self):
        self.__ds3PartUtil = None
        self.__window = None
        self.__gameDirectory = ''
        self.__moddedParts = []
        self.__gameParts = {}
        self.__replacedParts = {}
        self.__widgets = {}
        self.__selectedModdedPart = None
        self.__modelMaskPresets = {}

    def __getSelectedModdedPart(self):
        return self.__selectedModdedPart

    def __selectModdedPart(self, __selectedModdedPart):
        self.__selectedModdedPart = __selectedModdedPart
    
    def __getModelMaskPresetFile(self, part):
        return part.getEquipModelCategory() + '_' + str(part.getEquipModelId()) + '.modelmaskpreset.json'

    def __loadDS3PartUtil(self):
        self.__ds3PartUtil = DS3PartUtil(SoulsOutfitManager.assetsDirectory + os.path.sep + SoulsOutfitManager.partNamesFileName)

    def __initUI(self):
        self.__window = tk.Tk()
        self.__window.configure(bg='#1e1e1e')
        self.__window.geometry('1300x550')
        self.__window.title('SoulsOutfitManager')
        self.__window.iconbitmap('assets' + os.path.sep + 'smouldering-gs.ico')
        self.gameDirVariable = tk.StringVar()
        self.__widgets['game_dir_browse_button'] = tk.Button(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            text='Browse',
            width=8,
            height=1,
            relief=tk.RAISED,
            command=SoulsOutfitManager.openBrowseForGameDirectory)
        self.__widgets['game_dir_browse_button'].grid(
            row=0, 
            column=0,
            padx=5,
            pady=5)
        self.__widgets['game_dir_entry'] = tk.Entry(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            width=100)
        self.__widgets['game_dir_entry'].grid(
            row=0,
            column=1,
            columnspan=4,
            padx=5,
            pady=5)
        self.__widgets['modded_part_list_label'] = tk.Label(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
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
            bg='#333333',
            fg='#c3c3c3',
            width=50)
        self.__widgets['modded_part_list_search_box'].grid(
            row=2,
            column=0,
            padx=5,
            pady=0)
        self.__widgets['modded_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.moddedPartsSearchUpdate)
        self.__widgets['modded_part_list'] = DS3PartListbox(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
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
            bg='#333333',
            fg='#c3c3c3',
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
            bg='#333333',
            fg='#c3c3c3',
            width=50)
        self.__widgets['game_part_list_search_box'].grid(
            row=2,
            column=1,
            padx=5,
            pady=0)
        self.__widgets['game_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.gamePartsSearchUpdate)
        self.__widgets['game_part_list'] = DS3PartListbox(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
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
            bg='#333333',
            fg='#c3c3c3',
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
            bg='#333333',
            fg='#c3c3c3',
            width=50)
        self.__widgets['replaced_part_list_search_box'].grid(
            row=2,
            column=2,
            padx=5,
            pady=0)
        self.__widgets['replaced_part_list_search_box'].bind('<KeyRelease>',
            SoulsOutfitManager.replacedPartsSearchUpdate)
        self.__widgets['replaced_part_list'] = DS3PartListbox(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            width=50,
            height=25,
            relief=tk.SUNKEN,
            bd=3)
        self.__widgets['replaced_part_list'].grid(
            row=3,
            column=2,
            padx=5,
            pady=5)
        self.__widgets['replaced_part_list'].bind('<BackSpace>',
            SoulsOutfitManager.tryRestorePart)
        self.__widgets['replaced_part_list'].bind('<<ListboxSelect>>',
            SoulsOutfitManager.tryOpenModelMaskEditor)
        self.__widgets['refresh_button'] = tk.Button(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            text='Refresh Files',
            width=14,
            height=1,
            relief=tk.RAISED,
            command=SoulsOutfitManager.refresh)
        self.__widgets['refresh_button'].grid(
            row=0, 
            column=4,
            padx=5,
            pady=5,
            sticky='W')
        self.__widgets['model_mask_save_button'] = tk.Button(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            text='Save & Update\nModel Mask Changes',
            width=16,
            height=2,
            relief=tk.RAISED,
            command=SoulsOutfitManager.saveModelMaskChanges)
        self.__widgets['model_mask_save_button'].grid(
            row=1, 
            column=4,
            padx=5,
            pady=5,
            sticky='W')
        self.__widgets['model_mask_editor_label'] = tk.Label(
            self.__window,
            bg='#333333',
            fg='#c3c3c3',
            text='Edit Model Masks',
            relief=tk.RIDGE,
            padx=3,
            pady=3)
        self.__widgets['model_mask_editor_label'].grid(
            row=2,
            column=3,
            padx=5,
            pady=5)
        self.__widgets['model_mask_editor'] = ScrollableChecklist(
            self.__window,
            bg='#333333',
            width=150,
            height=410,
            relief=tk.SUNKEN,
            bd=3)
        self.__widgets['model_mask_editor'].grid(
            row=3,
            column=3,
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

    def __loadPartLists(self):
        self.__moddedParts = []
        self.__gameParts = []
        self.__replacedParts = []
        gameDirectory = soulsOutfitManager_global.getWidgets()['game_dir_entry'].get()

        if os.path.isdir(gameDirectory) and os.path.isdir(gameDirectory + os.path.sep + 'parts'):
            partsDir = gameDirectory + os.path.sep + 'parts'

            for entry in os.scandir(partsDir):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2:
                    continue
                elif os.path.splitext(entry.name)[1] == '.dcx':
                    self.__gameParts.append(DS3PartInfo(self.__ds3PartUtil, partsDir, entry.name))
                elif os.path.splitext(entry.name)[1] == '.sombak':
                    part = DS3PartInfo(self.__ds3PartUtil, partsDir, entry.name)
                    self.__replacedParts.append(part)
                    self.__loadModelMaskPresetFile(part)

                    if part.getPartFile() in self.__modelMaskPresets:
                        self.__applyModelMaskPresetToGame(part, self.__modelMaskPresets[part.getPartFile()])

        if os.path.isdir(SoulsOutfitManager.modsDirectory):
            for entry in os.scandir(SoulsOutfitManager.modsDirectory):
                if not entry.is_file() or len(os.path.splitext(entry.name)) != 2 or not os.path.splitext(entry.name)[1] == '.dcx':
                    continue
                self.__moddedParts.append(DS3PartInfo(self.__ds3PartUtil, SoulsOutfitManager.modsDirectory, entry.name))

    def __updateUIModdedPartList(self):
        self.__widgets['modded_part_list'].delete(0, self.__widgets['modded_part_list'].size())
        searchTerm = self.__widgets['modded_part_list_search_box'].get()

        for moddedPart in self.__moddedParts:
            partFile = os.path.splitext(moddedPart.getPartFile())[0]
            
            if searchTerm == '' or searchTerm.lower() in partFile.lower():
                self.__widgets['modded_part_list'].insert(0, partFile, moddedPart)

    def __updateUIGamePartList(self):
        self.__widgets['game_part_list'].delete(0, self.__widgets['game_part_list'].size())
        searchTerm = self.__widgets['game_part_list_search_box'].get()
        replacedPartFiles = []

        for replacedPart in self.__replacedParts:
            replacedPartFiles.append(replacedPart.getPartFile())

        for gamePart in self.__gameParts:
            if gamePart.getPartFile() + '.sombak' in replacedPartFiles:
                continue

            partName = gamePart.getPartName()

            if partName != 'Unknown' and (searchTerm == '' or searchTerm.lower() in partName.lower()):
                self.__widgets['game_part_list'].insert(0, partName, gamePart)

    def __updateUIReplacedPartList(self):
        self.__widgets['replaced_part_list'].delete(0, self.__widgets['replaced_part_list'].size())
        searchTerm = soulsOutfitManager_global.__widgets['replaced_part_list_search_box'].get()

        for replacedPart in self.__replacedParts:
            partName = replacedPart.getPartName()

            if partName != 'Unknown' and (searchTerm == '' or searchTerm.lower() in partName.lower()):
                self.__widgets['replaced_part_list'].insert(0, partName, replacedPart)
                
    def __replaceGamePart(self, moddedPart, gamePart):
        gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        moddedPartPath = moddedPart.getDirectory() + os.path.sep + moddedPart.getPartFile()
        gamePartPath = gamePart.getDirectory() + os.path.sep + gamePart.getPartFile()

        if not os.path.isfile(moddedPartPath):
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to replace game part with modded part: \n\n'
                + 'File \"'
                + moddedPart
                + '\" does not exist.\n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return

        if not os.path.isfile(gamePartPath):
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to replace game part with modded part: \n\n'
                + 'File \"'
                + gamePart
                + '\" does not exist.\n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return
        
        try:
            shutil.copyfile(gamePartPath,
                gamePartPath + '.sombak')
                    
            shutil.copyfile(moddedPartPath,
                gamePartPath)
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Python Error',
                str(error)
                + '\n\nUnable to replace game part with modded part. \n\n'
                + 'You may have deleted or moved the files. Please refresh.')
            return
            
        self.__loadPartLists()
        self.__updateUIModdedPartList()
        self.__updateUIReplacedPartList()
        self.__updateUIGamePartList()

    def __deleteGamePart(self, gamePart):
        gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        gamePartPath = gamePart.getDirectory() + os.path.sep + gamePart.getPartFile()

        if not os.path.isfile(gamePartPath):
            messagebox.showerror('SoulsOutfitManager Python Error',
                + 'Unable to delete game part. \n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return
        
        try:
            if not os.path.isfile(gamePartPath + '.sombak'):
                os.rename(gamePartPath,
                    gamePartPath + '.sombak')
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Python Error',
                str(error)
                + '\n\nUnable to delete game part. \n\n'
                + 'You may have deleted or moved the file. Please refresh.')
            return

        self.__loadPartLists()
        self.__updateUIModdedPartList()
        self.__updateUIReplacedPartList()
        self.__updateUIGamePartList()

    def __restoreReplacedPart(self, replacedPart):
        gameDirectory = soulsOutfitManager_global.__widgets['game_dir_entry'].get()
        replacedPartBackupPath = replacedPart.getDirectory() + os.path.sep + replacedPart.getPartFile()
        replacedPartPath = replacedPartBackupPath[:-7]

        if not os.path.isfile(replacedPartBackupPath):
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to restore part \"'
                + replacedPart.getPartFile()
                + '\"\n\nYou may have deleted or moved the file. Please refresh.')
            return

        try:
            if os.path.isfile(replacedPartPath):
                os.remove(replacedPartPath)

            os.rename(replacedPartBackupPath,
                replacedPartPath)
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Python Error',
                'Unable to restore part \"'
                + replacedPart.getPartFile()
                + '\"\n\nYou may have deleted or moved the file. Please refresh.')
            return

        self.__loadPartLists()
        self.__updateUIModdedPartList()
        self.__updateUIReplacedPartList()
        self.__updateUIGamePartList()
    
    def __applyModelMaskPresetToGame(self, part, preset):
        presetFile = os.path.splitext(self.__getModelMaskPresetFile(part))[0]

        if not presetFile.endswith('.modelmaskpreset'):
            return
            
        split = presetFile.split('.')

        if not len(split) == 2:
            return

        equipInfoSplit = split[0].split('_')
            
        if not len(equipInfoSplit) == 2:
            return

        bodyPart = equipInfoSplit[0]
        modelId = int(equipInfoSplit[1])

        for offset in preset:
            paramId = modelMaskPatcher.getParamIdByEquipModelIdAndEquipModelCategory(modelId, bodyPart)
            modelMaskPatcher.writeModelMask(paramId, int(offset), int(preset[offset]['hidden']))
    
    def __createModelMaskPresetFile(self, part):
        if not os.path.isdir(SoulsOutfitManager.modsDirectory):
            return

        template = json.load(open(SoulsOutfitManager.assetsDirectory + os.path.sep + 'template.modelmaskpreset.json'))
        preset = {}
        paramId = modelMaskPatcher.getParamIdByEquipModelIdAndEquipModelCategory(part.getEquipModelId(), part.getEquipModelCategory())
        
        for i in range(97):
            maskElement = { 'description' : '', 'hidden' : False }
            
            if str(i) in template:
                maskElement['description'] = 'Hide ' + template[str(i)]['description']
            else:
                maskElement['description'] = 'Hide ' + str(i)

            maskElement['hidden'] = modelMaskPatcher.readModelMask(paramId, i)
            preset[str(i)] = maskElement

        with open(SoulsOutfitManager.modsDirectory + os.path.sep + self.__getModelMaskPresetFile(part), 'w') as file:
            json.dump(preset, file, ensure_ascii=False, indent=2)

    def __saveModelMaskPreset(self, part):
        if not os.path.isdir(SoulsOutfitManager.modsDirectory):
            return

        template = json.load(open(SoulsOutfitManager.assetsDirectory + os.path.sep + 'template.modelmaskpreset.json'))
        preset = {}
        paramId = modelMaskPatcher.getParamIdByEquipModelIdAndEquipModelCategory(part.getEquipModelId(), part.getEquipModelCategory())
        presetFile = self.__getModelMaskPresetFile(part)

        with open(SoulsOutfitManager.modsDirectory + os.path.sep + presetFile, 'w') as file:
            json.dump(self.__modelMaskPresets[part.getPartFile()], file, ensure_ascii=False, indent=2)
        
    def __registerModelMaskPresetEdit(self, part, items):
        for i in range(97):
            if int(items[i]) == 1:
                self.__modelMaskPresets[part.getPartFile()][str(i)]['hidden'] = True
            else:
                self.__modelMaskPresets[part.getPartFile()][str(i)]['hidden'] = False
    
    def __loadModelMaskPresetFile(self, part):
        presetPath = SoulsOutfitManager.modsDirectory + os.path.sep + self.__getModelMaskPresetFile(part)

        if not os.path.isfile(presetPath):
            return
        
        preset = json.load(open(presetPath))
        self.__modelMaskPresets[part.getPartFile()] = preset

    def __loadPresetIntoModelMaksEditorUI(self, preset):
        self.__widgets['model_mask_editor'].setItems(preset, SoulsOutfitManager.tryUpdateModelMaskPreset)
    
    def __emptyModelMasksEditorUI(self):
        self.__widgets['model_mask_editor'].setItems({}, SoulsOutfitManager.tryUpdateModelMaskPreset)
    
    def __tryLoadModelMaskPresetIntoEditor(self, part):
        equipModelCategory = part.getEquipModelCategory()
        if equipModelCategory == EquipModelCategory.WEAPON.value:
            self.__emptyModelMasksEditorUI()
            return
        
        if not os.path.isfile(SoulsOutfitManager.modsDirectory 
                + os.path.sep 
                + self.__getModelMaskPresetFile(part)):
            self.__createModelMaskPresetFile(part)    
            self.__loadModelMaskPresetFile(part)
            
        if part.getPartFile() in self.__modelMaskPresets:
            preset = self.__modelMaskPresets[part.getPartFile()]
            self.__loadPresetIntoModelMaksEditorUI(preset)

    def start(self):
        self.__loadDS3PartUtil()
        self.__initUI()
        programDataFile = self.__tryLoadProgramData()

        if 'gameDirectory' in programDataFile and any(os.path.isfile(programDataFile['gameDirectory'] + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            currentText = self.__widgets['game_dir_entry'].get()
            self.__widgets['game_dir_entry'].delete(0, len(currentText))
            self.__widgets['game_dir_entry'].insert(0, programDataFile['gameDirectory'])
        self.__loadPartLists()
        self.__updateUIModdedPartList()
        self.__updateUIReplacedPartList()
        self.__updateUIGamePartList()
        self.__window.mainloop()

    def getWidgets(self):
        return self.__widgets

    @staticmethod
    def selectModdedPart(event):
        selection = soulsOutfitManager_global.getWidgets()['modded_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['modded_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            soulsOutfitManager_global.__selectModdedPart(part)
    
    @staticmethod
    def tryReplaceGamePart(event):
        selection = soulsOutfitManager_global.getWidgets()['game_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['game_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            moddedPart = soulsOutfitManager_global.__getSelectedModdedPart()
            
            if moddedPart == None:
                return

            result = messagebox.askokcancel('Replace game part with modded part?',
                'Are you sure you want to replace \"' 
                + str(part.getPartName()) + '\" with \"' 
                + str(moddedPart.getPartFile()) + '\"?'
                + '\nA backup will be created for you.')
            
            if result:
                soulsOutfitManager_global.__replaceGamePart(moddedPart, part)

    @staticmethod
    def tryDeleteGamePart(event):
        selection = soulsOutfitManager_global.getWidgets()['game_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['game_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            result = messagebox.askokcancel('Replace this game part with nothing?',
                'Are you you want to replace \"'
                + part.getPartName()
                + '\" with nothing?'
                + '\nA backup will be created for you.')
            
            if result:
                soulsOutfitManager_global.__deleteGamePart(part)

    @staticmethod
    def tryOpenModelMaskEditor(event):
        selection = soulsOutfitManager_global.getWidgets()['replaced_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['replaced_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            soulsOutfitManager_global.__tryLoadModelMaskPresetIntoEditor(part)

    @staticmethod
    def tryUpdateModelMaskPreset():
        selection = soulsOutfitManager_global.getWidgets()['replaced_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['replaced_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            soulsOutfitManager_global.__registerModelMaskPresetEdit(
                part,
                soulsOutfitManager_global.getWidgets()['model_mask_editor'].getItemCheckStates())
    
    @staticmethod
    def saveModelMaskChanges():
        selection = soulsOutfitManager_global.getWidgets()['replaced_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['replaced_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            soulsOutfitManager_global.__saveModelMaskPreset(part)

            if part.getPartFile() in soulsOutfitManager_global.__modelMaskPresets:
                soulsOutfitManager_global.__applyModelMaskPresetToGame(part,
                    soulsOutfitManager_global.__modelMaskPresets[part.getPartFile()])
    
    @staticmethod
    def tryRestorePart(event):
        selection = soulsOutfitManager_global.getWidgets()['replaced_part_list'].curselection()
        part = None
        
        if len(selection) == 1:
            part = soulsOutfitManager_global.getWidgets()['replaced_part_list'].getDS3PartInfo(selection[0])

        if part != None:
            result = messagebox.askokcancel('Restore this backup?',
                'Are you sure you want to restore this part to it\'s original?'
                + '\nAny file currently replacing it will be deleted.')
            
            if result:
                soulsOutfitManager_global.__restoreReplacedPart(part)

    @staticmethod
    def openBrowseForGameDirectory():
        directory = filedialog.askdirectory(mustexist=True)

        if any(os.path.isfile(directory + os.path.sep + EXEName) for EXEName in SoulsOutfitManager.supportedGameEXENames):
            programDataFile = soulsOutfitManager_global.__tryLoadProgramData()
            programDataFile['gameDirectory'] = directory
            soulsOutfitManager_global.__saveProgramData(programDataFile)
            currentText = soulsOutfitManager_global.getWidgets()['game_dir_entry'].get()
            soulsOutfitManager_global.getWidgets()['game_dir_entry'].delete(0, len(currentText))
            soulsOutfitManager_global.getWidgets()['game_dir_entry'].insert(0, directory)
            soulsOutfitManager_global.__updateUIModdedPartList()
            soulsOutfitManager_global.__updateUIGamePartList()
        elif len(directory) != 0:
            messagebox.showerror('Invalid Directory Given',
                'Could not find a valid EXE in the specified directory.'
                + '\nYou should select the directory containing the game EXE eg. steamapps\common\DARK SOULS III\Game')

    @staticmethod
    def refresh():
        soulsOutfitManager_global.__loadPartLists()
        soulsOutfitManager_global.__updateUIModdedPartList()
        soulsOutfitManager_global.__updateUIReplacedPartList()
        soulsOutfitManager_global.__updateUIGamePartList()
        modelMaskPatcher.attach()

    @staticmethod
    def moddedPartsSearchUpdate(event):
        soulsOutfitManager_global.__updateUIModdedPartList()

    @staticmethod
    def gamePartsSearchUpdate(event):
        soulsOutfitManager_global.__updateUIGamePartList()

    @staticmethod
    def replacedPartsSearchUpdate(event):
        soulsOutfitManager_global.__updateUIReplacedPartList()

global soulsOutfitManager_global
global modelMaskPatcher
soulsOutfitManager_global = SoulsOutfitManager()
modelMaskPatcher = DS3ModelMaskPatcher()
modelMaskPatcher.attach()
soulsOutfitManager_global.start()