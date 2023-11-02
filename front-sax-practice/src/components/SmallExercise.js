const SmallExercise = (props) => {
  const { exercise } = props;
  return (
    <>
      <h4>{exercise.exerciseName}</h4>
      <img
        key={props.index}
        src={exercise.imageURL}
        alt={exercise.description}
        height={50}
      ></img>
      <p>{exercise.description}</p>
    </>
  );
};

export default SmallExercise;
