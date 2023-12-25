import { useNavigate } from "react-router-dom";

const EmailVerificationFail = () => {
  const navigate = useNavigate();

  return (
    <div className="content-container">
      <h1>Uh Oh!</h1>
      <p>Something went wrong when verifying your email.</p>
      <button onClick={() => navigate("/loginPage")}>Go to home page</button>
    </div>
  );
};

export default EmailVerificationFail;
