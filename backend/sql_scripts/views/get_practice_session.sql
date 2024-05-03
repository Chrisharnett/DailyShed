USE Daily_Shed;
CREATE OR REPLACE VIEW get_practice_session AS
	SELECT 
		u.sub, 
		u.userName,
        pc.collectionTitle AS PrimaryCollectionTitle,
        rc.collectionTitle AS rhythmCollectionTitle,
        p.tonic, 
        p.scaleModeID,
        sm.scaleModeName AS mode,
        upr.rounds,
        upr.setLength,
        ure.reviewExercise,
        up.currentIndex,
        up.userProgramID,
		pc.collectionLength AS collectionLength,
		pc.collectionType AS PrimaryCollectionType,
        p.rhythmCollectionID,
        p.primaryCollectionID
    FROM users u 
    JOIN UserPrograms up ON u.sub = up.sub
    JOIN UserRoutineExercises ure ON(ure.UserProgramID = up.UserProgramID)
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
    JOIN Programs p ON(p.programID = up.programID)
    JOIN scaleModes sm ON sm.scaleModeID = p.scaleModeID
    LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
    LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    ;

SELECT 
		u.sub, 
		u.userName,
        pc.collectionTitle AS PrimaryCollectionTitle,
        rc.collectionTitle AS rhythmCollectionTitle,
        p.tonic, 
        p.scaleModeID,
        upr.rounds,
        upr.setLength,
        ure.reviewExercise,
        up.currentIndex,
		pc.collectionLength AS collectionLength,
		pc.collectionType AS PrimaryCollectionType,
        p.rhythmCollectionID,
        p.primaryCollectionID
    FROM users u 
    JOIN UserPrograms up ON u.sub = up.sub
    JOIN UserRoutineExercises ure ON(ure.UserProgramID = up.UserProgramID)
    JOIN UserPracticeRoutines upr ON(upr.sub = u.sub)
    JOIN Programs p ON(p.programID = up.programID)
    LEFT JOIN Collections rc ON rc.collectionID = p.rhythmCollectionID
    LEFT JOIN Collections pc ON pc.collectionID = p.primaryCollectionID
    WHERE u.userName = 'Chris Harnett';
    
SELECT * FROM users;
SELECT * FROM UserPrograms;
    