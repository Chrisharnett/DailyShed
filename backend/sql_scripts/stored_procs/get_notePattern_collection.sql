USE Daily_Shed;

CREATE OR REPLACE VIEW get_notePattern_collection AS

SELECT 
        -- el.sub AS sub,
        cp.collectionID AS collectionID,
        cp.notePatternID AS notePatternID,
        np.collectionNotePatternID AS collectionNotePatternID,
        np.noteLength AS noteLength,
        np.description AS description,
        np.directions AS directions,
        np.holdLastNote AS holdLastNote,
        np.notePatternType AS notePatternType,
        np.repeatMe AS repeatMe,
        np.notePattern AS notePattern,
        e.directionIndex AS directionIndex
    FROM
        CollectionPatterns cp
        JOIN NotePatterns np ON np.notePatternID = cp.notePatternID
        LEFT JOIN Exercises e ON np.notePatternID = e.notePatternID
        GROUP BY notePatternID 
        ;
        
SELECT * FROM get_notePattern_collection
;

SELECT * FROM Collections;

SELECT * FROM CollectionPatterns 
where collectionID = 129
;