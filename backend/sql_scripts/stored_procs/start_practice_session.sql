USE Daily_Shed;
DROP PROCEDURE IF EXISTS start_practice_session;
DELIMITER //

CREATE PROCEDURE start_practice_session(
    IN sub_p				VARCHAR(45)
)

BEGIN
    
		INSERT INTO UserPracticeSession (sub) VALUES (sub_p);
    
		SELECT LAST_INSERT_ID() AS userPracticeSessionID;
    
END //

DELIMITER ;


SELECT * FROM UserPracticeSession;

CALL add_new_user_proc('testSub', 'testEmail', 'testName');
CALL start_practice_session('testSub')