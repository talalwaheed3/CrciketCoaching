// import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom"; // Fix: Correct import
import WelcomePage from "./components/WelcomePage";
import SignInPage from "./components/auth/SignInPage";
import ManagerDashboard from "./components/dashboard/managerDashboard/ManagerDashboard";
import CoachDashboard from "./components/dashboard/coachDashboard/CoachDashboard";
import PlayerDashboard from "./components/dashboard/playerDashboard/PlayerDashboard";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import AuthContext from "./components/auth/AuthContext";
import { useContext, useEffect } from "react";
import "./styles/App.css";

const App = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      if (user.role.toLowerCase() === "manager") navigate("/managerDashboard");
      if (user.role.toLowerCase() === "coach") navigate("/coachDashboard");
      if (user.role.toLowerCase() === "player") navigate("/playerDashboard");
    }
  }, [user, navigate]);
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/signin" element={<SignInPage />} />
        <Route
          path="/managerDashboard"
          element={
            <ProtectedRoute>
              <ManagerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/coachDashboard"
          element={
            <ProtectedRoute>
              <CoachDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/playerDashboard"
          element={
            <ProtectedRoute>
              <PlayerDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
};

export default App;
