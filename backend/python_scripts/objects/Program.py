class Program:
    def __init__(self, tonic=None, mode=None, primaryCollection=None, rhythmCollection=None, tonicSequence=None, instrument = None):
        self.__tonic = tonic
        self.__mode = mode
        self.__primaryCollection = primaryCollection
        self.__rhythmCollection = rhythmCollection
        self.__tonicSequence = tonicSequence
        self.__instrument = instrument

    def __str__(self):
        return f"{self.instrument.level},{self.instrument.instrumentName},{self.tonic},{self.primaryCollection}"

    @property
    def tonic(self):
        return self.__tonic

    @tonic.setter
    def tonic(self, value):
        self.__tonic = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def primaryCollection(self):
        return self.__primaryCollection

    @primaryCollection.setter
    def primaryCollection(self, value):
        self.__primaryCollection = value

    @property
    def rhythmCollection(self):
        return self.__rhythmCollection

    @rhythmCollection.setter
    def rhythmCollection(self, value):
        self.__rhythmCollection = value

    @property
    def tonicSequence(self):
        return self.__tonicSequence

    @tonicSequence.setter
    def tonicSequence(self, value):
        self.__tonicSequence = value

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    def instrument(self, value):
        self.__instrument = value

