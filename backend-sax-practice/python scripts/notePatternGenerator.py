from exerciseObjects import NotePattern, Collection

preamble = r"""#(set-global-staff-size 14)
        """
# All ascending scalar patterns
def notePatterns(minNote, maxNote, maxLength):
    PATTERN_ID = 0
    scale1Ascending=[]
    notes = []
    toneExercises = Collection('tone')
    scale1 = Collection('ninthScale1')

    # One note options
    for i in range(minNote, maxNote):
        notes = [i]
        toneExercises.addPattern(NotePattern(notePatternId=PATTERN_ID,
                                        notePatternType='tone',
                                        notePattern=notes,
                                        description=f'on the {i}',
                                        direction='long'))
        PATTERN_ID += 1

    scale1Ascending = []
    # Ascending scalar options
    for i in range(minNote + 1, maxNote + 1):
        notes = []
        for j in range(1, i+1):
            notes.append(j)
        if notes:
            scale1Ascending.append(notes)
            scale1.addPattern(NotePattern(notePatternId=PATTERN_ID,
                                        notePatternType='scale',
                                        notePattern=notes,
                                        description=f'to the {j}',
                                        direction='ascending'))
            PATTERN_ID += 1

    # All descending scalar patterns
    scale1Descending = [x[::-1] for x in scale1Ascending]
    for pattern in scale1Descending:
        scale1.addPattern(
            NotePattern(notePatternId=PATTERN_ID,
                        notePatternType='scale',
                        notePattern=notes,
                        description=f'from the {pattern[0]}',
                        direction='descending')
        )
        PATTERN_ID += 1

    # All descending and ascending scalar patterns
    for i in range(len(scale1Ascending)):
        combinedPattern = scale1Ascending[i] + scale1Descending[i][1:]
        scale1.addPattern(
            NotePattern(notePatternId=PATTERN_ID,
                        notePatternType='scale',
                        notePattern=notes,
                        description=f'to the {scale1Ascending[i][-1]}',
                        direction='Ascending Descending')
        )
        PATTERN_ID += 1

    descendingAscendingNoteScales = []
    for i in range(len(scale1Ascending)):
        combinedPattern = scale1Descending[i] + scale1Ascending[i][1:]
        scale1.addPattern(
            NotePattern(notePatternId=PATTERN_ID,
                        notePatternType='scale',
                        notePattern=notes,
                        description=f'from the {scale1Descending[i][0]}',
                        direction='Descending Ascending')
        )
        PATTERN_ID += 1

    return [toneExercises, scale1]



def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    notePatternCollections = notePatterns(minNote, maxNote, maxLength)

    for collection in notePatternCollections:
        print(collection)
        for pattern in collection.getNotePatterns():
            print(pattern)

if __name__ == '__main__':
    main()