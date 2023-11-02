const SmallExercise = (props) => {
  const { exercise } = props;
  return (
    <>
      <h4>{exercise.exerciseName}</h4>
      <img
        key={props.index}
        src={exercise.imageURL}
        alt={exercise.exerciseName}
        height={50}
      ></img>
      <p>{exercise.exerciseName}</p>
    </>
  );
};

export default SmallExercise;
