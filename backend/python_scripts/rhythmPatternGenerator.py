from objects.exerciseObjects import RhythmPattern


def noDuplicateRhythms(newPattern, patternList):
    for pattern in patternList:
        if pattern['rhythmPattern'] == newPattern:
            return False
    return True


def singleNoteWholeToneRhythms(numerator, denominator):
    toneRhythmId = 0
    rhythmPatterns = []
    rhythmPatterns.append({
            'rhythmPatternId':str(toneRhythmId),
            'rhythmDescription':"single note long tone",
            'rhythmPattern':[["1"]],
            'timeSignature':(numerator, denominator),
            'articulation':[{"articulation": "fermata", "index": 0, "name": "fermata"}]
        }
    )
    toneRhythmId += 1
    rhythmPatterns.append(
        {
            'rhythmPatternId': str(toneRhythmId),
            'rhythmDescription': "single note long tone",
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


# TODO: Use rhythmPattern objects.
def quarterNoteRhythms(numerator, denominator):
    rhythm = str(denominator)
    rhythmId = 0
    rhythmPatterns = []

    rhythmPatterns.append({
        'rhythmPatternId': str(rhythmId),
        'rhythmDescription': "quarter_note",
        'rhythmPattern': [["4"], ["4"], ["4"], ["4"]],
        'timeSignature': (numerator, denominator),
        'articulation': None
    }
    )
    rhythmId += 1

    oneBarQuarterRests = [["r4"], ["r4"], ["r4"], ["r4"]]

    # One pitch, 3 rests
    for i in range(numerator):
        oneBarQuarterNoteRhythm = [["r4"], ["r4"], ["r4"], ["r4"]]
        oneBarQuarterNoteRhythm[i] = [rhythm]
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
            oneBarQuarterNoteRhythm = oneBarQuarterRests.copy()
            oneBarQuarterNoteRhythm[i] = ["4"]
            oneBarQuarterNoteRhythm[j] = ["4"]
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

    rhythmPatterns.append(
        {
            'rhythmPatternId': str(rhythmId),
            'rhythmDescription': "quarter_note",
            'rhythmPattern': [["r4"], ["r4"], ["4"], ["4"]],
            'timeSignature': (numerator, denominator),
            'articulation': None
        }

    )
    rhythmId += 1

    oppositePatterns = []
    for pattern in rhythmPatterns:
        newPattern = []
        p = pattern['rhythmPattern']
        for r in p:
            if r == ["4"]:
                newPattern.append(["r4"])
            elif r == ["r4"]:
                newPattern.append(["4"])
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
        print(pattern.getRhythmPattern)


if __name__ == "__main__":
    main()
