USE Daily_Shed;
DROP PROCEDURE IF EXISTS get_rhythmPattern_options;
DELIMITER //

CREATE PROCEDURE get_rhythmPattern_options(
    IN sub_p VARCHAR(45)
)
BEGIN
    DECLARE primaryCollectionID_p INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE sql_error BOOLEAN DEFAULT FALSE;

    DECLARE cur CURSOR FOR 
        SELECT DISTINCT primaryCollectionID 
        FROM get_practice_session 
        WHERE sub = sub_p;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
    BEGIN
        SET sql_error = TRUE;
        GET DIAGNOSTICS CONDITION 1
        @p_message_text = MESSAGE_TEXT;
        SELECT CONCAT('ERROR: ', @p_message_text) AS ErrorMessage;
    END;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_results (
            programID INT,
            primaryCollectionID INT,
            programTitle VARCHAR(255),
            rhythmCollection VARCHAR(255)
        );

        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO primaryCollectionID_p;
            IF done THEN
                LEAVE read_loop;
            END IF;

            INSERT INTO temp_results (programID, primaryCollectionID, programTitle, rhythmCollection)
            SELECT
                p.programID,
                p.primaryCollectionID,
                pc.collectionTitle AS programTitle,
                rc.collectionTitle AS rhythmCollection
            FROM Programs p
            JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
            JOIN Collections pc ON pc.collectionID = p.PrimaryCollectionID
            WHERE p.primaryCollectionID = primaryCollectionID_p;
        END LOOP;
        CLOSE cur;

        IF sql_error = FALSE THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;

        SELECT * FROM temp_results;
        DROP TEMPORARY TABLE IF EXISTS temp_results;
END //

DELIMITER ;


CALL get_rhythmPattern_options('0b44c9de-c681-479d-8f89-e8af14a57458');
SELECT * FROM get_user_practice_session WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
SELECT DISTINCT primaryCollectionID 
		FROM get_practice_session WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
SELECT * FROM get_rhythmPattern_Options WHERE primaryCollectionID = 127;

SELECT
	p.programID,
	p.primaryCollectionID,
	pc.collectionTitle AS programTitle,
	rc.collectionTitle AS rhythmCollection
FROM Programs p
JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
JOIN Collections pc ON pc.collectionID = p.PrimaryCollectionID
WHERE p.primaryCollectionID = 1338;