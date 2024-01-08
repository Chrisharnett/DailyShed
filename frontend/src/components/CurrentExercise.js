const CurrentExercise = (props) => {
  const { exercise } = props;
  return (
    <>
      <h4>{exercise.exerciseName}</h4>
      <img
        src={exercise.imageURL}
        alt={exercise.description}
        className="currentExercise"
      ></img>
      <p>{exercise.description}</p>
    </>
  );
};

export default CurrentExercise;
