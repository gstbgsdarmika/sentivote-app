/* eslint-disable react/prop-types */
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ element }) => {
  // Periksa keberadaan token
  const authToken = localStorage.getItem("token");

  return authToken ? element : <Navigate to="/login" />;
};

export default ProtectedRoute;
