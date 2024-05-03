from setDesigner.notePatterns import getReviewNotePattern, getNextNotePattern, getNotePatternRhythmLength
from setDesigner.rhythmPatterns import getNewRhythmPattern, getRhythmReviewPattern, getMinPlays, rhythmPatternNoteLength
from setDesigner.createExercise import createExercise
from setDesigner.patternCollections import getCollection
from setDesigner.fetchExerciseDetails import fetchExercisesFromLog
from setDesigner.queries import getPracticeSession, getUserHistory, getPreviousSet

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

def getNewExercise(interval):
    # Get next set of pitches from collection.
    # If no new set of pitches, get review pitches. If all rated 5, go to next key.
    # If history, get random matching rhythm from history.
    # If no history, get next matching rhythm in collection.
    exercise = None
    return exercise

def setDesigner(sub):
    z

    # program = userRoutineDetails['program']
    # exerciseDetails = userRoutineDetails.get('program').get('exerciseDetails')
    # previousSet = userRoutineDetails.get('previousSet')
    # exerciseHistory = userRoutineDetails.get('exerciseMetadata')
    # exerciseHistory = userRoutineDetails.get('exerciseHistory')
    #
    # newSet = []
    # for interval in practiceSession:
    #     if interval['reviewExercise'] and previousSet:
    #         newExercise = createReviewNoteExercise(interval, history)
    #         newSet.append(newExercise)
    #     else:
    #         # newExercise, updatedProgram = createNewNoteExercise(exercise, history, previousSet, program)
    #         newExercise = getNewExercise(interval)
    #
    #         if newExercise is None:
    #              newExercise = createReviewNoteExercise(interval, history)
    #         newSet.append(newExercise)
    #         # player['program'] = updatedProgram
    return newSet
    # return newSet, player