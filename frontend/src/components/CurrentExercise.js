const CurrentExercise = (props) => {
  const { exercise } = props;
  return (
    <>
      <h4>{exercise.exerciseName}</h4>
      <img src={props.src} alt={exercise.description} height={100}></img>
      <p>{exercise.description}</p>
    </>
  );
};

export default CurrentExercise;
