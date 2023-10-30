import random
from objects.exerciseObjects import Exercise

class PracticeSet:
    def __init__(self, player, notePatternCollections, rhythmPatterns):
        self.__player = player
        self.__notePatternCollections = notePatternCollections
        self.__rhythmPatterns = rhythmPatterns

    # TODO PICK THINGS UP HERE

    def minPlayCount(self, type):
        if len(self.__player.exerciseHistory) == 0:
            return None
        return min(self.__player.exerciseHistory, key = lambda x:x.getPlayCount).getPlayCount

    def getNoteReviewPatterns(self, min, type):
        reviewPatterns = [playerExercise.getExercise.getPitchPattern for playerExercise in self.__player.exerciseHistory if
                             playerExercise.getPlayCount == min and
                             playerExercise.getExercise.getPitchPattern.getRhythmMatcher == type]
        return reviewPatterns
    @property
    def getNextSet(self):
        currentSetPattern = self.__player.getSetPattern
        newSet = []
        setLength = len(currentSetPattern)
        # set the length of the new set with None values
        for n in range(setLength):
            newSet.append(None)


        #  Create a set for a new player
        if len(self.__player.getPreviousSet) == 0:
            for i in range(setLength - 1):
                if newSet[i] is None:
                    if currentSetPattern[i].get('type') == 'tone':
                        tonePatternCollection = next((collection for collection in self.__notePatternCollections if collection.getName == 'tone'), None)
                        possibleRhythms = [x for x in self.__rhythmPatterns if x.getRhythmType == 'tone']
                        for j in range(setLength - 1):
                            if 'tone' == currentSetPattern[j].get('type'):
                                pitchPattern = tonePatternCollection.getPatterns[j]
                                # Get rhythms of the appropriate length
                                possibleRhythms = [x for x in possibleRhythms if
                                                   len(x.getRhythmPattern) == len(pitchPattern.getNotePattern)]
                                # rhythmPattern = possibleRhythms[0]
                                if 0 <= j < len(possibleRhythms):
                                    rhythmPattern = possibleRhythms[j]
                                else:
                                    rhythmPattern = possibleRhythms[0]

                                exercise = Exercise(pitchPattern, rhythmPattern, currentSetPattern[j].get('key'), currentSetPattern[j].get('mode'))
                                newSet[j] = exercise
                    else:
                        pitches = next(x for x in self.__notePatternCollections if x.getName == currentSetPattern[i].get('type'))
                        rhythmTypes = [x for x in self.__rhythmPatterns if x.getRhythmType == 'general']
                        c = 0
                        for k in range(len(newSet)):
                            if newSet[k] is None:
                                rhythms = [x for x in rhythmTypes if
                                                   x.noteLength == len(pitches.getPatterns[c].getNotePattern)]
                                newSet[k] = Exercise(pitches.getPatterns[c], rhythms[c], currentSetPattern[k].get('key'), currentSetPattern[k].get('mode'))
                                c += 1
        # Create a set for an existing player
        else:
            #  Review lessons have a notePattern from the history with a new or random rhythm.
            #   Non-review exercises have a new notePattern with a rhythm from history.
            previousSet = self.__player.getPreviousSet
            history = self.__player.exerciseHistory

            for i in range(len(currentSetPattern)):
                e = currentSetPattern[i]
                if e.get('reviewBool'):
                #     Review exercise = pitch from same type in history.min + rhythm from same type w/ new rhythm or random rhythm
                    notePatternOptions = []
                    for playerExercise in history.values():
                        if playerExercise.get('exercise').getPitchPattern.getRhythmMatcher == previousSet[i].getPitchPattern.getRhythmMatcher:
                            notePatternOptions.append(playerExercise)

                    m = min(notePatternOptions, key = lambda x:x.get('playCount')).get('playCount')
                    toneReviewPitches = [x for x in notePatternOptions if x.get('playCount') == m]

                    if len(toneReviewPitches) > 0:
                        pitches = toneReviewPitches[random.randint(0, len(toneReviewPitches)-1)].get('exercise').getPitchPattern
                    else:
                        pitches = toneReviewPitches[0].getPitchPattern
                    # if e.get('type') == 'tone':
                        # Get the list of tone rhythms. Choose from matching new rhythms
                    possibleRhythms = [x for x in self.__rhythmPatterns if x.getRhythmType == previousSet[i].getPitchPattern.getRhythmMatcher]
                    rhythm = None
                    for rpat in possibleRhythms:
                        if rhythm is None:
                            for hisPattern in history.values():
                                if rpat.getRhythmPattern == hisPattern.get('exercise').getRhythmPattern.getRhythmPattern:
                                    break
                                if rpat.noteLength == len(pitches.getNotePattern):
                                    rhythm = rpat

                    if rhythm == None:
                        rhythm = possibleRhythms[random.randint(0, len(possibleRhythms))]
                    ex = Exercise(pitches, rhythm)
                    newSet[i] = (ex)
                else:
                    # Get the next note Pattern for the collection type
                    type = currentSetPattern[i].get('type')
                    c = next(x for x in self.__notePatternCollections if x.getName == type)
                    d = self.__player.getCollectionIndices[type]['currentIndex']
                    pitches = c.getPatterns[d + 1]
                    if d >= len(c.getPatterns):
                        self.__player.getCollectionIndices[type]['currentIndex'] = 0
                    else:
                        self.__player.getCollectionIndices[type]['currentIndex'] += 1

                    # Get a review rhythm pattern for the collection type.
                    possibleRhythms = []
                    for ex in history.values():
                        if ex.get('exercise').getRhythmPattern.getRhythmType == pitches.getRhythmMatcher:
                            possibleRhythms.append(ex)
                    m = min(possibleRhythms, key = lambda x:x.get('playCount')).get('playCount')
                    rhythms = []
                    for r in possibleRhythms:
                        if r.get('playCount') == m and r.get('exercise').getRhythmPattern.noteLength == len(pitches.getNotePattern):
                            rhythms.append(r)
                    rhythm = rhythms[random.randint(0, len(rhythms)-1)]
                    ex = Exercise(pitches, rhythm.get('exercise').getRhythmPattern)
                    newSet[i] = ex

        return newSet
