import Dashboard from "../Dashboard";
import GroupIcon from "@mui/icons-material/Group";
import EventIcon from "@mui/icons-material/Event";
import TodayIcon from "@mui/icons-material/Today";

const CoachDashboard = () => {
  const coachMenuItems = [
    { key: "viewTeam", label: "View Team", icon: <GroupIcon /> },
    { key: "arrangeSession", label: "Arrange Session", icon: <EventIcon /> },
    { key: "viewArrangeSession", label: "View Sessions", icon: <TodayIcon /> },
    {
      key: "viewPerformance",
      label: "View Sessions Results",
      icon: <TodayIcon />,
    },
    { key: "addIdealAngles", label: "Ideal Angles", icon: <TodayIcon /> },
    { key: "bestShotAngle", label: "Best Shot Angle", icon: <TodayIcon /> },
    // { key: "ideaAnglelRange", label: "Ideal Angle Range", icon: <TodayIcon /> },
    // { key: "trackProgress", label: "Track Progress", icon: <TodayIcon /> },
    // { key: "comparePlayerPerformanceByDate", label: "Compare Player Performance", icon: <TodayIcon /> },
  ];

  return (
    <Dashboard
      userDashboard="Coach Dashboard"
      defaultSection="viewTeam"
      menuItems={coachMenuItems}
      role="coach"
    />
  );
};

export default CoachDashboard;
