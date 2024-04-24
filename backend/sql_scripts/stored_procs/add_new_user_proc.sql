USE Daily_Shed;
DROP PROCEDURE IF EXISTS add_new_user_proc;
DELIMITER //

CREATE PROCEDURE add_new_user_proc(
    IN sub         VARCHAR(45),
    IN email       VARCHAR(45),
    IN name        VARCHAR(45)
)
BEGIN
    DECLARE userProgramID1_p INT;
    DECLARE userProgramID2_p INT;
    DECLARE userPracticeRoutine_p INT;
    
    -- Declare variable to track whether an error occurred
    DECLARE error_occurred BOOLEAN DEFAULT FALSE;

    -- Start transaction
    START TRANSACTION;

    -- Insert user
    INSERT INTO users (sub, email, userName) VALUES (sub, email, name);

    -- Check if user insertion was successful
    IF ROW_COUNT() > 0 THEN
        -- Insert default programs/user into userPrograms
        INSERT INTO UserPrograms(programID, sub) VALUES (2, sub);

        -- Check if UserPrograms insertion was successful
        IF ROW_COUNT() > 0 THEN
            -- Get the IDs generated from the inserts into UserPrograms
            SELECT LAST_INSERT_ID() INTO userProgramID1_p;
            
            INSERT INTO UserPrograms(programID, sub) VALUES (3, sub);
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
            SET error_occurred = TRUE;
        END IF;
    ELSE
        SET error_occurred = TRUE;
    END IF;

    IF error_occurred THEN
        SELECT('user not added')
        ROLLBACK;
    ELSE
		SELECT('User added')
        COMMIT;
    END IF;
END //


DELIMITER ;


CALL add_new_user_proc(421, 'testemail','testname');
CALL clearUsers();
SELECT * FROM users;
SELECT * FROM UserPrograms;
SELECT * FROM UserPracticeRoutines;
SELECT * FROM UserRoutineExercises;

 INSERT INTO users (sub, email, userName) VALUES (1, 'email@test.com', 'name');
 INSERT INTO UserPrograms(programID, sub) VALUES (2, 1), (3, 1);
 INSERT INTO UserPracticeRoutines(sub) VALUES (1);
 
 SELECT * FROM users;
 SELECT * FROM UserPracticeRoutines;
 SELECT * FROM UserPrograms;
 
 INSERT INTO UserRoutineExercises (UserPracticeRoutineID, UserProgramID, reviewExercise) 
	VALUES 
		(2, 7, TRUE),
		(2, 7, FALSE),
		(2, 8, TRUE),
		(2, 8, FALSE);
 