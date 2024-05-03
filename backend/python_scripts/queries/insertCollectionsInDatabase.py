from util.getDBConnection import getDBConnection
import json
from flask import jsonify

def insertCollectionsInDatabase(collections):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            for collection in collections:
                collectionType = collection['collectionType']
                collectionTitle = collection['title']
                collectionLength = collection['collectionLength'] or 0
                # patterns = json.dumps(collection['patterns'])

                match collectionType:
                    case 'notePattern':
                        for pattern in collection['patterns']:
                            description = pattern['description']
                            direction = pattern['direction']
                            directions = json.dumps(pattern['directions'])
                            holdLastNote = pattern['holdLastNote']
                            notePattern = json.dumps(pattern['notePattern'])
                            notePatternType = pattern['notePatternType']
                            repeatMe = pattern['repeatMe']
                            collectionNotePatternID = pattern['notePatternId']
                            noteLength = pattern['noteLength']
                            cursor.callproc('insert_notePattern_proc',
                                [
                                    collectionTitle,
                                    collectionType,
                                    collectionLength,
                                    description,
                                    direction,
                                    directions,
                                    holdLastNote,
                                    notePattern,
                                    notePatternType,
                                    repeatMe,
                                    collectionNotePatternID,
                                    noteLength
                                ])
                    case 'rhythm':
                        for i, pattern in enumerate(collection['patterns']):
                            rhythmDescription = pattern['rhythmDescription']
                            articulation = json.dumps(pattern['articulation'])
                            timeSignature = json.dumps(pattern['timeSignature'])
                            rhythmPattern = json.dumps(pattern['rhythmPattern'])
                            collectionRhythmPatternID = pattern['rhythmPatternID']
                            rhythmLength = pattern['rhythmLength']

                            cursor.callproc('insert_rhythmPattern_proc',
                                [
                                    collectionTitle,
                                    collectionType,
                                    collectionLength,
                                    rhythmDescription,
                                    articulation,
                                    timeSignature,
                                    rhythmPattern,
                                    collectionRhythmPatternID,
                                    rhythmLength
                                ])
    
                conn.commit()
        return jsonify({"status": "success", "message": "Collection added successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        conn.close()

