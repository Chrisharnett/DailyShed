USE Daily_Shed;
CREATE OR REPLACE VIEW get_user_history AS
	 SELECT
		u.userName,
        el.sub,
        MAX(el.timestamp) AS lastPlay,
        GROUP_CONCAT(CONCAT(DATE_FORMAT(el.timestamp, '%d/%m/%Y'), '-', el.comment, '-', el.rating) SEPARATOR '| ') AS playHistory,
        ROUND(AVG(el.rating), 0) AS averageRating,
		COUNT(el.exerciseID) AS playCount,
		e.exerciseName,
        e.imageFilename
	FROM ExerciseLog el
    JOIN users u ON u.sub = el.sub
    JOIN Exercises e ON e.ExerciseID = el.exerciseID
    GROUP BY
		el.exerciseID,
        u.userName
	ORDER BY el.timestamp desc;

   SELECT * FROM get_user_history WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
   
   SELECT
		u.userName,
        MAX(el.timestamp) AS lastPlay,
        GROUP_CONCAT(CONCAT(DATE_FORMAT(el.timestamp, '%d/%m/%Y'), '-', el.comment, '-', el.rating) SEPARATOR ', ') AS playHistory,
        ROUND(AVG(el.rating), 0) AS averageRating,
		COUNT(el.exerciseID) AS playCount,
		e.exerciseName,
        e.imageFilename
	FROM ExerciseLog el
    JOIN users u ON u.sub = el.sub
    JOIN Exercises e ON e.ExerciseID = el.exerciseID
    GROUP BY
		el.exerciseID,
        u.userName
	ORDER BY el.timestamp desc;
    
SELECT * FROM Exercises;