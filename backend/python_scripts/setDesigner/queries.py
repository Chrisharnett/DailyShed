from util.getDBConnection import getDBConnection
import json
from flask import jsonify

# def getIntervalDetails(notePatternID, rhythmPatternID, tonic, mode):
#     conn = getDBConnection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.callproc('get_interval_details_proc', [notePatternID, rhythmPatternID, tonic, mode])
#             exercise = cursor.fetchall()
#             return exercise
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         return  str(e)
#     finally:
#         conn.close()

def getCollections(session):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            collections = []
            collectionsCollected = set()
            for interval in session:
                primaryCollectionID = interval.get('primaryCollectionID')
                rhythmPatternCollectionID = interval.get('rhythmCollectionID')
                if primaryCollectionID not in collectionsCollected:
                    # =TODO: create view that will return this
                    query = "SELECT * FROM get_notePattern_collection  " \
                            "WHERE collectionID = %s"
                    cursor.execute(query, (primaryCollectionID))
                    result = cursor.fetchall()
                    patterns = []
                    for pattern in result:
                        patterns.append({
                            'notePatternID': pattern.get('notePatternID'),
                            'collectionNotePatternID': pattern.get('collectionNotePatternID'),
                            'noteLength': pattern.get('noteLength'),
                            'description': pattern.get('description'),
                            'directions': json.loads(pattern.get('directions')),
                            'holdLastNote': pattern.get('holdLastNote'),
                            'notePatternType': pattern.get('notePatternType'),
                            'repeatMe': pattern.get('repeatMe'),
                            'notePattern': json.loads(pattern.get('notePattern')),
                            'currentDirectionIndex': pattern.get('directionIndex'),
                            'programID': pattern.get('programID')
                        })

                    collections.append({
                        'collectionID': primaryCollectionID,
                        'patterns': patterns,
                        'currentIndex': interval.get('currentIndex')})
                    collectionsCollected.add(primaryCollectionID)
                if rhythmPatternCollectionID not in collectionsCollected:
                    # TODO: Create a view that will handle below.
                    query = "SELECT * FROM get_rhythmPattern_collection " \
                            "WHERE collectionID = %s"
                    cursor.execute(query, (rhythmPatternCollectionID))
                    result = cursor.fetchall()
                    patterns = []
                    for pattern in result:
                        patterns.append({
                            'rhythmPatternID': pattern.get('rhythmPatternID'),
                            'collectionRhythmPatternID': pattern.get('collectionRhythmPatternID'),
                            'rhythmLength': pattern.get('rhythmLength'),
                            'rhythmDescription': pattern.get('rhythmDescription'),
                            'articulation': json.loads(pattern.get('articulation')),
                            'timeSignature': json.loads(pattern.get('timeSignature')),
                            'rhythmPattern': json.loads(pattern.get('rhythmPattern'))
                        })
                    collections.append({
                        'collectionID': rhythmPatternCollectionID,
                        'patterns': patterns,
                        'currentIndex': interval.get('currentIndex')})
                    collectionsCollected.add(rhythmPatternCollectionID)
        return collections

    except Exception as e:
        return str(e)

    finally:
        conn.close()

def getUserHistory(sub):
    return None, 200

def getPreviousSet(sub):
    return None, 200

def getPracticeSession(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM get_practice_session WHERE sub = %s"
            cursor.execute(query, (sub, ))
            result = cursor.fetchall()
        return result

    except Exception as e:
        return str(e), 500

    finally:
        conn.close()

def fetchExercise(notePatternID, rhythmPatternID, tonic, mode, directionIndex):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * " \
                    "FROM view_exercises " \
                    "WHERE notePatternID = %s AND " \
                    "rhythmPatternID = %s AND " \
                    "tonic = %s AND " \
                    "mode = %s AND " \
                    "directionIndex = %s"
            cursor.execute(query, (
                notePatternID,
                rhythmPatternID,
                tonic,
                mode,
                directionIndex))
            exercise = cursor.fetchall()
            return exercise
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()

def addNewExercise(notePatternID, rhythmPatternID, tonic, mode, direction, directionIndex, programID):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:

            cursor.callproc('add_new_exercise_proc', [
                notePatternID,
                rhythmPatternID,
                tonic,
                mode,
                direction,
                directionIndex,
                programID])
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def insertTonicsAndModes():
    conn = getDBConnection()
    tonics = ['c', 'g', 'd', 'a', 'e', 'b', 'gb', 'db', 'ab', 'eb', 'bb', 'f']
    modes =  {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "natural_minor": [0, 2, 3, 5, 7, 8, 10],
            "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
            "jazz_minor": [0, 2, 3, 5, 7, 9, 11],
        }
    modeJSON = {key : json.dumps(value) for key, value in modes.items()}
    try:
        with conn.cursor() as cursor:
            with conn.cursor() as cursor:
                # Inserting modes using executemany for batch processing
                mode_data = [(mode, pattern) for mode, pattern in modeJSON.items()]
                cursor.executemany('INSERT INTO scaleModes (scaleModeName, scaleModePattern) VALUES (%s, %s)',
                                   mode_data)

                # Inserting tonics using executemany for batch processing
                tonic_data = [(tonic,) for tonic in tonics]  # note the comma to make it a tuple
                cursor.executemany('INSERT INTO pitchNames (pitchNames) VALUES (%s)', tonic_data)

        # FIXME: Commented out to prevent duplicating accidentally.
        # conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def insertPrograms(programs):
    conn = getDBConnection()
    #Being used now to create default starting programs for a give user on saxophone
    # insertTonicsAndModes()
    try:
        with conn.cursor() as cursor:
            for program in programs:
                primary = program['primaryCollectionTitle']
                rhythm = program['rhythmPatternTitle']
                cursor.callproc('add_program_proc', [primary, rhythm])
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

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

