import tkinter as tk

class DS3PartListbox(tk.Listbox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.__ds3PartInfoList = []
    
    def insert(self, index, element, ds3PartInfo):
        self.__ds3PartInfoList.insert(index, ds3PartInfo)
        super().insert(index, element)
    
    def delete(self, index1, index2=None):
        if index2 != None:
            del self.__ds3PartInfoList[index1:index2]
        else:
            del self.__ds3PartInfoList[index1]

        super().delete(index1, index2)
    
    def getDS3PartInfo(self, index):
        return self.__ds3PartInfoList[index]