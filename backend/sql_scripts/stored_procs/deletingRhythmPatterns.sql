SELECT * FROM Collections;

DELETE FROM ProgramExercises
WHERE ExerciseID IN (
	SELECT ExerciseID
    FROM Exercises
    Where rhythmPatternID >= 2638
    );
    
DELETE 
FROM UserPracticeSessionExercises
WHERE ExerciseID IN (
	SELECT ExerciseID
    FROM Exercises
    Where rhythmPatternID >= 2638
    );

DELETE 
FROM ExerciseLog
WHERE ExerciseID IN (
	SELECT ExerciseID
    FROM Exercises
    Where rhythmPatternID >= 2638
    );

DELETE FROM Exercises
WHERE rhythmPatternID >= 2638
; 

DELETE 
FROM CollectionPatterns
WHERE rhythmPatternID >= 2638
; 

DELETE FROM Daily_Shed.RhythmPatterns
WHERE rhythmPatternID >= 2638
;