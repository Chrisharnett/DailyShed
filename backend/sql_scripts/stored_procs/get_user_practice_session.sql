USE Daily_Shed;
CREATE OR REPLACE VIEW get_user_practice_session AS
	SELECT 
		u.sub,
        p.programID AS programID,
        upr.rounds,
        ure.reviewExercise,
        up.userProgramID,
        pc.scalePatternType,
        p.rhythmCollectionID,
        p.primaryCollectionID
        
	FROM users u 
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
	JOIN UserRoutineExercises ure ON(ure.UserPracticeRoutineID = upr.UserPracticeRoutineID)
    JOIN UserPrograms up ON up.UserProgramID =  ure.UserProgramID
    JOIN Programs p ON(p.programID = up.programID)
    JOIN Instruments i ON i.instrumentID = p.instrumentID
	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
    JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
    LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
    LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    WHERE upr.isActive = true
    ;
    
    SELECT * FROM get_user_practice_session
    WHERE sub = '0b44c9de-c681-479d-8f89-e8af14a57458';
  
  SELECT 
		u.sub,
        p.programID AS programID,
        upr.rounds,
        ure.reviewExercise,
        up.userProgramID,
        pc.scalePatternType,
        p.rhythmCollectionID,
        p.primaryCollectionID
        
	FROM users u 
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
	JOIN UserRoutineExercises ure ON(ure.UserPracticeRoutineID = upr.UserPracticeRoutineID)
    JOIN UserPrograms up ON up.UserProgramID =  ure.UserProgramID
    JOIN Programs p ON(p.programID = up.programID)
    JOIN Instruments i ON i.instrumentID = p.instrumentID
	JOIN TonicSequences ts ON ts.tonicSequenceID = p.tonicSequenceID
    JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
    LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
    LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    WHERE upr.isActive = true
    ;
   