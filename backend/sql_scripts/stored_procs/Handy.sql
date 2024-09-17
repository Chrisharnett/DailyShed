-- TABLES
SELECT * FROM Exercises;
SELECT * FROM CollectionPatterns;
SELECT * FROM ExerciseLog;
SELECT * FROM pitchNames;
SELECT * FROM ProgramExercises;
SELECT * FROM UserPracticeRoutines 
	-- WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
    ;
SELECT * FROM UserPracticeSession;
SELECT * FROM UserPracticeSessionExercises;
SELECT * FROM UserPrograms;
SELECT * FROM UserRoutineExercises;
SELECT * FROM users;
SELECT scalePatternType, notePatternType, description FROM NotePatterns;
SELECT * FROM RhythmPatterns;
SELECT * FROM Instruments;
SELECT * FROM TonicSequences;
SELECT * FROM Programs;
SELECT * FROM scaleModes;
SELECT * FROM Collections;
SELECT * FROM scalePatternTypes;
SELECT * FROM CollectionType;

CALL clear_collections_and_exercises_proc();

-- VIEWS
SELECT sub, reviewExercise, programID, PrimaryCollectionTitle, rhythmCollectionTitle FROM get_practice_session WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
SELECT * FROM get_user_practice_session 
-- WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458'
;
SELECT * FROM get_user_programs;
SELECT 
	*
	-- up.userProgramID, c.collectionTitle 
FROM UserRoutineExercises ure
JOIN UserPrograms up ON ure.UserProgramID = up.userProgramID
JOIN Programs p ON p.programID = up.programID
JOIN Collections c ON p.primaryCollectionID = c.collectionID
WHERE ure.UserPracticeRoutineID = 106
;

SELECT * FROM view_exercises
WHERE notePatternID = 14362;


-- STORED PROCS
CALL clear_collections_and_exercises_proc();

CALL clear_exercises_proc();

CALL reset_player_proc();

DELETE FROM UserPrograms;
DELETE FROM UserRoutineExercises;

SET foreign_key_checks = 1;
INSERT INTO scalePatternTypes (scalePatternType, allKeys, rhythmType) VALUES ('test', 0, 'test');

ALTER TABLE scalePatternTypes
ADD CONSTRAINT fk_collectionType
FOREIGN KEY (rhythmType)
REFERENCES other_table(collectionType);