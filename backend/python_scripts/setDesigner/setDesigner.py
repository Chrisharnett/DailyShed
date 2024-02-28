from setDesigner.notePatterns import getReviewNotePattern, getNextNotePattern, getNotePatternRhythmLength
from setDesigner.rhythmPatterns import getNewRhythmPattern, getRhythmReviewPattern, getMinPlays, rhythmPatternNoteLength
from setDesigner.createExercise import createExercise
from setDesigner.patternCollections import getCollection
from setDesigner.fetchExerciseDetails import fetchExercisesFromLog

def updateExerciseData(exercises, options):
    for index, exercise in enumerate(exercises):
        exercise['playCount'] = options[index].get('playCount')
        exercise['notePatternRhythmLength'] = options[index].get('notePatternRhythmLength')
        exercise['directions'] = options[index].get('directions')

    return exercises
def getExercisesFromHistory(matcher, exerciseHistory):
    options = []
    for exercise in exerciseHistory:
        if (exercise.get("rhythmMatcher") == matcher):
            options.append(exercise)
    return options


# TODO: after completing ascending patterns, then move on to other directions in order.
# TODO: currently, users must review patterns to add directions.
def createNewNoteExercise(exerciseDetails, exerciseHistory, previousSet, program):
    notePatternType = exerciseDetails['notePatternType']
    pitches, program = getNextNotePattern(program, notePatternType)
    if pitches == None:
        return createReviewNoteExercise(exerciseDetails, exerciseHistory), program
    pitches['notePatternRhythmLength'] = getNotePatternRhythmLength(pitches)
    if previousSet:
        options = getExercisesFromHistory(exerciseDetails.get('rhythmMatcher'), exerciseHistory)
        possibleExercises = fetchExercisesFromLog(options)
        possibleExercises = updateExerciseData(possibleExercises,options)
        # possibleRhythms = [exercise.get('rhythmPattern') for exercise in optionExercises]
        if 0 < len(possibleExercises):
            minPlays = getMinPlays(possibleExercises)
            rhythm = getRhythmReviewPattern(
                possibleExercises, minPlays, pitches.get('notePatternRhythmLength'), exerciseDetails
            )
        else:
            rhythm = getNewRhythmPattern(pitches.get['notePatternRhythmLength'], exerciseDetails["rhythmMatcher"])
    else:
        rhythmCollections = getCollection('rhythm')
        matchingCollections = [collection for collection in rhythmCollections if
                               exerciseDetails.get('rhythmMatcher') == collection.get('title')]
        rhythm = next(
            (pattern for collection in matchingCollections for pattern in collection['patterns']
            if pattern.get('rhythmDescription') == exerciseDetails.get('rhythmMatcher')
            and rhythmPatternNoteLength(pattern) == pitches.get('notePatternRhythmLength')),
            None
        )
        if rhythm is None:
            rhythm = getNewRhythmPattern(pitches.get('notePatternRhythmLength'),
                                         [collection for collection in getCollection('rhythm') if
                                         collection.get('collectionType') == 'rhythm' and
                                         exerciseDetails.get('rhythmMatcher') == collection.get('title')]
                                         )
    exercise = createExercise(pitches, rhythm, exerciseDetails)
    return exercise, program

def createReviewNoteExercise(exerciseDetails, exerciseHistory):
    notePatternType = exerciseDetails.get('notePatternType')
    notePatternOptions = []
    for exercise in exerciseHistory:
        if exercise.get('notePatternType') == notePatternType:
            notePatternOptions.append(exercise)
    possibleExercises = fetchExercisesFromLog(notePatternOptions)
    possibleExercises = updateExerciseData(possibleExercises, notePatternOptions)
    pitches = getReviewNotePattern(possibleExercises, exerciseDetails, exerciseHistory)
    if not pitches['notePatternRhythmLength']:
        pitches['notePatternRhythmLength'] = getNotePatternRhythmLength(pitches)
    rhythm = getNewRhythmPattern(
        pitches.get('notePatternRhythmLength'),
        [collection for collection in getCollection('rhythm') if
         collection.get('collectionType') == 'rhythm' and
         exerciseDetails.get('rhythmMatcher') == collection.get('title')]
    )
    return createExercise(pitches, rhythm, exerciseDetails)

def setDesigner(player):
    program = player.get('program')
    exerciseDetails = player.get('program').get('exerciseDetails')
    previousSet = player.get('previousSet')
    exerciseHistory = player.get('exerciseMetadata')

    newSet = []
    for exercise in exerciseDetails:
        if exercise.get('reviewBool') and previousSet:
            e = createReviewNoteExercise(exercise, exerciseHistory)
            newSet.append(e)
        else:
            e, program = createNewNoteExercise(exercise, exerciseHistory, previousSet, program)
            if e is None:
                 e = createReviewNoteExercise(exercise, exerciseHistory)
            newSet.append(e)
            player['program'] = program
    return newSet, player