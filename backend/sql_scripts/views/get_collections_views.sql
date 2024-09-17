USE Daily_Shed;

CREATE OR REPLACE VIEW get_rhythmPattern_collection AS
	SELECT cp.collectionID, 
		cp.rhythmPatternID, 
        rp.collectionRhythmPatternID, 
        rp.rhythmLength,
        rp.rhythmDescription,
        rp.articulation,
        rp.timeSignature,
        rp.rhythmPattern
    FROM CollectionPatterns cp
    JOIN RhythmPatterns rp
    ON rp.rhythmPatternID = cp.rhythmPatternID
	;

CREATE OR REPLACE VIEW get_notePattern_collection AS
-- TODO INCLUDE PLAYERS directionIndex FROM exerciseLog
	SELECT el.sub,
		cp.collectionID, 
		cp.notePatternID, 
		np.collectionNotePatternID, 
        np.noteLength,
        np.description,
        np.directions,
        np.holdLastNote,
        np.notePatternType,
        np.repeatMe,
        np.notePattern,
        e.directionIndex
    FROM CollectionPatterns cp
    JOIN NotePatterns np ON np.notePatternID = cp.notePatternID
    LEFT JOIN Exercises e ON np.notePatternID = e.notePatternID
    LEFT JOIN ExerciseLog el ON e.exerciseID = el.exerciseID
	;
    

SELECT el.sub,
		cp.collectionID, 
		cp.notePatternID, 
		np.collectionNotePatternID, 
        np.noteLength,
        np.description,
        np.directions,
        np.holdLastNote,
        np.notePatternType,
        np.repeatMe,
        np.notePattern,
        e.directionIndex
    FROM CollectionPatterns cp
    JOIN NotePatterns np ON np.notePatternID = cp.notePatternID
    LEFT JOIN Exercises e ON np.notePatternID = e.notePatternID
    LEFT JOIN ExerciseLog el ON e.exerciseID = el.exerciseID
	;