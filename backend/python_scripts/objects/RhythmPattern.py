from objects.MusicPattern import MusicPattern

class RhythmPattern(MusicPattern):
    def __init__(self, rhythmPatternType, rhythmPattern, description, timeSignature=(4, 4), articulation = None, measureLength = None):
        super().__init__(rhythmPatternType, rhythmPattern, description)
        self.__timeSignature = timeSignature
        self.__articulation = articulation
        self.__measureLength = measureLength
        self.__rhythmLength = self.rhythmPatternNoteLength()

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
    def rhythmLength(self):
        return self.__rhythmLength

    def noDuplicateRhythms(self, patternList):
        for pattern in patternList:
            if pattern.get('rhythmPattern') == self.pattern:
                return False
        return True

    def rhythmPatternNoteLength(self):
        count = 0
        for r in self.pattern:
            for n in r:
                if isinstance(n, int) or n.isdigit():
                    count += 1
        n = sum(sublist.count("~") for sublist in self.pattern)
        count -= n
        return count

    def fillBar(self, element, numerator):
        bar = []
        for i in range(numerator):
            if (element[0] == 'r'):
                rhythm = int(element[1:])
            else:
                rhythm = int(element)
            for j in range(math.floor(rhythm / numerator)):
                bar.append([element])
        return bar

    def oneBarOfRhythm(self, numerator, denominator, note):
        oneBarOfRhythm = self.fillBar(denominator, numerator)
        return oneBarOfRhythm