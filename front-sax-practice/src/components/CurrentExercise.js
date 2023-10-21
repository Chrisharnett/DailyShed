const CurrentExercise = ({ exercise }, props) => {
  return (
    <>
      <h4>{exercise.exerciseName}</h4>
      <img
        src={exercise.exerciseURL}
        alt={exercise.description}
        height={100}
      ></img>
      <p>{exercise.description}</p>
    </>
  );
};

export default CurrentExercise;
