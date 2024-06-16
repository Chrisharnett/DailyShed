USE Daily_Shed;
DROP PROCEDURE IF EXISTS get_program_data;
DELIMITER //

CREATE PROCEDURE get_program_data(
	IN sub_p	VARCHAR(45)
)
BEGIN
    SELECT * FROM get_user_programs
    WHERE sub = sub_p;
    
    SELECT * FROM Collections
    WHERE collectionType = 'rhythm'
    OR collectionType = 'long_tone_rhythm';
    
    SELECT * FROM scalePatternTypes;
    
    SELECT * FROM TonicSequences;
    
    SELECT * FROM Instruments;
    
    SELECT scaleModeID, scaleModeName FROM scaleModes;

END //

DELIMITER ;

CALL get_program_data('0b44c9de-c681-479d-8f89-e8af14a57458');

 SELECT * FROM Collections
    WHERE collectionType = 'rhythm'
    OR collectionType = 'long_tone_rhythm'
    ;
