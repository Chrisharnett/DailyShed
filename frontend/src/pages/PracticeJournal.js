const PracticeJournal = ({ user }) => {
  const { name } = user;
  return (
    <>
      <h1>Practice Journal</h1>
      <h2>{name}</h2>
    </>
  );
};

export default PracticeJournal;
