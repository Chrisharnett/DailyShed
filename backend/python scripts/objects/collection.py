class Collection:
    def __init__(self, name):
        self.__name = name
        self.__notePatterns = []

    def __str__(self):
        return self.__name

    def __iter__(self):
        return iter(self.__notePatterns)

    @property
    def getName(self):
        return self.__name

    @property
    def getPatterns(self):
        return self.__notePatterns

    def addPattern(self, pattern):
        self.__notePatterns.append(pattern)
