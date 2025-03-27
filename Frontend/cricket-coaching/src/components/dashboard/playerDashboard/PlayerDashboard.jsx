import Dashboard from "../Dashboard";

const PlayerDashboard = () => {
  return (
    <Dashboard
      userDashboard={"Player Dashboard"}
      defaultSection="addCoach"
      role="player"
    />
  );
};

export default PlayerDashboard;
