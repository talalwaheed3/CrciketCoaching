import { Navigate } from "react-router-dom";
import AuthContext from "./AuthContext";
import { useContext } from "react";

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);

  return user ? children : <Navigate to="/signin" />;
};
export default ProtectedRoute;
