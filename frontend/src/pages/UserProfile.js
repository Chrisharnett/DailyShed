const UserProfile = ({ user }) => {
  const { name } = user;
  return (
    <>
      <h1>User Profile</h1>
      <h2>{name}</h2>
    </>
  );
};

export default UserProfile;
