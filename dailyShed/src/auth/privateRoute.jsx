import { Navigate, Outlet } from "react-router-dom";
import { useUserContext } from "./useUserContext";
import PropTypes from "prop-types";

export const PrivateRoute = ({ redirectPath = "/", children }) => {
  const { user, loading } = useUserContext();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to={redirectPath} replace />;
  }

  return children ? children : <Outlet />;
};

PrivateRoute.propTypes = {
  redirectPath: PropTypes.string,
  children: PropTypes.node,
};
