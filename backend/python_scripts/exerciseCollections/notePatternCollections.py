
def getNotePatternRhythmLength(pattern, holdLastNote):
    if holdLastNote:
        length = len(pattern) - 1
        return length
    length = len(pattern)
    return length

preamble = r"""#(set-global-staff-size 14)
        """

def singleNoteLongToneWholeNotes(minNote, maxNote):
    PATTERN_ID = 0
    toneExercises = []

    # One note options
    for i in range(minNote, maxNote):
        notes = [i]
        directions = ['static']
        holdLastNote = False
        toneExercises.append(
            {
            'notePatternId': str(PATTERN_ID),
            'notePatternType': "single_note_long_tone",
            'notePattern': notes,
            'description': f"Scale note {i}. Play for one full breath. Strive full a full, steady, in tune sound. Repeat until you play 2 good notes.",
            'noteLength': getNotePatternRhythmLength(notes, holdLastNote),
            'direction': "static",
            'directions': directions,
            'repeatMe': False,
            'holdLastNote': holdLastNote
            }
            )
        PATTERN_ID += 1

    collectionLength = len(toneExercises) * len(directions)

    return toneExercises, collectionLength

# All ascending scalar patterns
def stepwiseScaleNotePatterns(minNote, maxNote):
    PATTERN_ID = 0
    scale1 = []

    # Ascending scalar options
    for i in range(minNote + 1, maxNote + 1):
        notes = []
        directions = ['ascending', 'descending', 'ascending/descending', 'descending/ascending']
        holdLastNote = True
        for j in range(1, i + 1):
            notes.append(j)
        if notes:
            scale1.append(
                {
                    'notePatternId':str(PATTERN_ID),
                    'notePatternType':"scale",
                    'notePattern':notes,
                    'noteLength': getNotePatternRhythmLength(notes, holdLastNote),
                    'description':f"Play twice. Repeat both times.",
                    'direction': 'ascending',
                    'directions':directions,
                    'repeatMe': True,
                    'holdLastNote': holdLastNote
                }
            )
            PATTERN_ID += 1
    collectionLength = len(scale1) * len(directions)
    return scale1, collectionLength
