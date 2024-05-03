# from notePatternGenerator import stepwiseScaleNotePatterns
# from rhythmPatternGenerator import quarterNoteRhythms
#
# preamble = r"""#(set-global-staff-size 14)
#         """
# def makeFirstSet(routinePattern, notePatternDictionary, rhythmPatternDictionary):
#     newSet = []
#     for i in range(len(routinePattern)):
#         if routinePattern[i] == 'longTone':
#             rhythms = list(filter(lambda x: x.get('rhythmType') == routinePattern[i], rhythmPatternDictionary))
#             for n in notePatternDictionary:
#                 for r in rhythms.get('rhythmPatterns'):
#                     if ((len(r.rhythmPattern) == len(n)) or (len(n) == len(r.rhythmPattern) - sum(1 for x in n if x == ['~']))):
#                         note = []
#                         for i in range(len(n)):
#                             note = [n[i], r[i]]
#                             print(note)
#             # newSet[i]
#     return newSet
#
# def main():
#     # TODO: Min note and max note for range. Attach to instruments
#     minNote = 1
#     maxNote = 9
#     maxLength = 2 * (maxNote)
#     routinePattern = ['longTone', 'longTone', 'scale', 'scale']
#     notePatternDictionary = stepwiseScaleNotePatterns(minNote, maxNote, maxLength)
#     rhythmPatternDictionary = quarterNoteRhythms(4, 4)
#     previousSet = []
#     # newSet = []
#     if len(previousSet) == 0:
#         newSet = makeFirstSet(routinePattern, notePatternDictionary, rhythmPatternDictionary)
#         print(newSet)
#
# if __name__ == '__main__':
#     main()
#
