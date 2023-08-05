class LoadEnv:
    def __init__(self, filename:str="./.env", erase_variable:bool=False):
        self.erase_variable = False
        self.filename = filename

        self.load()
    #endDef

    from ._loadenv import load, getEnvironVar
#endClass
