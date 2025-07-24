import Dashboard from "../Dashboard";
import GroupIcon from "@mui/icons-material/Group";
import EventIcon from "@mui/icons-material/Event";
import { QueryStats } from "@mui/icons-material";

const PlayerDashboard = () => {
  const playerMenuItems = [
    { key: "viewTeam", label: "View Team", icon: <GroupIcon /> },
    { key: "viewJoinedSession", label: "Joined Sessions", icon: <EventIcon /> },
    { key: "viewPerformance", label: "View Performance", icon: <QueryStats /> },
  ];

  return (
    <Dashboard
      userDashboard={"Player Dashboard"}
      defaultSection="viewTeam"
      menuItems={playerMenuItems}
      role="player"
    />
  );
};

export default PlayerDashboard;
