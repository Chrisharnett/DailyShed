import random
from objects.exerciseObjects import Exercise, NotePattern, RhythmPattern
import math

class PracticeSet:
    def __init__(self, player, notePatternCollections, rhythmPatterns):
        self.__player = player
        self.__notePatternCollections = notePatternCollections
        self.__rhythmPatterns = rhythmPatterns

    def minPlayCount(self, type):
        if len(self.__player.exerciseHistory) == 0:
            return None
        return min(self.__player.exerciseHistory, key=lambda x: x.getPlayCount).getPlayCount
    def chooseDirection(self, notePattern):
        directions = ['ascending', 'descending', 'ascending descending', 'descending ascending']
        uniqueDirections = set()
        reviewedDirections = [x['exercise'].getPitchPattern.getDirection for x in self.__player.exerciseHistory.values() if
                              x['exercise'].getPitchPattern == notePattern]
        index = len(reviewedDirections)-1
        if 0 < index < 4:
            print(index)
            return directions[index]
        return directions[random.randint(0, len(directions)-1)]

    def descendingPattern(self, pattern):
        d = pattern.getNotePattern.copy()
        d.reverse()
        n = NotePattern(f"{pattern.getPatternId}d",
                           pattern.getNotePatternType,
                           d,
                           pattern.getRhythmMatcher,
                           f'from the {pattern.getNotePattern[-1]}',
                           direction='descending')
        print(f"Descending: {NotePattern}")
        return n

    def ascendingDescendingPattern(self, pattern):
        a = pattern.getNotePattern.copy()
        d = pattern.getNotePattern.copy()
        d.reverse()
        a.pop()
        a.extend(d)
        n = NotePattern(f"{pattern.getPatternId}ad",
                           pattern.getNotePatternType,
                           a,
                           pattern.getRhythmMatcher,
                           f'to the {pattern.getNotePattern[-1]}',
                           direction='ascending descending')
        print(f"Ascending/Descending: {NotePattern}")
        return n

    def descendingAscendingPattern(self, pattern):
        d = pattern.getNotePattern.copy()
        d.reverse()
        d.pop()
        d.extend(pattern.getNotePattern)
        n = NotePattern(f"{pattern.getPatternId}da",
                           pattern.getNotePatternType,
                           d,
                           pattern.getRhythmMatcher,
                           f'from the {pattern.getNotePattern[-1]}',
                           direction='descending ascending')
        print(f"Descending/Ascending: {NotePattern}")
        return n

    def maxRhythmNoteLength(self, rhythms):
        return (max(rhythms, key=lambda x: x.noteLength)).noteLength

    def multipleBarRhythm(self, rhythms, length):
        # be aware of last note
        # Get the minimum number of bars using % ()
        maxRhythmLength = self.maxRhythmNoteLength(rhythms)
        minimumNumberOfMeasures = math.ceil(length/maxRhythmLength)
        measureNumber = 0
        remainder = length
        r = []
        id = ""
        while remainder > maxRhythmLength:
            # Get the rhythms that are at least length/minNumberOfMesures
            possibleRhythms = [x for x in rhythms if length/minimumNumberOfMeasures <= x.noteLength]
            if len(possibleRhythms) > 1:
                measure = possibleRhythms[random.randint(0, len(possibleRhythms) - 1)]
            else:
                measure = possibleRhythms[0]
            r.extend(measure.getRhythmPattern)
            id += measure.getRhythmPatternId
            remainder -= measure.noteLength
        possibleRhythms = [x for x in rhythms if x.noteLength == remainder]
        lastMeasure = possibleRhythms[random.randint(0, len(possibleRhythms)-1)]
        r.extend(lastMeasure.getRhythmPattern)
        id += lastMeasure.getRhythmPatternId
        rhythmPattern = RhythmPattern(id,
                                      lastMeasure.getRhythmType,
                                      lastMeasure.getRhythmDescription,
                                      r,
                                      lastMeasure.getTimeSignature,
                                      lastMeasure.getArticulation)
        return rhythmPattern

    def getNoteReviewPattern(self, type):
        notePatternOptions = []
        for playerExercise in self.__player.exerciseHistory.values():
            if playerExercise.get('exercise').getPitchPattern.getRhythmMatcher == type:
                notePatternOptions.append(playerExercise)
        minPlays = min(notePatternOptions, key=lambda x: x.get('playCount')).get('playCount')

        reviewPatterns = [playerExercise['exercise'].getPitchPattern for playerExercise in
                          self.__player.exerciseHistory.values() if playerExercise['playCount'] == minPlays and
                          playerExercise.get('exercise').getPitchPattern.getRhythmMatcher == type and
                          (isinstance(playerExercise.get('exercise').getPitchPattern.getPatternId, (int, str)) and
                          str(playerExercise.get('exercise').getPitchPattern.getPatternId).isdigit())]
        reviewPattern = reviewPatterns[random.randint(0, len(reviewPatterns)-1)]
        if reviewPattern.getNotePatternType != 'tone':
            direction = (self.chooseDirection(reviewPattern))
            if direction == 'descending':
                n = self.descendingPattern(reviewPattern)
                print(f"2: {n.getNotePattern} ")
                return n
            elif direction == 'ascending descending':
                n =  self.ascendingDescendingPattern(reviewPattern)
                print(f"2: {n.getNotePattern} ")
                return n
            elif direction == 'descending ascending':
                n =  self.descendingAscendingPattern(reviewPattern)
                print(f"2: {n.getNotePattern} ")
                return n
        else:
            print(f"Ascending: {reviewPattern.getNotePattern}")

        return reviewPattern


    def getRhythmReviewPattern(self, possibleRhythms, min, length):
        rhythms = []
        for rhythm in possibleRhythms:
            if rhythm.get('playCount') == min and rhythm.get('exercise').getRhythmPattern.noteLength == length:
                rhythms.append(rhythm['exercise'].getRhythmPattern)
        if len(rhythms) == 0:
            rhythms = [self.getNewRhythmPattern(possibleRhythms[0]['exercise'].getPitchPattern.getRhythmMatcher, length)]
        return rhythms[random.randint(0, len(rhythms) - 1)]

    def getNewNotePattern(self, type):

        notePatternCollection = next(x for x in self.__notePatternCollections if x.getName == type)
        currentPlayerIndex = self.__player.getCollectionIndices[type]['currentIndex']

        pitches = notePatternCollection.getPatterns[(currentPlayerIndex + 1) % len(notePatternCollection.getPatterns)]

        if currentPlayerIndex >= len(notePatternCollection.getPatterns):
            self.__player.getCollectionIndices[type]['currentIndex'] = -1
        else:
            self.__player.getCollectionIndices[type]['currentIndex'] += 1

        return pitches

    def getNewRhythmPattern(self, type, length):
        rhythmsThatFit = [x for x in self.__rhythmPatterns.getPatterns if
                    x.getRhythmType == type]
        max = self.maxRhythmNoteLength(rhythmsThatFit)
        if max >= length:
            return next(x for x in rhythmsThatFit if
                        x.noteLength == length)
        return self.multipleBarRhythm(rhythmsThatFit, length)

    def getNextSet(self):
        currentSetPattern = self.__player.getSetPattern
        newSet = []
        # set the length of the new set with None values
        for n in range(len(currentSetPattern)):
            newSet.append(None)

            #  Review lessons have a notePattern from the history with a new or random rhythm.
            #  Non-review exercises have a new notePattern with a rhythm from history.
        previousSet = self.__player.getPreviousSet

        for i in range(len(newSet)):
            # Build review exercise
            if currentSetPattern[i].get('reviewBool') and len(previousSet) > 0:

                pitches = self.getNoteReviewPattern(previousSet[i].getPitchPattern.getRhythmMatcher)
                rhythm = self.getNewRhythmPattern(previousSet[i].getPitchPattern.getRhythmMatcher, len(pitches.getNotePattern))

                ex = Exercise(pitches, rhythm)
                newSet[i] = (ex)
            else:
                # Get the next note Pattern for the collection type
                pitches = self.getNewNotePattern(currentSetPattern[i].get('type'))

                if len(previousSet) > 0:
                # Get a review rhythm pattern for the collection type.
                    possibleRhythms = []
                    for ex in self.__player.exerciseHistory.values():
                        if ex.get('exercise').getRhythmPattern.getRhythmType == pitches.getRhythmMatcher:
                            possibleRhythms.append(ex)
                    m = min(possibleRhythms, key=lambda x: x.get('playCount')).get('playCount')
                    rhythmReview = self.getRhythmReviewPattern(possibleRhythms, m, len(pitches.getNotePattern))
                    rhythm = rhythmReview
                else:
                    rhythm = next(pattern for pattern in self.__rhythmPatterns.getPatterns if
                                        pattern.getRhythmType == pitches.getRhythmMatcher and
                                        pattern.noteLength == len(pitches.getNotePattern))

                ex = Exercise(pitches, rhythm)
                newSet[i] = ex

        return newSet
