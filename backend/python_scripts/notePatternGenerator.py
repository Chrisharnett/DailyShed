from objects.exerciseObjects import NotePattern

preamble = r"""#(set-global-staff-size 14)
        """

def singleNoteLongToneWholeNotes(minNote, maxNote, maxLength):
    PATTERN_ID = 0
    toneExercises = []

    # One note options
    for i in range(minNote, maxNote):
        notes = [i]
        toneExercises.append(
            NotePattern(
                notePatternId="single_note_long_tone_" + str(PATTERN_ID),
                notePatternType="single_note_long_tone",
                notePattern=notes,
                rhythmMatcher="tone",
                description=f"on the {i}",
                direction="static",
                repeatMe=False,
                holdLastNote=False,
            )
        )
        PATTERN_ID += 1

    return toneExercises

# All ascending scalar patterns
def stepwiseScaleNotePatterns(minNote, maxNote, maxLength):
    PATTERN_ID = 0
    scale1Ascending = []
    notes = []
    # toneExercises = Collection("tone")
    # scale1 = Collection("ninthScale1")

    scale1 = []

    scale1Ascending = []
    # Ascending scalar options
    for i in range(minNote + 1, maxNote + 1):
        notes = []
        for j in range(1, i + 1):
            notes.append(j)
        if notes:
            scale1Ascending.append(notes)
            scale1.append(
                NotePattern(
                    notePatternId="stepwise_scale_" + str(PATTERN_ID),
                    notePatternType="stepwise_scale",
                    notePattern=notes,
                    rhythmMatcher="Quarter Note",
                    description=f"to the {j}",
                    direction="ascending",
                )
            )
            PATTERN_ID += 1

    return scale1


def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    notePatternCollections = []
    notePatternCollections.extend(stepwiseScaleNotePatterns(minNote, maxNote, maxLength))
    notePatternCollections.extend(singleNoteLongToneWholeNotes(minNote, maxNote, maxLength))

    for collection in notePatternCollections:
        print(collection)


if __name__ == "__main__":
    main()
