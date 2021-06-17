import json
from tkinter import messagebox
from enum import Enum

class EquipModelCategory(Enum):
    HEAD = 'hd'
    BODY = 'bd'
    ARMS = 'am'
    LEGS = 'lg'
    WEAPON = 'wp'

class EquipModelGender(Enum):
    MALE = 'm'
    FEMALE = 'f'
    ALL = 'a'

class DS3PartUtil:
    def __init__(self, partNamesLayoutFile):
        try:
            self.__partNames = json.load(open(partNamesLayoutFile))
        except FileNotFoundError as error:
            print(error)
            messagebox.showerror('SoulsOutfitManager Error', str(error) 
                + "\n\nPlease assure you don't move SoulsOutfitManager outside the same folder where \"assets\" is contained.")
            exit()

    def getPartNameFromPartFile(self, partFile):
        name = 'Unknown'

        if len(partFile.split('.')) == 0:
            return name

        partNameSections = partFile.split('.')[0].split('_')

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
    
    def getEquipModelIdFromPartFile(self, partFile):
        if len(partFile.split('.')) < 1:
            return None

        equipModelId = partFile.split('.')[0]
        
        if len(equipModelId.split('_')) > 2:
            try:
                return int(equipModelId.split('_')[2])
            except ValueError:
                return None
        else:
            return None
    
    def getEquipModelGenderFromPartFile(self, partFile):
        if len(partFile.split('.')) < 1:
            return None

        equipModelId = partFile.split('.')[0]
        
        if len(equipModelId.split('_')) > 2:
            for equipModelGender in EquipModelGender:
                if equipModelGender.value == equipModelId.split('_')[1].lower():
                    return equipModelGender.value
            
            return None
        else:
            return None
    
    def getEquipModelCategoryFromPartFile(self, partFile):
        if len(partFile.split('.')) < 1:
            return None

        equipModelId = partFile.split('.')[0]
        
        if len(equipModelId.split('_')) > 2:
            for equipModelCategory in EquipModelCategory:
                if equipModelCategory.value == equipModelId.split('_')[0].lower():
                    return equipModelCategory.value
            
            return None
        else:
            return None