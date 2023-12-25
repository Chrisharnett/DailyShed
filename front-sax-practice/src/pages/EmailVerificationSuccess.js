import { useNavigate } from "react-router-dom";

const EmailVerificationSuccess = () => {
  const navigate = useNavigate();

  return (
    <div className="content-container">
      <h1>Success!</h1>
      <p>
        Thanks for verifying your email, now you can use all the app's features.
      </p>
      <button onClick={() => navigate("/")}>Go to home page</button>
    </div>
  );
};

export default EmailVerificationSuccess;
