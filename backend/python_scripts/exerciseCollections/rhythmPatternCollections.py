def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern.get('rhythmPattern') == newPattern:
            return False
    # If the loop completes without finding a duplicate, add the new pattern
    return True


def singleNoteWholeToneRhythms(numerator, denominator):
    toneRhythmId = 0
    rhythmPatterns = []
    rhythmPatterns.append({
        'rhythmPatternId': str(toneRhythmId),
        'rhythmDescription': "single_note_long_tone",
        'rhythmPattern': [["1"]],
        'timeSignature': (numerator, denominator),
        'articulation': [{"articulation": "fermata", "index": 0, "name": "fermata"}]
    }
    )
    toneRhythmId += 1

    rhythmPatterns.append(
        {
            'rhythmPatternId': str(toneRhythmId),
            'rhythmDescription': "single_note_long_tone",
            'rhythmPattern': [["1"], ["~"], ["1"]],
            'timeSignature': (numerator, denominator),
            'articulation': [
                {"articulation": "fermata", "index": 0, "name": "fermata"},
                {"articulation": "fermata", "index": 1, "name": ""}
            ]
        }
    )

    toneRhythmId += 1

    return rhythmPatterns


def fillBar(element, numerator):
    bar = []
    for i in range(numerator):
        bar.append([element])
    return bar

# TODO: Use rhythmPattern objects.
def quarterNoteRhythms(numerator, denominator):
    # rhythm = str(denominator)
    rhythmId = 0
    rhythmPatterns = []
    rest = f"r{denominator}"

    rhythmPatterns.append({
        'rhythmPatternId': str(rhythmId),
        'rhythmDescription': "quarter_note",
        'rhythmPattern': fillBar(denominator, numerator),
        'timeSignature': (numerator, denominator),
        'articulation': None
    }
    )
    rhythmId += 1

    oneBarQuarterRests = fillBar(rest, numerator)
    # One pitch, 3 rests
    for i in range(numerator):
        oneBarQuarterNoteRhythm = fillBar(rest, numerator)
        oneBarQuarterNoteRhythm[i] = [denominator]
        if noDuplicateRhythms(oneBarQuarterNoteRhythm, rhythmPatterns) == True:
            rhythmPatterns.append(
                {
                    'rhythmPatternId': str(rhythmId),
                    'rhythmDescription': "quarter_note",
                    'rhythmPattern': oneBarQuarterNoteRhythm,
                    'timeSignature': (numerator, denominator),
                    'articulation': None
                }
            )
            rhythmId += 1

    for i in range(numerator):
        newPatterns = []
        for j in range(1 + i, numerator):
            oneBarQuarterNoteRhythm = fillBar(rest, numerator)
            oneBarQuarterNoteRhythm[i] = [denominator]
            oneBarQuarterNoteRhythm[j] = [denominator]
            if noDuplicateRhythms(oneBarQuarterNoteRhythm, rhythmPatterns) == True:
                rhythmPatterns.append(
                    {
                        'rhythmPatternId': str(rhythmId),
                        'rhythmDescription': "quarter_note",
                        'rhythmPattern': oneBarQuarterNoteRhythm,
                        'timeSignature': (numerator, denominator),
                        'articulation': None
                    }
                )
                rhythmId += 1

    oppositePatterns = []
    for pattern in rhythmPatterns[1:]:
        newPattern = []
        p = pattern.get('rhythmPattern')
        for r in p:
            if r == [denominator]:
                newPattern.append([rest])
            elif r == [rest]:
                newPattern.append([denominator])
        oppositePatterns.append(newPattern)

    for newPattern in oppositePatterns:
        if noDuplicateRhythms(newPattern, rhythmPatterns):
            rhythmPatterns.append(
                {
                    'rhythmPatternId': str(rhythmId),
                    'rhythmDescription': "quarter_note",
                    'rhythmPattern': newPattern,
                    'timeSignature': (numerator, denominator),
                    'articulation': None
                }
            )
            rhythmId += 1

    return rhythmPatterns


def main():
    # Time signature. Numerator has to be int, denominator a string.
    numerator = 4
    denominator = "4"
    rhythms = []
    rhythms.extend(singleNoteWholeToneRhythms(numerator, denominator))
    rhythms.extend(quarterNoteRhythms(numerator, denominator))
    for pattern in rhythms:
        print(pattern.get('rhythmPattern'))


if __name__ == "__main__":
    main()
