from musicData.modes import modeList
from musicData.scalePatternLists import scaleExercisePatterns
from objects.PatternCollection import (ScalePatternCollection,
                                       ScaleToTheNinthBuilderCollection,
                                       SingleNoteLongToneRhythms,
                                       QuarterNoteAndRestCollection,
                                       EighthAndQuarterRhythms,
                                       SingleNoteDiatonicLongToneCollection)
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
    scalePatterns = scaleExercisePatterns()
    for mode in modes:
        collections.append(SingleNoteDiatonicLongToneCollection(mode))
        collections.append(ScaleToTheNinthBuilderCollection(mode))
        for scalePatternName in scalePatterns:
            collections.append(ScalePatternCollection(mode, scalePatternName))
    defaultPrograms = []

    for instrument in getInstrumentsBySkillLevel('beginner'):
        scaleToTheNinth = next((collection for collection in collections if collection.title == 'major,scale_to_the_ninth') or None)
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
