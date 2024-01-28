from objects.exerciseObjects import NotePattern
from objects.collection import Collection

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
                                        rhythmMatcher='tone',
                                        description=f'on the {i}',
                                        direction='static',
                                        repeatMe=False,
                                        holdLastNote=False))
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
                                        rhythmMatcher='general',
                                        description=f'to the {j}',
                                        direction='ascending'))
            PATTERN_ID += 1

    return [toneExercises, scale1]



def main():
    minNote = 1
    maxNote = 9
    maxLength = 2 * (maxNote)
    notePatternCollections = notePatterns(minNote, maxNote, maxLength)

    for collection in notePatternCollections:
        print(collection)
        for pattern in collection.getPatterns:
            print(pattern)

if __name__ == '__main__':
    main()