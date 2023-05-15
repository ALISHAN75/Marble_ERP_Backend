# from typing_extensions import Self
from inventory.utility.InventoryUtil import InventoryUtil


class InventoryUtil(InventoryUtil):

    def addInventoryAdjustment(self):
        pass

def isSectioned( params):
    if "Sectioned" in params:
        return 1,0,0,0
    
    if "Sized" in params:
        return 0,1,0,0
    
    if "Gola" in params:
        return 0,0,1,0
    
    if "Polished" in params:
        return 0,0,0,1
    
    
