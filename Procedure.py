class Procedure:
    path = ""
    name = ""

    def __init__(self):
        return
        
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def getPath(self):
        return self.path

    def getName(self):
        return self.name

    def setPath(self, path):
        self.path = path

    def setName(self, name):
        self.name = name