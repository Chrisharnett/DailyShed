def sharpPitchSet():
    flats_to_sharps = {
        'db': 'cs',
        'eb': 'ds',
        'gb': 'fs',
        'ab': 'gs',
        'bb': 'as'
    }
    # Replace flats with sharps
    sharpPitchSet = []
    for pitch in flatPitchSet():
        for flat, sharp in flats_to_sharps.items():
            if flat in pitch:
                pitch = pitch.replace(flat, sharp)
        sharpPitchSet.append(pitch)
    return sharpPitchSet

def flatPitchSet():
    return [
        'c0', 'db0', 'd0', 'eb0', 'e0', 'f0', 'gb0', 'g0', 'ab0', 'a0', 'bb0', 'b0',
        'c1', 'db1', 'd1', 'eb1', 'e1', 'f1', 'gb1', 'g1', 'ab1', 'a1', 'bb1', 'b1',
        'c2', 'db2', 'd2', 'eb2', 'e2', 'f2', 'gb2', 'g2', 'ab2', 'a2', 'bb2', 'b2',
        'c3', 'db3', 'd3', 'eb3', 'e3', 'f3', 'gb3', 'g3', 'ab3', 'a3', 'bb3', 'b3',
        'c4', 'db4', 'd4', 'eb4', 'e4', 'f4', 'gb4', 'g4', 'ab4', 'a4', 'bb4', 'b4',
        'c5', 'db5', 'd5', 'eb5', 'e5', 'f5', 'gb5', 'g5', 'ab5', 'a5', 'bb5', 'b5',
        'c6', 'db6', 'd6', 'eb6', 'e6', 'f6', 'gb6', 'g6', 'ab6', 'a6', 'bb6', 'b6',
        'c7', 'db7', 'd7', 'eb7', 'e7', 'f7', 'gb7', 'g7', 'ab7', 'a7', 'bb7', 'b7',
        'c8'
    ]

def sharpModes():
    majorSharpKeys = ['c', 'g', 'd', 'a', 'e', 'b', 'fs', 'cs']
    majorModes = ['major', 'major_pentatonic', 'bebop_major', 'bebop_dominant', 'altered', 'ionian',
                  'klezmer', 'freygish', 'gypsy_major', 'gypsy_minor',
                  'bhairav', 'ahir_bhairav', 'kafi', 'khamaj', 'marwa', 'yaman', 'todi']
    minorSharpKeys = ['a', 'e', 'b', 'fs', 'cs', 'gs', 'ds', 'as']
    minorModes = ['harmonic minor', 'minor_pentatonic', 'bebop_minor', 'melodic_minor', 'jazz_minor']
    sharpDefaultModes =  [
        ('d', 'dorian'), ('a', 'dorian'), ('e', 'dorian'), ('b', 'dorian'),
        ('fs', 'dorian'), ('cs', 'dorian'), ('gs', 'dorian'), ('ds', 'dorian'),

        ('e', 'phrygian'), ('b', 'phrygian'), ('fs', 'phrygian'), ('cs', 'phrygian'),
        ('gs', 'phrygian'), ('ds', 'phrygian'), ('as', 'phrygian'), ('es', 'phrygian'),

        ('f', 'lydian'), ('c', 'lydian'), ('g', 'lydian'), ('d', 'lydian'),
        ('a', 'lydian'), ('e', 'lydian'), ('b', 'lydian'), ('fs', 'lydian'),

        ('g', 'mixolydian'), ('d', 'mixolydian'), ('a', 'mixolydian'), ('e', 'mixolydian'),
        ('b', 'mixolydian'), ('fs', 'mixolydian'), ('cs', 'mixolydian'), ('gs', 'mixolydian'),

        ('a', 'aeolian'), ('e', 'aeolian'), ('b', 'aeolian'), ('fs', 'aeolian'),
        ('cs', 'aeolian'), ('gs', 'aeolian'), ('ds', 'aeolian'), ('as', 'aeolian'),

        ('b', 'locrian'), ('fs', 'locrian'), ('cs', 'locrian'), ('gs', 'locrian'),
        ('ds', 'locrian'), ('as', 'locrian'), ('es', 'locrian'), ('bs', 'locrian'),
    ]
    for mode in majorModes:
        for key in majorSharpKeys:
            sharpDefaultModes.append((key, mode))
    for mode in minorModes:
        for key in minorSharpKeys:
            sharpDefaultModes.append((key, mode))
    return sharpDefaultModes

