import Dashboard from "../Dashboard";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import SportsCricketIcon from "@mui/icons-material/SportsCricket";
import GroupIcon from "@mui/icons-material/Group";
import VisibilityIcon from "@mui/icons-material/Visibility";

const ManagerDashboard = () => {
  const managerMenuItems = [
    { key: "addCoach", label: "Add Coach", icon: <PersonAddIcon /> },
    { key: "addTeam", label: "Add Team", icon: <AddCircleOutlineIcon /> },
    { key: "addPlayer", label: "Add Player", icon: <SportsCricketIcon /> },
    { key: "viewCoach", label: "View Coach", icon: <VisibilityIcon /> },
    { key: "viewTeam", label: "View Team", icon: <GroupIcon /> },
    { key: "viewPlayer", label: "View Player", icon: <VisibilityIcon /> },
  ];
  return (
    <Dashboard
      userDashboard="Manager Dashboard"
      defaultSection="addCoach"
      menuItems={managerMenuItems}
      role="manager"
    />
  );
};

export default ManagerDashboard;
