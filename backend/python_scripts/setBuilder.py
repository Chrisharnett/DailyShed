# from notePatternGenerator import stepwiseScaleNotePatterns
# from rhythmPatternGenerator import quarterNoteRhythms
# from objects.practiceSet import PracticeSet
# from objects.player import Player
# import random
#
#
# # build a set of setLength exercises from the setPattern.
# def main():
#     minNote = 1
#     maxNote = 9
#     maxLength = 2 * (maxNote)
#     currentSetPattern = [{"type": 'tone', "reviewBool": 1, "key": 'g', 'mode': 'major'},
#                       {"type": 'tone', "reviewBool": 0, "key": 'g', 'mode': 'major'},
#                       {"type": 'ninthScale1', "reviewBool": 1, "key": 'g', 'mode': 'major'},
#                       {"type": 'ninthScale1', "reviewBool": 0, "key": 'g', 'mode': 'major'}]
#
#     player = Player()
#     notes = stepwiseScaleNotePatterns(minNote, maxNote, maxLength)
#     rhythms = quarterNoteRhythms(4, 4)
#     keys = ['g', 'c', 'd']
#     practiceSet = PracticeSet(player, notes, rhythms)
#     sessions = 1
#     for i in range(sessions):
#         currentSet = practiceSet.getNextSet()
#         player.setPreviousSet(currentSet)
#         print(f"day {i}")
#         for exercise in currentSet:
#             player.addExercise(exercise, random.randint(0, 5))
#             url = exercise.createImage()
#             print(url)
#         print()
#         player.setPreviousSet(currentSet)
#
# if __name__ == '__main__':
#     main()