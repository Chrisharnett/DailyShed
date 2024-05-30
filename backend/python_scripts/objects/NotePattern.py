from objects.MusicPattern import MusicPattern

class NotePattern(MusicPattern):
    def __init__(self, notePatternType, notePattern, description, directions = ['ascending', 'descending', 'ascending_descending', 'descending_ascending'], repeatMe = False, holdLastNote = False, patternID=None):
        super().__init__(notePatternType, notePattern, description, patternID=patternID)
        self.__noteLength = len(notePattern)
        self.__directions = directions
        self.__repeatMe = repeatMe
        self.__holdLastNote = holdLastNote

    def __str__(self):
        return self.__description

    @property
    def noteLength(self):
        return self.__noteLength

    @noteLength.setter
    def noteLength(self, value):
        self.__noteLength = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def directions(self):
        return self.__directions

    @directions.setter
    def directions(self, value):
        self.__directions = value

    @property
    def repeatMe(self):
        return self.__repeatMe

    @repeatMe.setter
    def repeatMe(self, value):
        self.__repeatMe = value

    @property
    def holdLastNote(self):
        return self.__holdLastNote

    @holdLastNote.setter
    def holdLastNote(self, value):
        self.__holdLastNote = value

class LongTone(NotePattern):
    def __init__(self, notePatternType, notePattern, description, directions='static', repeatMe = False, holdLastNote = False, patternID=None):
        super().__init__(notePatternType, notePattern, description, directions, repeatMe, holdLastNote, patternID)
        self.__scalePatternType = 'long_tone'

    @property
    def scalePatternType(self):
        return self.__scalePatternType

    @scalePatternType.setter
    def scalePatternType(self, scalePattern):
        self.__scalePatternType = scalePattern

class ScalePattern(NotePattern):
    def __init__(self, notePatternType, notePattern, description, scalePatternType, directions = ['ascending', 'descending', 'ascending_descending', 'descending_ascending'], repeatMe = True, holdLastNote = True, patternID=None):
        super().__init__(notePatternType, notePattern, description, directions, repeatMe, holdLastNote, patternID=patternID)
        self.__scalePatternType = scalePatternType

    @property
    def scalePatternType(self):
        return self.__scalePatternType

    @scalePatternType.setter
    def scalePatternType(self, scalePattern):
        self.__scalePatternType = scalePattern


class CreativePattern(NotePattern):
    def __init__(self, notePatternType, notePattern, description, directions, repeatMe = False, holdLastNote = False, patternID=None):
        super().__init__(notePatternType, notePattern, description, directions, repeatMe, holdLastNote, patternID=patternID)

class CustomPattern(NotePattern):
    def __init__(self, notePatternType, notePattern, description, directions, repeatMe = False, holdLastNote = False, patternID=None):
        super().__init__(notePatternType, notePattern, description, directions, repeatMe, holdLastNote, patternID=patternID)