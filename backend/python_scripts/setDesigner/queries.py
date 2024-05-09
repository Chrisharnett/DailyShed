from util.getDBConnection import getDBConnection
import json
from flask import jsonify
from data.instruments import instrumentList
from data.tonicSequences import tonicSequenceList
from data.modes import modeList

def getCollections(session):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            collections = []
            collectionsCollected = set()
            for interval in session.get('intervals'):
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

def startUserPracticeSession(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('start_practice_session', [sub])
            result = cursor.fetchone()
            conn.commit()
            return result['userPracticeSessionID'] if result else None

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def getPracticeSession(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM get_practice_session WHERE sub = %s"
            cursor.execute(query, (sub, ))
            result = cursor.fetchall()
        session = {'sub': result[0].get('sub'),
                   'userName': result[0].get('userName'),
                   'rounds': result[0].get('rounds'),
                   'setLength': result[0].get('setLength'),
                   'intervals': []}
        for exercise in result:
            session.get('intervals').append({
                'PrimaryCollectionTitle': exercise.get('PrimaryCollectionTitle'),
                'rhythmCollectionTitle': exercise.get('rhythmCollectionTitle'),
                'tonic': exercise.get('tonic'),
                'mode': exercise.get('mode'),
                'reviewExercise': exercise.get('reviewExercise'),
                'currentIndex': exercise.get('currentIndex'),
                'userProgramID': exercise.get('userProgramID'),
                'collectionLength': exercise.get('collectionLength'),
                'primaryCollectionType': exercise.get('PrimaryCollectinType'),
                'rhythmCollectionID': exercise.get('rhythmCollectionID'),
                'primaryCollectionID': exercise.get('primaryCollectionID')
            })
        return session

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
            cursor.execute(query, [
                notePatternID,
                rhythmPatternID,
                tonic,
                mode,
                directionIndex
            ])
            exercise = cursor.fetchone()
            return exercise
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()

def addNewExercise(notePatternID, rhythmPatternID, tonic, mode, direction, directionIndex, userProgramID, userPracticeSessionID):
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
                userProgramID,
                userPracticeSessionID])
            exercise = cursor.fetchone()
            conn.commit()
            return exercise if exercise else None

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def addTheBasics():
    conn = getDBConnection()
    instruments = instrumentList()
    tonicSequences = tonicSequenceList()
    modes =  modeList()
    try:
        cursor = conn.cursor()
        query = "INSERT IGNORE INTO Instruments (" \
                "instrumentName, " \
                "beginnerLowNote, " \
                "intermediateLowNote, " \
                "advancedLowNote, " \
                "beginnerHighNote, " \
                "intermediateHighNote, " \
                "advancedHighNote, " \
                "defaultTonic" \
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        for instrument in instruments:
            cursor.execute(query, (
                instrument['instrumentName'],
                instrument['beginnerLowNote'],
                instrument['intermediateLowNote'],
                instrument['advancedLowNote'],
                instrument['beginnerHighNote'],
                instrument['intermediateHighNote'],
                instrument['advancedHighNote'],
                instrument['defaultTonic']
            ))

        query = "INSERT IGNORE INTO TonicSequences (name, sequence) VALUES (%s, %s)"
        for sequence in tonicSequences:
            cursor.execute(query, (
                sequence['name'],
                json.dumps(sequence['sequence'])
            ))

        query = "INSERT IGNORE INTO scaleModes (scaleModeName, scaleModePattern) VALUES (%s, %s)"
        for mode in modes:
            cursor.execute(query, (
                mode['modeName'],
                json.dumps(mode['modePattern'])
            ))

        conn.commit()
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
    addTheBasics()
    try:
        with conn.cursor() as cursor:
            for program in programs:
                primary = program['primaryCollectionTitle']
                rhythm = program['rhythmPatternTitle']
                instrument = 'saxophone'
                cursor.callproc('add_program_proc', [primary, rhythm, instrument, None, None])
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

