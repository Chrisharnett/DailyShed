# from objects.exerciseObjects import NotePattern
#
# preamble = r"""#(set-global-staff-size 14)
#         """
#
#
# def singleNoteLongToneWholeNotes(minNote, maxNote, maxLength, collectionTitle="", rhythm="long_tone"):
#     PATTERN_ID = 0
#     toneExercises = []
#
#     # One note options
#     for i in range(minNote, maxNote):
#         notes = [i]
#         toneExercises.append(
#             NotePattern(
#                 notePatternId=str(PATTERN_ID),
#                 notePatternType="single_note_long_tone_",
#                 collectionTitle=collectionTitle,
#                 notePattern=notes,
#                 rhythmMatcher=rhythm,
#                 description=f"Scale note {i}. Play for one full breath. Strive full a full, steady, in tune sound. Repeat until you play 2 good notes.",
#                 direction="static",
#                 repeatMe=False,
#                 holdLastNote=False,
#             )
#         )
#         PATTERN_ID += 1
#
#     return toneExercises
#
#
# # All ascending scalar patterns
# def stepwiseScaleNotePatterns(minNote, maxNote, maxLength, collectionTitle="", rhythm="quarter_note"):
#     PATTERN_ID = 0
#     scale1Ascending = []
#     scale1 = []
#
#     # Ascending scalar options
#     for i in range(minNote + 1, maxNote + 1):
#         notes = []
#         for j in range(1, i + 1):
#             notes.append(j)
#         if notes:
#             scale1Ascending.append(notes)
#             scale1.append(
#                 NotePattern(
#                     notePatternId=str(PATTERN_ID),
#                     notePatternType="stepwise_scale",
#                     collectionTitle=collectionTitle,
#                     notePattern=notes,
#                     rhythmMatcher=rhythm,
#                     description=f"Play twice. Repeat both times.",
#                     direction="ascending",
#                 )
#             )
#             PATTERN_ID += 1
#
#     return scale1
#
#
# def main():
#     minNote = 1
#     maxNote = 9
#     maxLength = 2 * (maxNote)
#     collections = {}
#
#     stepwiseNotePatterns = stepwiseScaleNotePatterns(minNote, maxNote, maxLength, "Scale to the 9", "quarter_note")
#     singleNoteScalerLongTonePatterns = singleNoteLongToneWholeNotes(minNote, maxNote, maxLength, "Single Note Long Tones", "long_tone")
#
#     collections['Scale to the Ninth'] = stepwiseNotePatterns.serialize()
#     collections['Single Note Diatonic Long Tones'] = singleNoteScalerLongTonePatterns.serialize()
#
#     for collection in collections:
#         print(collection)
#
#
# if __name__ == "__main__":
#     main()
