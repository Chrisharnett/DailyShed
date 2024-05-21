from exerciseCollections.notePatternCollections import singleNoteLongToneWholeNotes, stepwiseScaleNotePatterns, scaleExerciseCollection
from exerciseCollections.rhythmPatternCollections import singleNoteWholeToneRhythms, quarterNoteAndRestRhythms
from objects.PatternCollection import PatternCollection
from musicData.modes import modeList
from musicData.scalePatternLists import scaleExercisePatterns
from objects.PatternCollection import (ScalePatternCollection,
                                       ScaleToTheNinthBuilderCollection,
                                       SingleNoteLongToneRhythms,
                                       QuarterNoteAndRestCollection,
                                       EighthAndQuarterRhythms)

def collectionCreator():
    collections = []
    programs = []

    # newPattern, collectionLength = stepwiseScaleNotePatterns(1, 9)
    # notePatternTitle = "scale_to_the_ninth"
    # collections.append({
    #     'collectionType': 'notePattern',
    #     'title': notePatternTitle,
    #     'patterns': newPattern,
    #     'collectionLength': collectionLength
    # })
    # rhythmPatternTitle= 'quarter_note'
    # newPattern, collectionLength = quarterNoteAndRestRhythms(4, 4)
    # collections.append({
    #     'collectionType': 'rhythm',
    #     'title': rhythmPatternTitle,
    #     'patterns': newPattern,
    #     'collectionLength': collectionLength
    # })
    #
    # programs.append({'primaryCollectionTitle': notePatternTitle, 'rhythmPatternTitle' : rhythmPatternTitle})
    #
    # notePatternTitle = 'single_note_long_tone'
    # newPattern, collectionLength = singleNoteLongToneWholeNotes(1,9)
    # collections.append({
    #     'collectionType': 'notePattern',
    #     'title': notePatternTitle,
    #     'patterns': newPattern,
    #     'collectionLength': collectionLength
    # })
    # rhythmPatternTitle = 'single_note_long_tone_rhythms'
    # newPattern, collectionLength = singleNoteWholeToneRhythms(4, 4)
    # collections.append({
    #     'collectionType': 'rhythm',
    #     'title': rhythmPatternTitle,
    #     'patterns': newPattern,
    #     'collectionLength': collectionLength
    # })
    # programs.append({'primaryCollectionTitle': notePatternTitle, 'rhythmPatternTitle': rhythmPatternTitle})


    # scaleCollections = scaleExerciseCollections()
    # collections.append(scaleCollections)
    # programs.append({'primaryCollectionTitle': notePatternTitle, 'rhythmPatternTitle': rhythmPatternTitle})

    return collections, programs

def main():
    collections=[]
    timeSignature = (4, 4)
    collections.append(EighthAndQuarterRhythms(timeSignature))
    collections.append(QuarterNoteAndRestCollection(timeSignature))
    collections.append(SingleNoteLongToneRhythms(timeSignature))
    modes = modeList()
    scalePatterns = scaleExercisePatterns()
    for mode in modes:
        collections.append(ScaleToTheNinthBuilderCollection(mode))
        for scalePatternName in scalePatterns:
            collections.append(ScalePatternCollection(mode, scalePatternName))
    for collection in collections:
        for pattern in collection.patterns:
            print(pattern.pattern)



if __name__ == '__main__':
    main()
