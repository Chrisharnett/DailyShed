def scaleExercisePatterns():
    return [
            'full_range_ascending_scale',
            'one_octave_ascending_descending_scale',
            'two_octave_ascending_descending_scale'
            ]

def scalePatternPrograms():
    return [
        {
        'scalePatternType': 'scale_to_the_ninth_builder',
        'allKeys': False,
        'rhythmType': 'rhythm'
        }, {
        'scalePatternType': 'one_octave_scale',
        'allKeys': True,
        'rhythmType': 'rhythm'
        }, {
        'scalePatternType': 'two_octave_scale',
        'allKeys': True,
        'rhythmType': 'rhythm'
        }, {
        'scalePatternType': 'full_range_scale',
        'allKeys': True,
        'rhythmType': 'rhythm'
        }, {
        'scalePatternType': 'full_range_builder',
        'allKeys': True,
        'rhythmType': 'rhythm'
        }, {
        'scalePatternType': 'diatonic_one_note_long_tone',
        'allKeys': False,
        'rhythmType': 'long_tone_rhythm'
        }, {
        'scalePatternType': 'descending_long_tone',
        'allKeys': False,
        'rhythmType': 'long_tone_rhythm'
        }
    ]