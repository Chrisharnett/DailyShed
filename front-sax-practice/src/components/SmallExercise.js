const SmallExercise = (props) => {
  const { index, exercise } = props;
  return (
    <>
      <h4 key={"h" + index}>{exercise.exerciseName}</h4>
      <img
        key={index}
        src={exercise.imageURL}
        alt={exercise.description}
        height={50}
      ></img>
      <p key={"d" + index}>{exercise.description}</p>
    </>
  );
};

export default SmallExercise;
