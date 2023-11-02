import "bootstrap/dist/css/bootstrap.min.css";
import { Navigate } from "react-router-dom";

const StudentPracticePage = () => {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="../login" replace={true} />;
  } else {
    return <h2>You're Logged In</h2>;
  }
};

export default StudentPracticePage;
