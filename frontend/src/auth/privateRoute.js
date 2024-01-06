import { Navigate, Outlet } from "react-router-dom";
import useUser from "./useUser";

export const PrivateRoute = ({ redirectPath = "/", children }) => {
  const user = useUser();
  if (!user) return <Navigate to={redirectPath} replace />;

  return children ? children : <Outlet />;
};
