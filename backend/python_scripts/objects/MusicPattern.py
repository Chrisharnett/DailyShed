class MusicPattern:
    def __init__(self, patternType, pattern, description, patternID=None):
        self.__patternType = patternType
        self.__pattern = pattern
        self.__description = description
        self.__collectionPatternID = patternID

    @property
    def patternType(self):
        return self.__patternType

    @patternType.setter
    def patternType(self, value):
        self.__patternType = value

    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, value):
        self.__pattern = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value
