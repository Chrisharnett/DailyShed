from exerciseCollections.notePatternCollections import singleNoteLongToneWholeNotes, stepwiseScaleNotePatterns
from exerciseCollections.rhythmPatternCollections import singleNoteWholeToneRhythms, quarterNoteRhythms

def collectionCreator():
    collections = []

    newPattern, collectionLength = stepwiseScaleNotePatterns(1, 9)

    collections.append({
        'collectionType': 'notePattern',
        'title': 'scale_to_the_ninth',
        'patterns': newPattern,
        'collectionLength': collectionLength
    })

    newPattern, collectionLength = singleNoteLongToneWholeNotes(1,9)
    collections.append({
        'collectionType': 'notePattern',
        'title': 'single_note_long_tone',
        'patterns': newPattern,
        'collectionLength': collectionLength
    })

    newPattern, collectionLength = singleNoteWholeToneRhythms(4, 4)
    collections.append({
        'collectionType': 'rhythm',
        'title': 'single_note_long_tone_rhythms',
        'patterns': newPattern,
        'collectionLength': collectionLength
    })

    newPattern, collectionLength = quarterNoteRhythms(4, 4)
    collections.append({
        'collectionType': 'rhythm',
        'title': 'quarter_note',
        'patterns': newPattern,
        'collectionLength': collectionLength
    })

    return collections

# def main():
#     with app.app_context():
#         collections = collectionCreator()
#         insertCollectionsInDatabase(collections)
#     # dynamodb = boto3.resource('dynamodb')
#     # table = dynamodb.Table('Daily_Shed_Collections')
#     #
#     # for collection in collections:
#     #     response = table.put_item(Item=collection)
#
# if __name__ == "__main__":
#     main()