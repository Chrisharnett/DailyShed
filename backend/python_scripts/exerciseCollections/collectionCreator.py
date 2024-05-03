from exerciseCollections.notePatternCollections import singleNoteLongToneWholeNotes, stepwiseScaleNotePatterns
from exerciseCollections.rhythmPatternCollections import singleNoteWholeToneRhythms, quarterNoteRhythms

def collectionCreator():
    collections = []
    programs = []

    newPattern, collectionLength = stepwiseScaleNotePatterns(1, 9)
    notePatternTitle = "scale_to_the_ninth"
    collections.append({
        'collectionType': 'notePattern',
        'title': notePatternTitle,
        'patterns': newPattern,
        'collectionLength': collectionLength
    })
    rhythmPatternTitle= 'quarter_note'
    newPattern, collectionLength = quarterNoteRhythms(4, 4)
    collections.append({
        'collectionType': 'rhythm',
        'title': rhythmPatternTitle,
        'patterns': newPattern,
        'collectionLength': collectionLength
    })

    programs.append({'primaryCollectionTitle': notePatternTitle, 'rhythmPatternTitle' : rhythmPatternTitle})

    notePatternTitle = 'single_note_long_tone'
    newPattern, collectionLength = singleNoteLongToneWholeNotes(1,9)
    collections.append({
        'collectionType': 'notePattern',
        'title': notePatternTitle,
        'patterns': newPattern,
        'collectionLength': collectionLength
    })
    rhythmPatternTitle = 'single_note_long_tone_rhythms'
    newPattern, collectionLength = singleNoteWholeToneRhythms(4, 4)
    collections.append({
        'collectionType': 'rhythm',
        'title': rhythmPatternTitle,
        'patterns': newPattern,
        'collectionLength': collectionLength
    })
    programs.append({'primaryCollectionTitle': notePatternTitle, 'rhythmPatternTitle': rhythmPatternTitle})

    return collections, programs
