USE Daily_Shed;
CREATE OR REPLACE VIEW view_exercises AS
   SELECT 
		e.ExerciseID AS exerciseID,
        e.exerciseName,
        e.tonic,
        e.mode,
        e.directionIndex,
        e.rhythmPatternID,
        e.notePatternID,
        e.imageFilename,
        np.description,     
        rp.articulation,
        c.collectionTitle AS notePatternTitle,
        c.collectionTitle AS rhythmPatternTitle,        
        pe.programID
	FROM Exercises e
    JOIN NotePatterns np ON e.notePatternID = np.notePatternID
    JOIN RhythmPatterns rp ON e.rhythmPatternID = rp.rhythmPatternID
    JOIN CollectionPatterns rcp ON rcp.rhythmPatternID = rp.rhythmPatternID
    JOIN CollectionPatterns ncp ON ncp.notePatternID = e.notePatternID
    JOIN Collections c ON c.collectionID = ncp.collectionID
    JOIN Collections rc ON rc.collectionID = rcp.collectionID
    JOIN ProgramExercises pe ON pe.ExerciseID = e.ExerciseID;
   
   SELECT 
		e.ExerciseID,
        e.exercseName,
        e.tonic,
        e.mode,
        e.directionIndex,
        e.rhythmPatternID,
        e.notePatternID,
        np.description,     
        rp.articulation,
        c.collectionTitle AS notePatternTitle,
        c.collectionTitle AS rhythmPatternTitle,        
        pe.programID
	FROM Exercises e
    JOIN NotePatterns np ON e.notePatternID = np.notePatternID
    JOIN RhythmPatterns rp ON e.rhythmPatternID = rp.rhythmPatternID
    JOIN CollectionPatterns rcp ON rcp.rhythmPatternID = rp.rhythmPatternID
    JOIN CollectionPatterns ncp ON ncp.notePatternID = e.notePatternID
    JOIN Collections c ON c.collectionID = ncp.collectionID
    JOIN Collections rc ON rc.collectionID = rcp.collectionID
    JOIN ProgramExercises pe ON pe.ExerciseID = e.ExerciseID;
    
    SELECT * FROM NotePatterns;