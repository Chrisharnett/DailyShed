from objects.Instrument import Instrument

def instrumentList():
    return [
            {
            'instrumentName': 'saxophone',
            'abbr': 'sax',
            'lowNote': {'beginner': 'd4',
                        'intermediate': 'bb3',
                        'advanced': 'bb3'},
            'highNote': {'beginner': 'c6',
                        'intermediate': 'f6',
                        'advanced': 'g6'},
            'defaultTonic': 'g4'
            }, {
            'instrumentName': 'clarinet',
            'abbr': 'clar',
            'lowNote': {'beginner': 'g3',
                        'intermediate': 'eb3',
                        'advanced': 'eb3'},
            'highNote': {'beginner': 'c5',
                         'intermediate': 'c6',
                         'advanced': 'c7'},
            'defaultTonic': 'c4'
            }
            ]


def getInstrumentsBySkillLevel(level):
    instruments = []
    for instrument in instrumentList():
        lowNote = instrument['lowNote'][level]
        highNote = instrument['highNote'][level]
        instruments.append(Instrument(instrument.get('instrumentName'), level, lowNote, highNote, instrument.get('defaultTonic'), instrument.get('abbr')))
    return instruments

def getAllInstruments():
    instruments = []
    for instrument in instrumentList():
        for level, lowNote in instrument.get('lowNote').items():
            highNote = instrument['highNote'][level]
            instruments.append(
                Instrument(instrument.get('instrumentName'), level, lowNote, highNote, instrument.get('defaultTonic'), instrument.get('abbr')))
    return instruments