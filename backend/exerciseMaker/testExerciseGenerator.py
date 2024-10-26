from musicData.instruments import instrumentList
from objects.Instrument import Instrument
from objects.Scale import Scale
from objects.ScaleExercise import ScaleExercise
from exerciseCollections.rhythmPatternCollections import eighthAndQuarterRhythms, quarterNoteAndRestRhythms

def createScaleExerciseImage(scale, range, instrument, level, rhythms):
    scaleExercise = ScaleExercise(scale)
    scaleExercise.getRandomRhythmPattern(rhythms)
    scaleExercise.description = f"{scale.tonic.title()} {scale.mode.title()} {range.title()} Scale for {instrument.instrumentName} {instrument.level}"
    scaleExercise.filename = f"[{level}_{instrument.instrumentName}_{scale.tonic}_{scale.mode.replace(' ', '_')}_{range.replace(' ', '_')}"
    scaleExercise.createTestImage()

def createScale(instrument, level, tonic, mode, range, rhythms):
    details = next(i for i in instrumentList() if i.get('instrumentName') == instrument)
    lowNote = details.get('lowNote').get(level)
    highNote = details.get('highNote').get(level)
    instrument = Instrument(details.get('instrumentName'), level, lowNote, highNote, details.get('defaultTonic'))
    scale = Scale(tonic=tonic, mode=mode, lowNote=instrument.lowNote, highNote=instrument.highNote)

    match range:
        case 'full range':
            scale.fullRangeAscendingScale()
        case 'one octave':
            scale.oneOctaveAscendingDescendingScale()
        case 'two octave':
            scale.twoOctaveAscendingDescendingScale()
    createScaleExerciseImage(scale, range, instrument, level, rhythms=rhythms)


def main():
    # tonicSequence = getTonicSequenceByName('circle of fifths')
    # instruments = ['saxophone', 'clarinet']
    # levels = ['beginner', 'advanced']
    # tonics = ['c', 'g']
    # modes = ['major', 'jazz_minor', 'altered', 'whole_tone']
    # ranges = ['one octave', 'two octave', 'full range']
    instruments = ['saxophone']
    levels = ['advanced']
    tonics = ['g', 'a']
    modes = ['melodic_minor']
    ranges = ['one octave']

    # rhythms, collectionLength = quarterNoteAndRestRhythms(int(4), '4')
    rhythms, collectionLength = eighthAndQuarterRhythms(int(4), '4')

    for instrument in instruments:
        for level in levels:
            for tonic in tonics:
                for mode in modes:
                    for range in ranges:
                        createScale(instrument, level, tonic, mode, range, rhythms)


if __name__ == '__main__':
    main()