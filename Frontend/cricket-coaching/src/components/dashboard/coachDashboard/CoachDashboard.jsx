import Dashboard from "../Dashboard";
import GroupIcon from "@mui/icons-material/Group";
import EventIcon from "@mui/icons-material/Event";
import TodayIcon from "@mui/icons-material/Today";

const CoachDashboard = () => {
  const coachMenuItems = [
    { key: "viewTeam", label: "View Team", icon: <GroupIcon /> },
    { key: "arrangeSession", label: "Arrange Session", icon: <EventIcon /> },
    { key: "viewArrangeSession", label: "View Sessions", icon: <TodayIcon /> },
    { key: "viewResults", label: "View Sessions Results", icon: <TodayIcon /> },
  ];

  return <Dashboard userDashboard="Coach Dashboard" defaultSection="viewTeam" menuItems={coachMenuItems} role="coach"/>;
};

export default CoachDashboard;
