from util.getDBConnection import getDBConnection
from flask import jsonify

def getNextPitchPattern(interval):
    conn = getDBConnection()
    currentIndex = interval['currentIndex']
    notePatternCollection = interval['notePatternCollectionID']
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_next_pitch_pattern_proc', [currentIndex, notePatternCollection])
            query = "SELECT * FROM NotePatternCollections WHERE sub = %s"
            cursor.execute(query, (sub, ))
            result = cursor.fetchall()
        return result, 200

    except Exception as e:
        return str(e), 500

    finally:
        conn.close()

