def getScaleDetails(tonic, mode):
    scales = modeList()
    for scale in scales:
        if scale['modeName'] == mode:
            scaleDetails = scale.copy()
            adjustments = scaleDetails.get('adjustments', {})
            scaleDetails['adjustments'] = adjustments.get(tonic, {})
            return scaleDetails
    return None

def modeList():
    return [
        {
            'modeName': 'major',
            'modePattern': [0, 2, 4, 5, 7, 9, 11],
            'diatonicTriads': [[0, 4, 7], [2, 5, 9], [4, 7, 11], [5, 9, 12], [7, 11, 14], [9, 12, 16], [11, 14, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'natural_minor',
            'modePattern': [0, 2, 3, 5, 7, 8, 10],
            'diatonicTriads': [[0, 3, 7], [2, 5, 8], [3, 7, 10], [5, 8, 12], [7, 10, 14], [8, 12, 15], [10, 14, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'harmonic_minor',
            'modePattern': [0, 2, 3, 5, 7, 8, 11],
            'diatonicTriads': [[0, 3, 7], [2, 5, 8], [3, 7, 11], [5, 8, 12], [7, 11, 14], [8, 12, 15], [11, 14, 17]],
            'adjustments': {
                'a': {'ab': 'gs'},
                'e': {'eb': 'ds'},
                'g': {'gb': 'fs'}
            }
        },
        {
            'modeName': 'melodic_minor',
            'modePattern': [0, 2, 3, 5, 7, 9, 11],
            'diatonicTriads': [[0, 3, 7], [2, 5, 9], [3, 7, 11], [5, 9, 12], [7, 11, 14], [9, 12, 16], [11, 14, 17]],
            'adjustments': {
                'a': {'ab': 'gs', 'gb': 'fs'},
                'g': {'gb': 'fs'}
            }
        },
        {
            'modeName': 'jazz_minor',
            'modePattern': [0, 2, 3, 5, 7, 9, 11],
            'diatonicTriads': [[0, 3, 7], [2, 5, 9], [3, 7, 11], [5, 9, 12], [7, 11, 14], [9, 12, 16], [11, 14, 17]],
            'adjustments': {
                'a': {'ab': 'gs', 'gb': 'fs'},
                'g': {'gb': 'fs'}
            }
        },
        {
            'modeName': 'altered',
            'modePattern': [0, 1, 3, 4, 6, 8, 10],
            'diatonicTriads': [[0, 3, 6], [1, 4, 8], [3, 6, 10], [4, 8, 11], [6, 10, 13], [8, 11, 14], [10, 13, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'chromatic',
            'modePattern': list(range(12)),
            'diatonicTriads': [],
            'adjustments': {}
        },
        {
            'modeName': 'diminished',
            'modePattern': [0, 2, 3, 5, 6, 8, 9, 11],
            'diatonicTriads': [[0, 3, 6], [2, 5, 8], [3, 6, 9], [5, 8, 11], [6, 9, 12], [8, 11, 14], [9, 12, 15], [11, 14, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'whole_tone',
            'modePattern': [0, 2, 4, 6, 8, 10],
            'diatonicTriads': [],
            'adjustments': {}
        },
        {
            'modeName': 'major_pentatonic',
            'modePattern': [0, 2, 4, 7, 9],
            'diatonicTriads': [[0, 4, 7], [2, 7, 9], [4, 7, 9], [7, 9, 11], [9, 11, 14]],
            'adjustments': {}
        },
        {
            'modeName': 'minor_pentatonic',
            'modePattern': [0, 3, 5, 7, 10],
            'diatonicTriads': [[0, 3, 7], [3, 7, 10], [5, 7, 10], [7, 10, 12], [10, 12, 15]],
            'adjustments': {}
        },
        {
            'modeName': 'bebop_major',
            'modePattern': [0, 2, 4, 5, 7, 8, 9, 11],
            'diatonicTriads': [[0, 4, 7], [2, 5, 9], [4, 7, 11], [5, 9, 12], [7, 11, 14], [8, 12, 16], [9, 14, 17],
                               [11, 14, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'bebop_minor',
            'modePattern': [0, 2, 3, 5, 7, 8, 10, 11],
            'diatonicTriads': [[0, 3, 7], [2, 5, 8], [3, 7, 10], [5, 8, 11], [7, 10, 14], [8, 11, 15], [10, 14, 17],
                               [11, 14, 17]],
            'adjustments': {}
        },
        {
            'modeName': 'bebop_dominant',
            'modePattern': [0, 2, 4, 5, 7, 9, 10, 11],
            'diatonicTriads': [[0, 4, 7], [2, 5, 9], [4, 7, 10], [5, 9, 11], [7, 10, 14], [9, 11, 16], [10, 14, 17],
                               [11, 14, 17]],
            'adjustments': {}
        },
        # {
        #     'modeName': 'dorian',
        #     'modePattern': [0, 2, 3, 5, 7, 9, 10],
        #     'diatonicTriads': [[0, 3, 7], [2, 5, 9], [3, 7, 10], [5, 9, 12], [7, 10, 14], [9, 12, 16], [10, 14, 17]],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'phrygian',
        #     'modePattern': [0, 1, 3, 5, 7, 8, 10],
        #     'diatonicTriads': [[0, 3, 7], [1, 5, 8], [3, 7, 10], [5, 8, 12], [7, 10, 14], [8, 12, 15], [10, 14, 17]],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'lydian',
        #     'modePattern': [0, 2, 4, 6, 7, 9, 11],
        #     'diatonicTriads': [[0, 4, 7], [2, 6, 9], [4, 7, 11], [6, 9, 12], [7, 11, 14], [9, 12, 16], [11, 14, 17]],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'mixolydian',
        #     'modePattern': [0, 2, 4, 5, 7, 9, 10],
        #     'diatonicTriads': [[0, 4, 7], [2, 5, 9], [4, 7, 10], [5, 9, 12], [7, 10, 14], [9, 12, 16], [10, 14, 17]],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'aeolian',
        #     'modePattern': [0, 2, 3, 5, 7, 8, 10],
        #     'diatonicTriads': [[0, 3, 7], [2, 5, 8], [3, 7, 10], [5, 8, 12], [7, 10, 14], [8, 12, 15], [10, 14, 17]],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'locrian',
        #     'modePattern': [0, 1, 3, 5, 6, 8, 10],
        #     'diatonicTriads': [[0, 3, 6], [1, 5, 8], [3, 6, 10], [5, 8, 11], [6, 10, 13], [8, 11, 15], [10, 13, 17]],
        #     'adjustments': {}
        # },
        # # Klezmer Scales
        # {
        #     'modeName': 'klezmer',
        #     'modePattern': [0, 1, 4, 5, 7, 8, 10],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'freygish',
        #     'modePattern': [0, 1, 4, 5, 7, 8, 11],
        #     'adjustments': {}
        # },
        # # Balkan Scales
        # {
        #     'modeName': 'gypsy_major',
        #     'modePattern': [0, 1, 4, 5, 7, 8, 11],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'gypsy_minor',
        #     'modePattern': [0, 2, 3, 6, 7, 8, 11],
        #     'adjustments': {}
        # },
        # # Indian Scales (Ragas)
        # {
        #     'modeName': 'bhairav',
        #     'modePattern': [0, 1, 4, 5, 7, 8, 11],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'ahir_bhairav',
        #     'modePattern': [0, 1, 4, 6, 7, 9, 11],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'kafi',
        #     'modePattern': [0, 2, 3, 5, 7, 9, 10],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'khamaj',
        #     'modePattern': [0, 2, 4, 5, 7, 9, 10],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'marwa',
        #     'modePattern': [0, 1, 4, 6, 7, 9, 11],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'yaman',
        #     'modePattern': [0, 2, 4, 6, 7, 9, 11],
        #     'adjustments': {}
        # },
        # {
        #     'modeName': 'todi',
        #     'modePattern': [0, 1, 3, 6, 7, 8, 11],
        #     'adjustments': {}
        # }
    ]

