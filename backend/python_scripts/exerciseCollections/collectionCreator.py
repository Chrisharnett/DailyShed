from notePatternCollections import singleNoteLongToneWholeNotes, stepwiseScaleNotePatterns
from rhythmPatternCollections import singleNoteWholeToneRhythms, quarterNoteRhythms
import boto3

def main():
    collections = []

    collections.append({
        'collectionType': 'notePattern',
        'title': 'scale_to_the_ninth',
        'patterns': stepwiseScaleNotePatterns(1, 9)
    })
    collections.append({
        'collectionType': 'notePattern',
        'title': 'single_note_long_tone',
        'patterns': singleNoteLongToneWholeNotes(1, 9)
    })
    collections.append({
        'collectionType': 'rhythm',
        'title': 'single_note_long_tone',
        'patterns': singleNoteWholeToneRhythms(4, 4)
    })
    collections.append({
        'collectionType': 'rhythm',
        'title': 'quarter_note',
        'patterns': quarterNoteRhythms(4, 4)
    })

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Daily_Shed_Collections')

    for collection in collections:
        response = table.put_item(Item=collection)
        print(response)

if __name__ == "__main__":
    main()