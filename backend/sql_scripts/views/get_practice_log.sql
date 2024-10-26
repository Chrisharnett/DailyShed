CREATE OR REPLACE VIEW get_practice_log AS

	SELECT el.sub, el.timeStamp, el.comment, el.rating, el.sessionID, e.exerciseName, e.imagefileName 
	FROM ExerciseLog el
	JOIN Exercises e ON(el.exerciseID = e.exerciseId);


SELECT * FROM get_practice_log;
