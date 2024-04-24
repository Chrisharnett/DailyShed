from objects.exerciseObjects import NotePattern

preamble = r"""#(set-global-staff-size 14)
        """

def singleNoteLongToneWholeNotes(minNote, maxNote):
    PATTERN_ID = 0
    toneExercises = []

    # One note options
    for i in range(minNote, maxNote):
        notes = [i]
        directions = ["static"]
        toneExercises.append(
            {
            'notePatternId': str(PATTERN_ID),
            'notePatternType': "single_note_long_tone",
            'notePattern': notes,
            'description': f"Scale note {i}. Play for one full breath. Strive full a full, steady, in tune sound. Repeat until you play 2 good notes.",
            'direction': "static",
            'directions': directions,
            'repeatMe': False,
            'holdLastNote': False
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
        for j in range(1, i + 1):
            notes.append(j)
        if notes:
            scale1.append(
                {
                    'notePatternId':str(PATTERN_ID),
                    'notePatternType':"scale",
                    'notePattern':notes,
                    'description':f"Play twice. Repeat both times.",
                    'direction': 'ascending',
                    'directions':directions,
                    'repeatMe': True,
                    'holdLastNote': True
                }
            )
            PATTERN_ID += 1
    collectionLength = len(scale1) * len(directions)
    return scale1, collectionLength
