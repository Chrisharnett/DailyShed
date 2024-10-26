from objects.MusicPattern import MusicPattern
import math

class RhythmPattern(MusicPattern):
    def __init__(self, rhythmPatternType, rhythmPattern, description, timeSignature=(4, 4), articulation = None, measureLength = None, patternID=None):
        super().__init__(rhythmPatternType, rhythmPattern, description, patternID)
        self.__timeSignature = timeSignature
        self.__articulation = articulation
        self.__measureLength = measureLength
        self.__rhythmLength = self.rhythmPatternNoteLength()
        self.__patternID = patternID

    @property
    def timeSignature(self):
        return self.__timeSignature

    @timeSignature.setter
    def timeSignature(self, value):
        self.__timeSignature = value

    @property
    def articulation(self):
        return self.__articulation

    @articulation.setter
    def articulation(self, value):
        self.__articulation = value

    @property
    def measureLength(self):
        return self.__measureLength

    @measureLength.setter
    def measureLength(self, value):
        self.__measureLength = value

    @property
    def patternID(self):
        return self.__patternID

    @patternID.setter
    def patternID(self, patternID):
        self.__patternID = patternID

    @property
    def rhythmLength(self):
        return self.__rhythmLength

    def rhythmPatternNoteLength(self):
        count = 0
        for r in self.pattern:
            for n in r:
                if isinstance(n, int) or n.isdigit():
                    count += 1
        n = sum(sublist.count("~") for sublist in self.pattern)
        count -= n
        return count

    def oneBarOfRhythm(self, numerator, denominator, note):
        oneBarOfRhythm = self.fillBar(denominator, numerator)
        return oneBarOfRhythm