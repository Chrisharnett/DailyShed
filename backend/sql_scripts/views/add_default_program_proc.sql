USE Daily_Shed;
CALL add_default_program_proc('major_scale_to_the_ninth', 'major_single_note_long_tone', 'saxophone', '534' );

DROP PROCEDURE IF EXISTS add_default_program_proc;

DELIMITER //

CREATE PROCEDURE add_default_program_proc (
	IN program1Name_p	VARCHAR(255),
    IN program2Name_p	VARCHAR(255),
    IN instrumentName_p	VARCHAR(255),
	IN sub_p 			VARCHAR(45)
)
BEGIN 
	DECLARE defaultMode_p			INT;
    DECLARE defaultProgram1_p		INT;
    DECLARE defaultProgram2_p		INT;
    DECLARE userProgramID1_p 		INT;
    DECLARE userProgramID2_p 		INT;
    DECLARE userPracticeRoutine_p 	INT;
    DECLARE message					VARCHAR(255);
    DECLARE sql_error				TINYINT DEFAULT FALSE;
        
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		BEGIN
			SET sql_error = TRUE;
		END;
    
    START TRANSACTION;
    
		SELECT scaleModeID INTO defaultMode_p
		FROM scaleModes sm
        WHERE sm.scaleModeName = 'major';
                            
        SELECT p.programID INTO defaultProgram1_p
		FROM Programs p
		JOIN Collections c ON p.primaryCollectionID = c.collectionID
		JOIN Instruments i ON p.instrumentID = i.instrumentID
		WHERE c.collectionTitle = program1Name_p
		AND i.instrumentName = instrumentName_p
        AND i.level = 'beginner';
		
        SELECT p.programID INTO defaultProgram2_p
		FROM Programs p
		JOIN Collections c ON p.primaryCollectionID = c.collectionID
        JOIN Instruments i ON p.instrumentID = i.instrumentID		
		WHERE c.collectionTitle = program2Name_p
		AND i.instrumentName = instrumentName_p
        AND i.level = 'beginner';
        
        SELECT CONCAT(defaultMode_p, '-', defaultProgram1_p, '-', defaultProgram2_p) INTO message;
		INSERT INTO UserPrograms(programID, sub, scaleTonicIndex) VALUES (defaultProgram1_p, sub_p, 1);	
		IF ROW_COUNT() > 0 THEN
			SELECT LAST_INSERT_ID() INTO userProgramID1_p;
			SET message = CONCAT(message, ' | Inserted UserProgram1:', userProgramID1_p);
			INSERT INTO UserPrograms(programID, sub, scaleTonicIndex) VALUES (defaultProgram2_p, sub_p, 1);
			IF ROW_COUNT() > 0 THEN
				SELECT LAST_INSERT_ID() INTO userProgramID2_p;                    
				SET message = CONCAT(message, ' | Inserted UserProgram2:', userProgramID2_p);
				-- Insert default routine into UserPracticeRoutines
				INSERT INTO UserPracticeRoutines(sub) VALUES (sub_p);
                IF ROW_COUNT() > 0 THEN
					SELECT LAST_INSERT_ID() INTO userPracticeRoutine_p;
					SET message = CONCAT(message, ' | Inserted UserPracticeRoutine:', userPracticeRoutine_p);
					-- Insert default details into UserRoutineExercises
					INSERT INTO UserRoutineExercises (UserPracticeRoutineID, UserProgramID, reviewExercise) 
					VALUES 
						(userPracticeRoutine_p, userProgramID1_p, TRUE),
						(userPracticeRoutine_p, userProgramID1_p, FALSE),
						(userPracticeRoutine_p, userProgramID2_p, TRUE),
						(userPracticeRoutine_p, userProgramID2_p, FALSE);
					IF ROW_COUNT() = 4 THEN
                    SET message = CONCAT(message, ' | Inserted UserRoutineExercises successfully');
                ELSE
                    SET message = CONCAT(message, ' | routineExercises error');
                    SET sql_error = TRUE;
                END IF;                    
            ELSE
                SET message = CONCAT(message, ' | practiceRoutine error');
                SET sql_error = TRUE;
            END IF;
        ELSE
            SET message = CONCAT(message, ' | program error');
            SET sql_error = TRUE;
        END IF;
    ELSE
        SET message = CONCAT(message, ' | program2 error');
        SET sql_error = TRUE;
    END IF;                       
    IF sql_error = FALSE THEN
		COMMIT;
        SELECT * FROM get_practice_session WHERE sub = sub_p;
	ELSE
		SELECT message AS error_message;
		ROLLBACK;        
	END IF;

END //

DELIMITER ;

CALL add_default_program_proc('major_scale_to_the_ninth', 'major_single_note_long_tone', 'saxophone', '534' );

SELECT scaleModeID
FROM scaleModes sm
WHERE sm.scaleModeName = 'major';
                            
SELECT p.programID
FROM Programs p
JOIN Collections c ON p.primaryCollectionID = c.collectionID
JOIN Instruments i ON p.instrumentID = i.instrumentID
WHERE c.collectionTitle = 'major_scale_to_the_ninth'
AND i.instrumentName = 'saxophone'
AND i.level = 'beginner';

SELECT * FROM Collections WHERE collectionTitle = 'major_scale_to_the_ninth';

SELECT p.programID
FROM Programs p
JOIN Collections c ON p.primaryCollectionID = c.collectionID
JOIN Instruments i ON p.instrumentID = i.instrumentID
WHERE c.collectionTitle = 'major_single_note_long_tone'
AND i.instrumentName = 'saxophone'
AND i.level = 'beginner';
        
INSERT INTO UserPrograms(programID, sub) VALUES (350, '534');
INSERT INTO UserPrograms(programID, sub, scaleTonicIndex) VALUES (351, '534', 1);
INSERT INTO UserPracticeRoutines(sub) VALUES ('534');

SELECT * FROM UserPrograms;
SELECT * FROM UserPracticeRoutines;
INSERT INTO UserRoutineExercises (UserPracticeRoutineID, UserProgramID, reviewExercise) 
VALUES 
	(49, 107, TRUE),
	(49, 107, FALSE),
	(49, 108, TRUE),
	(49, 108, FALSE);

SELECT * FROM UserRoutineExercises;

CALL add_new_user_proc('534', 'testemail','testname');
SELECT * FROM users;
DELETE FROM users WHERE sub='534';
INSERT INTO users (sub, email, userName) VALUES ('534', 'testemail','testname');

SELECT * FROM UserPrograms;
SELECT * FROM UserPracticeRoutines;
SELECT * FROM UserRoutineExercises;

SELECT * FROM get_practice_session WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
SELECT * FROM get_practice_session WHERE sub = '534';

SELECT * FROM users;
DELETE FROM UserRoutineExercises;
DELETE FROM UserPrograms;
DELETE FROM UserPracticeRoutines;

SELECT scaleModeID
FROM scaleModes sm
WHERE sm.scaleModeName = 'major';
