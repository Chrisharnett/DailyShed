USE Daily_Shed;
CREATE OR REPLACE VIEW get_practice_session AS
-- rounds, setLength, exercises, program, ?history
	SELECT u.sub, u.userName
    FROM users u;
    

SELECT * FROM get_practice_session;