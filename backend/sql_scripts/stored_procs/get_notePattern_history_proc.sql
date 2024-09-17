clearAllUSE Daily_Shed;
DROP PROCEDURE IF EXISTS get_notePattern_history_proc;
DELIMITER //

CREATE PROCEDURE get_notePattern_history_proc(
	IN sub_p			INT,
    IN collectionID_p	INT
)
BEGIN
	SELECT e.notePatternID, e.directionIndex, np.directions, COUNT(*) AS playcount 
	FROM ExerciseLog el
	JOIN Exercises e ON el.exerciseID = e.ExerciseID
	JOIN ProgramExercises pe ON el.exerciseID = pe.exerciseID
	JOIN Programs p ON p.programID = pe.programID
	JOIN NotePatterns np ON e.notePatternID = np.notePatternID
	WHERE el.sub = sub_p
	AND p.primaryCollectionID = collectionID_p
	GROUP BY notePatternID; 
    
END //

DELIMITER ;

SELECT cp.notePatternID, e.directionIndex, np.directions, COUNT(*) AS playcount
FROM ExerciseLog el
JOIN Exercises e ON e.exerciseID = el.exerciseID
JOIN ProgramExercises pe ON el.exerciseID = pe.exerciseID
JOIN Programs p ON p.programID = pe.programID
JOIN CollectionPatterns cp ON cp.collectionID = p.primaryCollectionID
JOIN NotePatterns np ON np.notePatternID =  cp.notePatternID
WHERE el.sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
AND cp.collectionID = 129
GROUP BY notePatternID; 

SELECT e.notePatternID, e.directionIndex, np.directions, COUNT(*) AS playcount 
FROM ExerciseLog el
JOIN Exercises e ON el.exerciseID = e.ExerciseID
JOIN ProgramExercises pe ON el.exerciseID = pe.exerciseID
JOIN Programs p ON p.programID = pe.programID
JOIN NotePatterns np ON e.notePatternID = np.notePatternID
WHERE el.sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
AND p.primaryCollectionID = 129
GROUP BY e.notePatternID;


SELECT * FROM Exercises;
SELECT * FROM users;
SELECT * FROM Collections;
SELECT * FROM CollectionPatterns;
SELECT * FROM UserPrograms;
SELECT * FROM get_notePattern_collection;
DELETE FROM ExerciseLog;
UPDATE UserPrograms
    SET currentIndex = -1
    WHERE currentIndex > -1;