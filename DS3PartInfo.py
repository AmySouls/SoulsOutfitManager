from DS3PartUtil import DS3PartUtil

class DS3PartInfo:
    """Stores info about a DARK SOULS III part"""

    def __init__(self, ds3PartUtil, directory, partFile):
        self.__directory = directory
        self.__partFile = partFile
        self.__partName = ds3PartUtil.getPartNameFromPartFile(partFile)
        self.__equipModelId = ds3PartUtil.getEquipModelIdFromPartFile(partFile)
        self.__equipModelGender = ds3PartUtil.getEquipModelGenderFromPartFile(partFile)
        self.__equipModelCategory = ds3PartUtil.getEquipModelCategoryFromPartFile(partFile)
    
    def getDirectory(self):
        return self.__directory
    
    def getPartFile(self):
        return self.__partFile
    
    def getPartName(self):
        return self.__partName
    
    def getEquipModelId(self):
        return self.__equipModelId
    
    def getEquipModelGender(self):
        return self.__equipModelCategory
    
    def getEquipModelCategory(self):
        return self.__equipModelCategory