import pymem
from DS3PartUtil import EquipModelCategory

class DS3ModelMaskPatcher:
    """Patches Params in DARK SOULS III's memory for part model masks"""

    def __init__(self):
        self.__pyMem = pymem.Pymem('DarkSoulsIII.exe')
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
                    return self.__pyMem.read_bytes(baseAddress, 1)[0]
                except pymem.exception.MemoryReadError as error:
                    return None
            elif cTypeName == 'int16':
                try:
                    return self.__pyMem.read_short(baseAddress)
                except pymem.exception.MemoryReadError as error:
                    return None
            elif cTypeName == 'int32':
                try:
                    return self.__pyMem.read_int(baseAddress)
                except pymem.exception.MemoryReadError as error:
                    return None
            elif cTypeName == 'uint64':
                try:
                    return self.__pyMem.read_ulonglong(baseAddress)
                except pymem.exception.MemoryReadError as error:
                    return None
            elif cTypeName == 'float':
                try:
                    return self.__pyMem.read_float(baseAddress)
                except pymem.exception.MemoryReadError as error:
                    return None

        
        try:
            address = self.__pyMem.read_ulonglong(baseAddress)
        except pymem.exception.MemoryReadError as error:
            return None

        offsets.pop(0)
        offset = offsets[0]
        offsets[0] = address + offset
        return self.__accessMultilevelPointer(cTypeName, offsets)

    def __loadEquipParamProtector(self):
        self.__paramOffset = self.__accessMultilevelPointer('uint64',
            [self.__pyMem.base_address + 0x4798118, 0xB8, 0x68, 0x68])
        tableSize = self.__accessMultilevelPointer('int16',
            [self.__paramOffset + 0xA])

        for i in range(tableSize):
            paramId = self.__accessMultilevelPointer('uint64',
                [self.__paramOffset + 0x40 + 0x18 * i])
            idOffset = self.__accessMultilevelPointer('uint64',
                [self.__paramOffset + 0x48 + 0x18 * i])
            self.__paramTable[paramId] = self.__paramOffset + idOffset

    def getParamIdByEquipModelIdAndEquipModelCategory(self, equipModelId, equipModelCategory):
        equipModelCategoryId = None
        
        if equipModelCategory.lower() == EquipModelCategory.HEAD.value:
            equipModelCategoryId = 5
        elif equipModelCategory.lower() == EquipModelCategory.BODY.value:
            equipModelCategoryId = 2
        elif equipModelCategory.lower() == EquipModelCategory.ARMS.value:
            equipModelCategoryId = 1
        elif equipModelCategory.lower() == EquipModelCategory.LEGS.value:
            equipModelCategoryId = 6
        else:
            return None

        for paramId in self.__paramTable:
            try:
                if self.__pyMem.read_bytes(self.__paramTable[paramId] + 0xD0, 1)[0] == equipModelCategoryId and equipModelId == self.__pyMem.read_ushort(self.__paramTable[paramId] + 0xA0):
                    return paramId
            except pymem.exception.MemoryReadError as error:
               continue
        
        return None

    def readModelMask(self, id, maskOffset):
        try:
            return self.__pyMem.read_bytes(self.__paramTable[id] + 0x12E + maskOffset, 1)[0]
        except pymem.exception.MemoryReadError as error:
            return None

    def writeModelMask(self, id, maskOffset, isHide):
        try:
            self.__pyMem.write_bytes(self.__paramTable[id] + 0x12E + maskOffset, bytes([isHide]), 1)
        except pymem.exception.MemoryReadError as error:
            return

    def isAttached(self):
        result = None

        try:
            result = self.__accessMultilevelPointer('uint64',
                [self.__pyMem.base_address + 0x4798118])
        except pymem.exception.ProcessError as error:
            return False
        
        if result != None:
            return True
        else:
            return False
    
    def isParamsDefined(self):
        return self.__paramOffset != None

    def undefineParams(self):
        self.__paramOffset = None
        self.__paramTable = {}

    def attach(self):
        try:
            self.__pyMem.open_process_from_name('DarkSoulsIII')
        except pymem.exception.ProcessNotFound as error:
            return
        except pymem.exception.CouldNotOpenProcess as error:
            return
        
        if not self.isAttached():
            return

        try:
            self.__loadEquipParamProtector()
            return
        except TypeError as error:
            self.undefineParams()
            return
        except pymem.exception.ProcessNotFound as error:
            return
        except pymem.exception.MemoryReadError as error:
            return
