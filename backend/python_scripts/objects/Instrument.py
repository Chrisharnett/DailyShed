class Instrument:
    def __init__(self, instrumentName, level, lowNote, highNote, defaultTonic, abbr):
        self.__instrumentName = instrumentName
        self.__level = level
        self.__lowNote = lowNote
        self.__highNote = highNote
        self.__defaultTonic = defaultTonic
        self.__abbr = abbr

    def toDict(self):
        return {
            "instrumentName": self.instrumentName,
            "level": self.level,
            "lowNote": self.lowNote,
            "highNote": self.highNote,
            "defaultTonic": self.defaultTonic
        }


    def __str__(self):
        return f"{self.level}_{self.instrumentName}"

    # instrumentName property
    @property
    def instrumentName(self):
        return self.__instrumentName

    @instrumentName.setter
    def instrumentName(self, instrumentName):
        self.__instrumentName = instrumentName

    # level property
    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level

    # lowNote property
    @property
    def lowNote(self):
        return self.__lowNote

    @lowNote.setter
    def lowNote(self, lowNote):
        self.__lowNote = lowNote

    # highNote property
    @property
    def highNote(self):
        return self.__highNote

    @highNote.setter
    def highNote(self, highNote):
        self.__highNote = highNote

    # defaultTonic property
    @property
    def defaultTonic(self):
        return self.__defaultTonic

    @defaultTonic.setter
    def defaultTonic(self, defaultTonic):
        self.__defaultTonic = defaultTonic

    @property
    def abbr(self):
        return self.__abbr

    @abbr.setter
    def abbr(self, abbr):
        self.__abbr = abbr
