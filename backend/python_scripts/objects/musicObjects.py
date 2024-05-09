# import abjad
#
# class Scale:
#     def __init__(self, tonic, mode):
#         self.__tonic = tonic
#         self.__mode = mode
#
#     def getPitches(self):
#         pitchSets = {
#             "major": [0, 2, 4, 5, 7, 9, 11],
#             "natural_minor": [0, 2, 3, 5, 7, 8, 10],
#             "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
#             "jazz_minor": [0, 2, 3, 5, 7, 9, 11],
#         }
#         return pitchSets
#
#     def makeScale(self):
#         pitches = []
#         tonic = abjad.NamedPitch(self.__tonic)
#         for scalePitch in self.getPitches()[self.__mode]:
#             pitch = tonic + scalePitch
#             pitches.append(pitch)
#         return pitches