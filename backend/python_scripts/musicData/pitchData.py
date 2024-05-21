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
    return [
        # Major Scales
        ('c', 'major'), ('g', 'major'), ('d', 'major'), ('a', 'major'),
        ('e', 'major'), ('b', 'major'), ('fs', 'major'), ('cs', 'major'),

        # Harmonic Minor Scales
        ('a', 'harmonic minor'), ('e', 'harmonic minor'), ('b', 'harmonic minor'),
        ('fs', 'harmonic minor'), ('cs', 'harmonic minor'), ('gs', 'harmonic minor'),
        ('ds', 'harmonic minor'), ('as', 'harmonic minor'),

        # Melodic Minor Scales
        ('a', 'melodic minor'), ('e', 'melodic minor'), ('b', 'melodic minor'),
        ('fs', 'melodic minor'), ('cs', 'melodic minor'), ('gs', 'melodic minor'),
        ('ds', 'melodic minor'), ('as', 'melodic minor'),

        # Jazz Minor Scales
        ('a', 'jazz minor'), ('e', 'jazz minor'), ('b', 'jazz minor'),
        ('fs', 'jazz minor'), ('cs', 'jazz minor'), ('gs', 'jazz minor'),
        ('ds', 'jazz minor'), ('as', 'jazz minor'),

        # Altered Scales
        ('c', 'altered'), ('g', 'altered'), ('d', 'altered'), ('a', 'altered'),
        ('e', 'altered'), ('b', 'altered'), ('fs', 'altered'), ('cs', 'altered'),

        # Church Modes
        ('c', 'ionian'), ('g', 'ionian'), ('d', 'ionian'), ('a', 'ionian'),
        ('e', 'ionian'), ('b', 'ionian'), ('fs', 'ionian'), ('cs', 'ionian'),

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

        # Klezmer Scales
        ('c', 'klezmer'), ('g', 'klezmer'), ('d', 'klezmer'), ('a', 'klezmer'),
        ('e', 'klezmer'), ('b', 'klezmer'), ('fs', 'klezmer'), ('cs', 'klezmer'),

        ('c', 'freygish'), ('g', 'freygish'), ('d', 'freygish'), ('a', 'freygish'),
        ('e', 'freygish'), ('b', 'freygish'), ('fs', 'freygish'), ('cs', 'freygish'),

        # Balkan Scales
        ('c', 'gypsy_major'), ('g', 'gypsy_major'), ('d', 'gypsy_major'), ('a', 'gypsy_major'),
        ('e', 'gypsy_major'), ('b', 'gypsy_major'), ('fs', 'gypsy_major'), ('cs', 'gypsy_major'),

        ('c', 'gypsy_minor'), ('g', 'gypsy_minor'), ('d', 'gypsy_minor'), ('a', 'gypsy_minor'),
        ('e', 'gypsy_minor'), ('b', 'gypsy_minor'), ('fs', 'gypsy_minor'), ('cs', 'gypsy_minor'),

        # Indian Scales (Ragas)
        ('c', 'bhairav'), ('g', 'bhairav'), ('d', 'bhairav'), ('a', 'bhairav'),
        ('e', 'bhairav'), ('b', 'bhairav'), ('fs', 'bhairav'), ('cs', 'bhairav'),

        ('c', 'ahir_bhairav'), ('g', 'ahir_bhairav'), ('d', 'ahir_bhairav'), ('a', 'ahir_bhairav'),
        ('e', 'ahir_bhairav'), ('b', 'ahir_bhairav'), ('fs', 'ahir_bhairav'), ('cs', 'ahir_bhairav'),

        ('c', 'kafi'), ('g', 'kafi'), ('d', 'kafi'), ('a', 'kafi'),
        ('e', 'kafi'), ('b', 'kafi'), ('fs', 'kafi'), ('cs', 'kafi'),

        ('c', 'khamaj'), ('g', 'khamaj'), ('d', 'khamaj'), ('a', 'khamaj'),
        ('e', 'khamaj'), ('b', 'khamaj'), ('fs', 'khamaj'), ('cs', 'khamaj'),

        ('c', 'marwa'), ('g', 'marwa'), ('d', 'marwa'), ('a', 'marwa'),
        ('e', 'marwa'), ('b', 'marwa'), ('fs', 'marwa'), ('cs', 'marwa'),

        ('c', 'yaman'), ('g', 'yaman'), ('d', 'yaman'), ('a', 'yaman'),
        ('e', 'yaman'), ('b', 'yaman'), ('fs', 'yaman'), ('cs', 'yaman'),

        ('c', 'todi'), ('g', 'todi'), ('d', 'todi'), ('a', 'todi'),
        ('e', 'todi'), ('b', 'todi'), ('fs', 'todi'), ('cs', 'todi')
    ]

