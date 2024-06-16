from musicData.modes import modeList
from musicData.scalePatternLists import (scalePatternPrograms)
from objects.PatternCollection import (ScalePatternCollection,
                                       ScaleToTheNinthBuilderCollection,
                                       SingleNoteLongToneRhythms,
                                       QuarterNoteAndRestCollection,
                                       EighthAndQuarterRhythms,
                                       SingleNoteDiatonicLongToneCollection)
from objects.NotePattern import (LongTone, ScalePattern)
from musicData.instruments import getInstrumentsBySkillLevel
from musicData.tonicSequences import tonicSequenceList
from objects.Program import Program

def collectionCreator():
    collections = []
    timeSignature = (4, 4)
    collections.append(EighthAndQuarterRhythms(timeSignature))
    collections.append(QuarterNoteAndRestCollection(timeSignature))
    collections.append(SingleNoteLongToneRhythms(timeSignature))
    modes = modeList()
    scalePatterns = scalePatternPrograms()
    rhythmPatterns = [pattern for pattern in scalePatterns if pattern.get('rhythmType') == 'rhythm' and pattern.get('scalePatternType') != 'scale_to_the_ninth_builder']
    tonePatterns = [pattern for pattern in scalePatterns if pattern.get('rhythmType') == 'long_tone_rhythm']
    for mode in modes:
        for tonePattern in tonePatterns:
            # LongToneCollections
            longToneCollection = SingleNoteDiatonicLongToneCollection(mode, tonePattern.get('scalePatternType'), False)
            modePattern = mode.get('modePattern')
            id = 0
            for note in modePattern:
                directions = ['static']
                holdLastNote = False
                repeatMe = False
                description = f"{longToneCollection.title.title().replace('_', ' ')}. Play twice. Internalize the sound you create."
                longToneCollection.addPattern(LongTone(longToneCollection.collectionType, [note], description, directions,
                                         holdLastNote=holdLastNote, repeatMe=repeatMe, patternID=str(id)))
                id += 1
            collections.append(longToneCollection)

        # Beginner Scale to the ninth
        ninthScales = ScaleToTheNinthBuilderCollection(mode, False)
        directions = ['ascending', 'descending', 'ascending/descending', 'descending/ascending']
        holdLastNote = True
        repeatMe = True
        modePattern = mode.get('modePattern')
        topNote = modePattern[0] + 12
        ninth = modePattern[1] + 12
        modePattern.append(topNote)
        modePattern.append(ninth)
        notePatterns = ninthScales.createPatternLists(modePattern)
        for pattern in notePatterns:
            id = 0
            #  FIXME
            description = f"{ninthScales.title.title().replace('_', ' ')}. Play twice. Repeat both times."
            ninthScales.addPattern(ScalePattern(ninthScales.collectionType, pattern, description, ninthScales.scalePatternType, directions,
                                         holdLastNote=holdLastNote, repeatMe=repeatMe, patternID=str(id)))
            id += 1

        # Scales
        collections.append(ninthScales)
        for i, scalePattern in enumerate(rhythmPatterns):
            scales = ScalePatternCollection(mode, scalePattern.get('scalePatternType'), True)
            notePattern = mode.get('modePattern')
            description = f"{scales.title.title().replace('_', ' ')}. Play twice. Repeat both times."
            scales.addPattern(
                ScalePattern(scales.collectionType, notePattern, description, scales.scalePatternType, patternID=str(i)))
            collections.append(scales)
    defaultPrograms = []

    for instrument in getInstrumentsBySkillLevel('beginner'):
        scaleToTheNinth = next((collection for collection in collections if collection.title == 'major,scale_to_the_ninth_builder') or None)
        quarterNotes = next((collection for collection in collections if collection.title == 'quarter_note_in_4-4') or None)
        tonicSequence = next((sequence for sequence in tonicSequenceList() if sequence.get('name') == 'circle_of_fifths') or None)
        tonic = instrument.defaultTonic
        defaultPrograms.append(Program(tonic, 'major', scaleToTheNinth, quarterNotes, tonicSequence, instrument))
        longTones = next((collection for collection in collections if collection.title == 'major,single_note_long_tone') or None)
        longToneRhythms = next((collection for collection in collections if collection.title == 'single_note_long_tone_rhythms_in_4-4') or None)
        defaultPrograms.append(Program(tonic, 'major', longTones, longToneRhythms, tonicSequence, instrument))

    return collections, defaultPrograms

def main():
    collections, defaultPrograms = collectionCreator()

if __name__ == '__main__':
    main()