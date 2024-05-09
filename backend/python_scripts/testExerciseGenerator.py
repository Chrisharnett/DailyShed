from exercise import Exercise
from exerciseCollections.collectionCreator import collectionCreator
from setDesigner.notePatterns import getNotePatternRhythmLength
import random
import math
import copy

GLOBAL_PREAMBLE = r"#(set-global-staff-size 28)"

def maxRhythmNoteLength(rhythms):
    return max(rhythms.get('patterns'), key=lambda x: x.get('rhythmLength')).get('rhythmLength')

def multipleBarRhythm(notePattern, rhythms):

    length = notePattern.get('noteLength')
    maxRhythmLength = maxRhythmNoteLength(rhythms)
    minimumNumberOfMeasures = math.ceil(length / maxRhythmLength)
    measureNumber = 0
    remainder = length
    r = []
    id = "Multi"
    rLength = 0
    artic = []
    while remainder > maxRhythmLength:
        # Get the rhythms that are at least length/minNumberOfMesures
        possibleRhythms = [
            x for x in rhythms.get('patterns') if length / minimumNumberOfMeasures <= x.get('rhythmLength')
        ]
        measure = random.choice(possibleRhythms)
        r.extend(measure.get('rhythmPattern'))
        id += str(measure.get('rhythmPatternId'))
        rLength += measure.get('rhythmLength')
        remainder -= measure.get('rhythmLength')
        if measure.get('articulation'):
            artic.extend(measure.get('articulation'))
    possibleRhythms = [x for x in rhythms.get('patterns') if x.get('rhythmLength') == remainder]
    lastMeasure = random.choice(possibleRhythms)
    rLength += lastMeasure.get('rhythmLength')
    if lastMeasure.get('articulation'):
        artic.extend(lastMeasure.get('articulation'))
    r.extend(lastMeasure.get('rhythmPattern'))
    random.shuffle(r)

    return {'rhythmPatternID': id,
            'rhythmDescription': lastMeasure.get('rhythmDescription'),
            'rhythmPattern': r,
            'rhythmLength': rLength,
            'timeSignature': lastMeasure.get('timeSignature'),
            'articulation': artic,
        }

def getRandomRhythmPattern(notePattern, rhythmCollection):
    matchingRhythms = [r for r in rhythmCollection.get('patterns') if r.get('rhythmLength') == notePattern.get('noteLength')]
    if matchingRhythms:
        return random.choice(matchingRhythms)
    else:
        return multipleBarRhythm(notePattern, rhythmCollection)


def applyNewDirection(direction, notePattern):
    match direction:
        case 'ascending':
            return notePattern
        case 'descending':
            return descendingPattern(notePattern)
        case 'ascending/descending':
            return ascendingDescendingPattern(notePattern)
        case 'descending/ascending':
            return descendingAscendingPattern(notePattern)
        case _:
            return notePattern

def descendingPattern(notePattern):
    descendingNotePattern = copy.deepcopy(notePattern)
    d = descendingNotePattern.get('notePattern').copy()
    d.reverse()
    descendingNotePattern['notePattern'] = d
    return newNoteLength(descendingNotePattern)

def ascendingDescendingPattern(notePattern):
    adPattern = copy.deepcopy(notePattern)
    a = adPattern.get('notePattern').copy()
    d = adPattern.get('notePattern').copy()
    d.reverse()
    a.pop()
    a.extend(d)
    adPattern['notePattern'] = a
    return newNoteLength(adPattern)

def descendingAscendingPattern(notePattern):
    daPattern = copy.deepcopy(notePattern)
    d = daPattern.get('notePattern').copy()
    d.reverse()
    d.pop()
    d.extend(daPattern['notePattern'])
    daPattern['notePattern'] = d
    return newNoteLength(daPattern)

def newNoteLength(notePattern):
    newLength = getNotePatternRhythmLength(notePattern.get('notePattern'), notePattern.get('holdLastNote'))
    notePattern['noteLength'] = newLength
    return notePattern

def main():
    tonic = 'g'
    mode = 'major'
    collections, programs = collectionCreator()
    exercises = []
    exerciseID = 0
    patternID = 0

    for pr in programs[1:]:
        for c in collections:
            if c.get('title') == pr.get('primaryCollectionTitle'):
                rhythmCollection = next((coll for coll in collections if coll.get('title') == pr.get('rhythmPatternTitle')))
                for p in c.get('patterns'):
                    patternID += 1
                    for d in p.get('directions'):
                        ex = Exercise(tonic, mode)
                        np = applyNewDirection(d, p)
                        ex.notePatternID = patternID
                        ex.notePattern = np.get('notePattern')
                        ex.directionIndex = None
                        ex.directions = np.get('directions')
                        ex.holdLastNote = np.get('holdLastNote')
                        ex.repeatMe = np.get('repeatMe')
                        rhythm = getRandomRhythmPattern(np, rhythmCollection)
                        ex.rhythmPatternID = None
                        ex.rhythmPattern = rhythm.get('rhythmPattern')
                        ex.articulation = rhythm.get('articulation')
                        ex.timeSignature = rhythm.get('timeSignature')
                        ex.rhythmPattern = rhythm.get('rhythmPattern')
                        ex.exerciseID = exerciseID
                        ex.exerciseName = f"{exerciseID}-{d.replace('/', '-')}"
                        ex.filename = f"TEST-{exerciseID}-{d.replace('/', '-')}"

                        exercises.append(ex)
                        exerciseID += 1

    for exercise in exercises:
        print(f"created {exercise.filename}")
        exercise.createImage()

if __name__ == '__main__':
    main()