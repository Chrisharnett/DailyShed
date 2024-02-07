class Collection:
    def __init__(self, name):
        self.__name = name
        self.__notePatterns = []
        self.__rhythmPatterns = []
        self.__key = ""
        self.__mode = ""

    def __str__(self):
        return self.__name

    def __iter__(self):
        return iter(self.__notePatterns)

    def serialize(self):
        notePatterns = self.serializeNotePatterns()
        return {"name": self.__name, "notePatterns": notePatterns}

    def serializeNotePatterns(self):
        serializedNotePatterns = []
        for p in self.__notePatterns:
            serializedNotePatterns.append(p.serialize())
        return serializedNotePatterns

    @property
    def getName(self):
        return self.__name

    @property
    def getPatterns(self):
        return self.__notePatterns

    def addPattern(self, pattern):
        self.__notePatterns.append(pattern)
