USE Daily_Shed;
DROP PROCEDURE IF EXISTS insert_collection_proc;

DELIMITER //

CREATE PROCEDURE insert_collection_proc (
	IN collection_title_p 	VARCHAR(255),
    IN collection_type_p	VARCHAR(255),
    IN collection_length_p	INT,
    IN patterns_p			TEXT
    
)
BEGIN 
	DECLARE collectionID_p		INT;
	DECLARE finished 			TINYINT DEFAULT 0;
    DECLARE description_p		TEXT;
    DECLARE direction_p			VARCHAR(25);
    DECLARE directions_p		JSON;
    DECLARE holdLastNote_p		TINYINT DEFAULT 0;
    DECLARE notePattern_p 		JSON;
    DECLARE notePatternType_p	VARCHAR(45);
    DECLARE repeatMe_p			TINYINT DEFAULT 0;
    
    DECLARE pattern_cursor CURSOR FOR SELECT 
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].notePatternType'))) AS notePatternType,
        JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].notePattern')) AS notePattern,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].description'))) AS description,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].direction'))) AS direction,
        JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].directions')) AS directions,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].repeatMe'))) AS repeatMe,
        JSON_UNQUOTE(JSON_EXTRACT(patterns_p, CONCAT('$[', _i, '].holdLastNote'))) AS holdLastNote
        FROM DUAL;
    
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
     
	INSERT INTO Collections (collection_title, collection_type, collection_length) VALUES (collection_title_p, collection_type_p, collection_length_p);
    SET collectionID_p = LAST_INSERT_ID();
    
    OPEN pattern_cursor;
    
    read_loop: LOOP
		FETCH pattern_cursor INTO notePatternType_p, notePattern_p, description_p, direction_p, directions_p, repeatMe_p, holdLastNote_p;
    
		IF finished THEN
			LEAVE read_loop;
        END IF;
        
        INSERT INTO NotePatterns
    
    

    END //

DELIMITER ;


USE Daily_Shed;
SELECT * FROM Collections;
DELETE FROM Collections;


CALL insert_collection_proc("Test title");