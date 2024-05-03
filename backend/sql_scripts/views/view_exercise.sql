USE Daily_Shed;
CREATE OR REPLACE VIEW view_exercises AS
	SELECT 
		e.ExerciseID,
        e.tonic,
        e.mode,
        np.description,
        e.directionIndex,
        rp.articulation,
        c.collectionTitle AS notePatternTitle,
        c.collectionTitle AS rhythmPatternTitle,
        e.rhythmPatternID,
        e.notePatternID,
        pe.programID
	FROM Exercises e
    JOIN NotePatterns np ON e.notePatternID = e.notePatternID
    JOIN RhythmPatterns rp ON e.notePatternID = np.notePatternID
    LEFT JOIN CollectionPatterns rcp ON rcp.rhythmPatternID = rp.rhythmPatternID
    LEFT JOIN CollectionPatterns ncp ON ncp.notePatternID = e.notePatternID
    LEFT JOIN Collections c ON c.collectionID = ncp.collectionID
    LEFT JOIN Collections rc ON rc.collectionID = rcp.collectionID
    JOIN ProgramExercises pe ON pe.ExerciseID = e.ExerciseID;
    ;
   
   
   SELECT * FROM UserPrograms;