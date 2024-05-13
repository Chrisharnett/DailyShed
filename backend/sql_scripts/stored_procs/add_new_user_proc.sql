USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_user_proc;
DELIMITER //

CREATE PROCEDURE add_new_user_proc(
    IN sub         VARCHAR(45),
    IN email       VARCHAR(45),
    IN name        VARCHAR(45)
)
BEGIN
    DECLARE userProgramID1_p 		INT;
    DECLARE userProgramID2_p 		INT;
    DECLARE userPracticeRoutine_p 	INT;
    DECLARE defaultProgram1_p		INT;
    DECLARE defaultProgram2_p		INT;
    DECLARE defaultMode_p			VARCHAR(25);
    
    DECLARE sql_error BOOLEAN DEFAULT FALSE;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
		SET sql_error = TRUE;

    START TRANSACTION;
       
        SELECT scaleModeID INTO defaultMode_p
		FROM scaleModes sm
        WHERE sm.scaleModeName = 'major';
                            
        SELECT p.programID INTO defaultProgram1_p
		FROM Programs p
		JOIN Collections c ON p.primaryCollectionID = c.collectionID
		WHERE c.collectionTitle = 'single_note_long_tone'
		AND scaleModeID = defaultMode_p;
		
        SELECT p.programID INTO defaultProgram2_p
		FROM Programs p
		JOIN Collections c ON p.primaryCollectionID = c.collectionID
		WHERE c.collectionTitle = 'scale_to_the_ninth'
		AND scaleModeID = defaultMode_p;
		
        INSERT INTO users (sub, email, userName) VALUES (sub, email, name);
		-- Check if user insertion was successful
		IF ROW_COUNT() > 0 THEN
			INSERT INTO UserPrograms(programID, sub) VALUES (defaultProgram1_p, sub);

			-- Check if UserPrograms insertion was successful
			IF ROW_COUNT() > 0 THEN
				SELECT LAST_INSERT_ID() INTO userProgramID1_p;
				
				INSERT INTO UserPrograms(programID, sub, scaleTonicIndex) VALUES (defaultProgram2_p, sub, 1);
				SELECT LAST_INSERT_ID() INTO userProgramID2_p;

				-- Insert default routine into UserPracticeRoutines
				INSERT INTO UserPracticeRoutines(sub) VALUES (sub);
				SELECT LAST_INSERT_ID() INTO userPracticeRoutine_p;

				-- Insert default details into UserRoutineExercises
				INSERT INTO UserRoutineExercises (UserPracticeRoutineID, UserProgramID, reviewExercise) 
				VALUES 
					(userPracticeRoutine_p, userProgramID1_p, TRUE),
					(userPracticeRoutine_p, userProgramID1_p, FALSE),
					(userPracticeRoutine_p, userProgramID2_p, TRUE),
					(userPracticeRoutine_p, userProgramID2_p, FALSE);
			ELSE
				SELECT('2') AS message;
				SET sql_error = TRUE;
			END IF;
		ELSE
			SELECT('1') AS message;
			SET sql_error = TRUE;
		END IF;

    IF sql_error = TRUE THEN
        SELECT message;
        ROLLBACK;
    ELSE
		SELECT('User added')
        COMMIT;
    END IF;
END //

DELIMITER ;

CALL add_new_user_proc(534, 'testemail','testname');

SELECT* FROM  UserPrograms;
UPDATE UserPrograms
SET scaleTonicIndex = 1 
WHERE scaleTonicIndex = 0;
 