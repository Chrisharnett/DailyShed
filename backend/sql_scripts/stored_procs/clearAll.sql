USE Daily_Shed;
DROP PROCEDURE IF EXISTS clearAll;
DELIMITER //

CREATE PROCEDURE clearAll()

BEGIN
	DELETE FROM CollectionPatterns;
	DELETE FROM UserRoutineExercises;
	DELETE FROM UserPracticeRoutines;
	DELETE FROM UserPrograms;
	DELETE FROM Programs;
	DELETE FROM Collections;
	DELETE FROM NotePatterns;
	DELETE FROM RhythmPatterns;
	DELETE FROM users;
    
END //

DELIMITER ;

call clearAll;