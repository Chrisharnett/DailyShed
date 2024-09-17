import abjad
# from musicData.fullScale import pitchesInRange
from musicData.modes import modeList
from musicData.pitchData import flatPitchSet, sharpPitchSet, sharpModes
from musicData.modes import getScaleDetails

class Scale:
    def __init__(self, tonic, mode, lowNote, highNote):
        self.__tonic = tonic
        self.__mode = mode
        self.__lowNote = lowNote
        self.__highNote = highNote
        self.__scalePattern = self.getScalePatternByName(mode)
        self.__notePattern = None
        self.__pitchesInRange = None

    def toDict(self):
        return {
            "tonic": self.tonic,
            "mode": self.mode,
            "lowNote": self.lowNote,
            "highNote": self.highNote
        }

    # tonic property
    @property
    def tonic(self):
        return self.__tonic

    @tonic.setter
    def tonic(self, tonic):
        self.__tonic = tonic

    # mode property
    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode

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

    # scalePattern property
    @property
    def scalePattern(self):
        return self.__scalePattern

    @scalePattern.setter
    def scalePattern(self, scalePattern):
        self.__scalePattern = scalePattern

    @property
    def notePattern(self):
        return self.__notePattern

    @notePattern.setter
    def notePattern(self, notePattern):
        self.__notePattern = notePattern

    @property
    def pitchesInRange(self):
        return self.__pitchesInRange

    @pitchesInRange.setter
    def pitchesInRange(self, pitchesInRange):
        self.__pitchesInRange = pitchesInRange

    def getPitchesInRange(self):
        scaleInfo = getScaleDetails(self.tonic, self.mode)
        if not scaleInfo:
            return flatPitchSet()
        if (self.tonic, self.mode) in sharpModes():
            baseScale = sharpPitchSet()
        else:
            baseScale = flatPitchSet()
        adjustments = scaleInfo.get('adjustments', {})
        adjustedScale = baseScale.copy()
        for i, note in enumerate(baseScale):
            if note[:-1] in adjustments:
                adjustedScale[i] = adjustments.get(note[:-1]) + baseScale[i][-1]
        return adjustedScale

    def __str__(self):
        string = ""
        for note in self.__notePattern:
            string += f"{note[0]}, "

        return f"{self.tonic[:-1].title()} {self.mode.title()}\n{string[:-1]}"

    def getScalePatternByName(self, name):
        result = [mode['modePattern'] for mode in modeList() if mode['modeName'] == name]
        return result[0] if result else None

    def getPitches(self):
        pitchSets = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "natural_minor": [0, 2, 3, 5, 7, 8, 10],
            "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
            "jazz_minor": [0, 2, 3, 5, 7, 9, 11],
        }
        return pitchSets

    def getNamedPitches(self, sequence):
        namedScalePitches = []
        for note in sequence:
            namedPitch = abjad.NamedPitch(note)
            namedScalePitches.append(namedPitch)
        self.__notePattern = namedScalePitches

    def makeScale(self):
        scalePitches = []
        tonic = abjad.NamedPitch(self.__tonic)
        for scalePitch in self.getPitches()[self.__mode]:
            pitch = tonic + scalePitch
            scalePitches.append(pitch)
        return scalePitches

    def getNotesInRange(self):
        allPitches = self.getPitchesInRange()
        if 'as3' in allPitches:
            self.lowNote = 'as3'
        #FIXME: allPitches have 'g01', not g1
        lowIndex = allPitches.index(self.lowNote)
        highIndex = allPitches.index(self.highNote)
        self.pitchesInRange = allPitches[lowIndex:highIndex + 1]

    def getForwardPattern(self):
        sequence = []
        tonicIndex = self.pitchesInRange.index(self.tonic)
        noteIndex = tonicIndex
        i, octave = 0, 0
        while noteIndex < len(self.pitchesInRange):
            sequence.append(self.pitchesInRange[noteIndex])
            i += 1
            if i >= len(self.scalePattern):
                octave += 1
                i = 0
            interval = self.scalePattern[i]
            noteIndex = (tonicIndex + interval + (octave * 12))
        return sequence

    def reversePattern(self, forwardPattern):
        sequence = forwardPattern[1:-1].copy()
        sequence.reverse()
        return sequence

    def descendFromTonic(self):
        tonicIndex = self.pitchesInRange.index(self.tonic)
        i = -1
        noteIndex = tonicIndex
        octave = 0
        lowRange = []
        while noteIndex > 0:
            lowRange.append(self.pitchesInRange[noteIndex])
            interval = self.scalePattern[i] - 12
            noteIndex = (tonicIndex + interval - (octave * 12))
            if i == 0:
                i = -1
                octave += 1
            i -= 1
        return lowRange

    def updateRange(self):
        lowIndex = self.pitchesInRange.index(self.lowNote)
        highIndex = self.pitchesInRange.index(self.highNote)
        newRange = self.pitchesInRange[lowIndex: highIndex + 1]
        self.pitchesInRange = newRange

    def getTonicInRange(self):
        if self.__tonic in self.pitchesInRange:
            return
        else:
            self.tonic = next(note for note in self.pitchesInRange if self.__tonic == note[:-1])

    def scalePatterns(self):
        return ['full_range_ascending_descending_scale', 'one_octave_ascending_descending_scale', 'two_octave_ascending_descending_scale', 'scale_to_the_ninth']

    def fullRangeAscendingScale(self):
        self.getNotesInRange()
        self.getTonicInRange()
        sequence = []
        sequence.extend(self.getForwardPattern())
        reverse = self.reversePattern(sequence)
        sequence.extend(reverse)
        descendFromTonic = self.descendFromTonic()
        sequence.extend(descendFromTonic)
        sequence.extend(self.reversePattern(descendFromTonic))
        self.getNamedPitches(sequence)

    def ascendingDescending(self):
        self.updateRange()
        sequence = []
        sequence.extend(self.getForwardPattern())
        reverse = self.reversePattern(sequence)
        sequence.extend(reverse)
        self.getNamedPitches(sequence)

    def oneOctaveAscendingDescendingScale(self):
        self.getNotesInRange()
        self.getTonicInRange()
        lowTonic = self.tonic
        octave = int(lowTonic[-1]) + 1
        self.highNote = lowTonic[:-1] + str(octave)
        self.ascendingDescending()

    def twoOctaveAscendingDescendingScale(self):
        self.getNotesInRange()
        self.getTonicInRange()
        lowTonic = self.tonic
        octave = int(lowTonic[-1]) + 2
        highNote = lowTonic[:-1] + str(octave)
        if highNote in self.pitchesInRange:
            self.highNote = highNote
        else:
            pass
        self.ascendingDescending()

    def scaleToTheNinth(self):
        self.getNotesInRange()
        self.getTonicInRange()
        sequence = self.getDefaultPattern()
        self.getNamedPitches(sequence)

    def getDefaultPattern(self):
        sequence = []
        tonicIndex = self.pitchesInRange.index(self.tonic)
        for note in self.notePattern:
            noteIndex = tonicIndex + note
            sequence.append(self.pitchesInRange[noteIndex])
        return sequence

    def defaultScaleExercise(self):
        self.getNotesInRange()
        self.getTonicInRange()
        sequence = self.getDefaultPattern()
        self.getNamedPitches(sequence)


