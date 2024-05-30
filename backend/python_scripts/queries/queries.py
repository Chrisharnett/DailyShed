from util.getDBConnection import getDBConnection
import json
from flask import jsonify
from musicData.instruments import getAllInstruments
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
                id = np.get('notePatternID')
                playcount = np.get('playcount')
                index = np.get('directionIndex')
                if index:
                    direction = json.loads(np.get('directions')[index])
                else:
                    direction = 'static'
                history.append({
                    'notePatternID': id,
                    'playcount': playcount,
                    'direction': direction,
                    'directionIndex': index
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
            for interval in session.intervals:
                primaryCollectionID = interval.primaryCollectionID
                rhythmPatternCollectionID = interval.rhythmCollectionID
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
                        'currentIndex': interval.currentIndex})
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
                        'currentIndex': interval.currentIndex})
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

def addDefaultPrograms(program1, program2, instrument, sub):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_default_program_proc', [program1, program2, instrument, sub])
            result = cursor.fetchall()
            conn.commit()
            return result
    except Exception as e:
        return str(e), 500

    finally:
        conn.close()

def getPracticeSession(sub):
    from objects.PracticeSession import PracticeSession
    from objects.PracticeInterval import PracticeInterval
    from objects.NotePatternPracticeInterval import  NotePatternPracticeInterval
    from objects.Instrument import Instrument
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM get_practice_session WHERE sub = %s"
            cursor.execute(query, (sub, ))
            result = cursor.fetchall()
        if not result:
            result = addDefaultPrograms('major,scale_to_the_ninth', 'major,single_note_long_tone', 'saxophone', sub)
        sub =  result[0].get('sub')
        userName = result[0].get('userName')
        rounds = result[0].get('rounds')
        setLength = result[0].get('setLength')
        session = PracticeSession(sub, userName, rounds, setLength)

        for exercise in result:
            scaleTonicIndex = exercise.get('scaleTonicIndex')
            scaleTonicSequence = json.loads(exercise.get('tonicSequence'))
            tonic = scaleTonicSequence[exercise.get('scaleTonicIndex')]
            mode = exercise.get('mode')
            primaryCollectionTitle = exercise.get('PrimaryCollectionTitle')
            rhythmCollectionTitle = exercise.get('rhythmCollectionTitle')
            reviewExercise = exercise.get('reviewExercise')
            currentIndex = exercise.get('currentIndex')
            userProgramID = exercise.get('userProgramID')
            primaryCollectionType = exercise.get('PrimaryCollectionType')
            rhythmCollectionID = exercise.get('rhythmCollectionID')
            primaryCollectionID = exercise.get('primaryCollectionID')
            collectionLength = exercise.get('collectionLength')
            instrumentName = exercise.get('instrumentName')
            level = exercise.get('level')
            lowNote = exercise.get('lowNote')
            highNote = exercise.get('highNote')
            defaultTonic = exercise.get('defaultTonic')
            instrument = Instrument(instrumentName, level, lowNote, highNote, defaultTonic)
            # Divide among different collectionTypes here to make different notepattern.
            values = (  tonic,
                        mode,
                        primaryCollectionTitle,
                        rhythmCollectionTitle,
                        currentIndex,
                        userProgramID,
                        primaryCollectionType,
                        primaryCollectionID,
                        rhythmCollectionID,
                        collectionLength,
                        reviewExercise,
                        instrument,
                        scaleTonicSequence,
                        )
            match primaryCollectionType:
                case 'notePattern':
                    # FIXME - RANGE
                    scalePatternType = exercise.get('scalePatternType')
                    session.addInterval(NotePatternPracticeInterval(*values, scalePatternType))
                case _:
                    session.addInterval(PracticeInterval(*values))

        session.collections = getCollections(session)
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
            conn.commit()
            return exercise

    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()

def addNewExercise(values):
    conn = getDBConnection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_new_exercise_proc', [*values])
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
    instruments = getAllInstruments()
    tonicSequences = tonicSequenceList()
    modes =  modeList()
    try:
        cursor = conn.cursor()
        query = "INSERT IGNORE INTO Instruments (" \
                "instrumentName, " \
                "lowNote, " \
                "highNote, " \
                "level, " \
                "defaultTonic" \
                ") VALUES (%s, %s, %s, %s, %s)"

        for instrument in instruments:
            values = (instrument.instrumentName, instrument.lowNote, instrument.highNote, instrument.level, instrument.defaultTonic)
            cursor.execute(query, values)

        query = "INSERT IGNORE INTO TonicSequences (name, sequence) VALUES (%s, %s)"

        for sequence in tonicSequences:
            values = (sequence['name'], json.dumps(sequence['sequence']))
            cursor.execute(query, values)

        query = "INSERT IGNORE INTO scaleModes (scaleModeName, scaleModePattern, diatonicTriads, adjustments) VALUES (%s, %s, %s, %s)"
        for mode in modes:
            values = (mode['modeName'],
                      json.dumps(mode['modePattern']),
                      json.dumps(mode.get('diatonicTriads', None)),
                      json.dumps(mode.get('adjustments', None)))
            cursor.execute(query, values)
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
                values = (program.primaryCollection.title,
                          program.rhythmCollection.title,
                          program.mode,
                          program.tonicSequence.get('name'),
                          program.instrument.instrumentName,
                          program.instrument.level)
                cursor.callproc('add_program_proc', values)
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
            for collectionPattern in collections:
                collectionType = collectionPattern.collectionType
                collectionTitle = collectionPattern.title
                collectionLength = collectionPattern.collectionLength or 0
                # patterns = json.dumps(collection['patterns'])
                match collectionType:
                    case 'notePattern':
                        for pattern in collectionPattern.patterns:
                            values = (collectionTitle,
                                      collectionType,
                                      collectionLength,
                                      pattern.description,
                                      json.dumps(pattern.directions),
                                      pattern.holdLastNote,
                                      json.dumps(pattern.pattern),
                                      pattern.patternType,
                                      pattern.repeatMe,
                                      pattern.patternID,
                                      pattern.noteLength,
                                      getattr(pattern, 'scalePatternType', None))
                            cursor.callproc('insert_notePattern_proc', values)
                    case 'rhythm':
                        for i, pattern in enumerate(collectionPattern.patterns):
                            values = (collectionTitle,
                                      collectionType,
                                      collectionLength,
                                      pattern.description,
                                      json.dumps(pattern.articulation),
                                      json.dumps(pattern.timeSignature),
                                      json.dumps(pattern.pattern),
                                      pattern.patternID,
                                      pattern.rhythmLength,
                                      pattern.measureLength
                                      )
                            cursor.callproc('insert_rhythmPattern_proc', values)
                    case _:
                        pass

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
            conn.commit()
            return result.get('rhythmPatternID')

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        conn.close()
