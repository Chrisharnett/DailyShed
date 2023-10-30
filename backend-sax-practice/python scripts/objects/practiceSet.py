import random
from objects.exerciseObjects import Exercise

class PracticeSet:
    def __init__(self, player, notePatternCollections, rhythmPatterns):
        self.__player = player
        self.__notePatternCollections = notePatternCollections
        self.__rhythmPatterns = rhythmPatterns

    def minPlayCount(self, type):
        if len(self.__player.exerciseHistory) == 0:
            return None
        return min(self.__player.exerciseHistory, key=lambda x: x.getPlayCount).getPlayCount

    def getNoteReviewPatterns(self, min, type):
        reviewPatterns = [playerExercise.getExercise.getPitchPattern for playerExercise in self.__player.exerciseHistory
                          if
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

            #  Review lessons have a notePattern from the history with a new or random rhythm.
            #   Non-review exercises have a new notePattern with a rhythm from history.
            previousSet = self.__player.getPreviousSet
            history = self.__player.exerciseHistory

            for i in range(len(newSet)):
                e = currentSetPattern[i]

                # Build review exercise
                if e.get('reviewBool') and len(previousSet) > 0:
                    notePatternOptions = []
                    for playerExercise in history.values():
                        if playerExercise.get('exercise').getPitchPattern.getRhythmMatcher == previousSet[
                            i].getPitchPattern.getRhythmMatcher:
                            notePatternOptions.append(playerExercise)

                    m = min(notePatternOptions, key=lambda x: x.get('playCount')).get('playCount')
                    toneReviewPitches = [x for x in notePatternOptions if x.get('playCount') == m]

                    if len(toneReviewPitches) > 0:
                        pitches = toneReviewPitches[random.randint(0, len(toneReviewPitches) - 1)].get(
                            'exercise').getPitchPattern
                    else:
                        pitches = toneReviewPitches[0].getPitchPattern
                    # if e.get('type') == 'tone':
                    # Get the list of tone rhythms. Choose from matching new rhythms
                    possibleRhythms = [x for x in self.__rhythmPatterns if
                                       x.getRhythmType == previousSet[i].getPitchPattern.getRhythmMatcher]
                    rhythm = None
                    for rpat in possibleRhythms:
                        if rhythm is None:
                            for hisPattern in history.values():
                                if rpat.getRhythmPattern == hisPattern.get(
                                        'exercise').getRhythmPattern.getRhythmPattern:
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
                        self.__player.getCollectionIndices[type]['currentIndex'] = -1
                    else:
                        self.__player.getCollectionIndices[type]['currentIndex'] += 1

                    # Get a review rhythm pattern for the collection type.
                    possibleRhythms = []
                    for ex in history.values():
                        if ex.get('exercise').getRhythmPattern.getRhythmType == pitches.getRhythmMatcher:
                            possibleRhythms.append(ex)
                    m = min(possibleRhythms, key=lambda x: x.get('playCount')).get('playCount')
                    rhythms = []
                    for r in possibleRhythms:
                        if r.get('playCount') == m and r.get('exercise').getRhythmPattern.noteLength == len(
                                pitches.getNotePattern):
                            rhythms.append(r)
                    rhythm = rhythms[random.randint(0, len(rhythms) - 1)]
                    ex = Exercise(pitches, rhythm.get('exercise').getRhythmPattern)
                    newSet[i] = ex

        return newSet
