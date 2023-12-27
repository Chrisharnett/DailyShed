const TheShed = ({ user }) => {
  const { name } = user;
  return (
    <>
      <h1>The Shed</h1>
      <h2>{name}</h2>
    </>
  );
};

export default TheShed;
