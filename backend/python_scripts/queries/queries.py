from util.getDBConnection import getDBConnection
import json
from flask import jsonify
from musicData.instruments import instrumentList
from musicData.tonicSequences import tonicSequenceList
from musicData.modes import modeList
from util.imageURL import imageURL

def fetchUserExerciseLog(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT userName, lastPlay, playHistory, averageRating, playCount, exerciseName, imageFilename FROM get_user_history WHERE sub = %s"
            cursor.execute(query, (sub,))
            result = cursor.fetchall()
        history = {'userName': result[0].get('userName'),
                   'exerciseHistory': []}
        for exercise in result:
            playHistoryRaw = exercise.get('playHistory').split('| ')
            playHistory = []
            for play in playHistoryRaw:
                details = play.split('-', 1)
                if len(details) == 2:
                    playHistory.append({'date': details[0], 'comment': '', 'rating': details[1][1:]})
                else:
                    playHistory.append({'date': details[0], 'comment': details[1], 'rating': details[2]})
            history.get('exerciseHistory').append({
                'exerciseName': exercise.get('exerciseName'),
                'playCount': exercise.get('playCount'),
                'lastPlay': exercise.get('lastPlay'),
                'playHistory': playHistory,
                'averageRating': exercise.get('averageRating'),
                'imageFilename': imageURL(exercise.get('imageFilename')),
            })
        return history

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def fetchRhythmPatternOptions(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_rhythmPattern_options', [sub])
            options = []
            while True:
                result = cursor.fetchall()
                for rhythm in result:
                    options.append({
                        'programID': rhythm.get('programID'),
                        'programTitle': rhythm.get('programTitle'),
                        'primaryCollectionID': rhythm.get('primaryCollectionID'),
                        'rhythmCollection': rhythm.get('rhythmCollection')
                    })
                if not cursor.nextset():
                    break

            conn.commit()
            return options if options else None

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def fetchModes():
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            modes = []
            query = "SELECT scaleModeName FROM scaleModes"
            cursor.execute(query, )
            result = cursor.fetchall()
            for mode in result:
                modes.append(mode.get('scaleModeName').replace('_', ' ').title())
        return modes

    except Exception as e:
        return str(e)

    finally:
        conn.close()

def getNotePatternHistory(sub, collectionID):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_notePattern_history_proc', [sub, collectionID])
            result = cursor.fetchall()
            history = []
            for np in result:
                history.append({
                    'notePatternID': np.get('notePatternID'),
                    'playcount': np.get('playcount'),
                    'direction': json.loads(np.get('directions'))[np.get('directionIndex')],
                    'directionIndex': np.get('directionIndex')
                })
            conn.commit()
            return history if history else None

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def incrementProgramIndex(userProgramID):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('increment_program_index_proc', [userProgramID])
            result = cursor.fetchone()
            conn.commit()
            return result['currentIndex'] if result else None

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False

    finally:
        conn.close()

def logExerciseDetails(exerciseDetails):
    # FIXME: Add an increment boolean here. If true, increment the user index. Increment should stay within overall length of program.
    conn = getDBConnection()
    sessionID = exerciseDetails.get('sessionID')
    timestamp = exerciseDetails.get('timestamp')
    sub = exerciseDetails.get('sub')
    exerciseID = exerciseDetails.get('exerciseID')
    rating = exerciseDetails.get('rating')
    comment = exerciseDetails.get('comment')
    incrementMe = exerciseDetails.get('incrementMe') or None
    try:
        cursor = conn.cursor()
        cursor.callproc(
            'log_exercise_proc',
            [
                sessionID,
                timestamp,
                sub,
                exerciseID,
                rating,
                comment,
                incrementMe
            ])
        conn.commit()
        exerciseDetails['incrementMe'] = False
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

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
            tonicSequence = json.loads(exercise.get('tonicSequence'))
            session.get('intervals').append({
                'primaryCollectionTitle': exercise.get('PrimaryCollectionTitle'),
                'rhythmCollectionTitle': exercise.get('rhythmCollectionTitle'),
                'tonicSequence': tonicSequence,
                'tonic': tonicSequence[exercise.get('scaleTonicIndex')],
                'mode': exercise.get('mode'),
                'reviewExercise': exercise.get('reviewExercise'),
                'currentIndex': exercise.get('currentIndex'),
                'userProgramID': exercise.get('userProgramID'),
                'primaryCollectionType': exercise.get('PrimaryCollectionType'),
                'rhythmCollectionID': exercise.get('rhythmCollectionID'),
                'primaryCollectionID': exercise.get('primaryCollectionID'),
                'collectionLength': exercise.get('collectionLength')
            })
        return session

    except Exception as e:
        return str(e), 500

    finally:
        conn.close()

def fetchUserPrograms(sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM get_user_programs WHERE sub = %s"
            cursor.execute(query, (sub, ))
            result = cursor.fetchall()
        programs = {'userName': result[0].get('userName'),
                    'programs': []}
        for interval in result:
            program = {
                        'programTitle': interval.get('collectionTitle'),
                        'collectionType': interval.get('collectionType'),
                        'collectionLength': interval.get('collectionLength'),
                        'instrument': interval.get('instrumentName'),
                        'tonicSequence': json.loads(interval.get('sequence')),
                        'tonicSequenceName': interval.get('tonicSequenceName'),
                        'scaleTonicIndex': interval.get('scaleTonicIndex'),
                        'mode': interval.get('scaleModeName'),
                        'currentIndex': interval.get('currentIndex'),
                        'rhythmCollection': interval.get('rhythmCollection')
                        }
            programs['programs'].append(program)
        return programs

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
                cursor.callproc('add_program_proc', [primary, rhythm, None, None])
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

def insertNewRhythmPattern(
        collectionID,
        rhythmDescription,
        articulation,
        timeSignature,
        rhythmPattern,
        rhythmLength,
        subRhythms
):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('insert_new_rhythmPattern_proc',
                            [
                                collectionID,
                                rhythmDescription,
                                json.dumps(articulation),
                                json.dumps(timeSignature),
                                json.dumps(rhythmPattern),
                                rhythmLength,
                                json.dumps(subRhythms)
                            ])
            result = cursor.fetchone()
            return result.get('rhythmPatternID')
        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        conn.close()
