def modeList():
    return [
            {
                'modeName': 'major',
                'modePattern': [0, 2, 4, 5, 7, 9, 11]
            }, {
            'modeName': "natural_minor",
                'modePattern': [0, 2, 3, 5, 7, 8, 10]
            }, {
                'modeName': "harmonic_minor",
                'modePattern': [0, 2, 3, 5, 7, 8, 11]
            }, {
                'modeName': "jazz_minor",
                'modePattern': [0, 2, 3, 5, 7, 9, 11]
            }
        ]