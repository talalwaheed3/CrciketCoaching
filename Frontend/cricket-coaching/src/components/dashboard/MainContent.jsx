import UserForm from "../forms/UserForm";
import AddTeamForm from "../forms/AddTeamForm";
import ViewUserTable from "../tables/ViewUserTable";
import ViewTeam from "../sections/ViewTeam";
import ArrangeSession from "../sections/ArrangeSession";
import ViewArrangeSession from "../sections/ViewArrangeSession";
import Performance from "../sections/Performance";
import IdealAngles from "../sections/IdealAngles";
import TrackProgress from "../sections/TrackProgress";
import ComparePlayerPerformanceByDate from "../sections/ComparePlayerPerformanceByDate";
import AddIdealAngles from "../sections/AddIdealAngles";
import BestShotAngle from "../sections/BestShotAngle";

const MainContent = ({ selectedSection, role }) => {
  switch (selectedSection) {
    case "addCoach":
      return <UserForm roleType="coach" apiEndpoint="/manager/add_coach" />;
    case "addTeam":
      return <AddTeamForm />;
    case "addPlayer":
      return <UserForm roleType="player" apiEndpoint="/manager/add_player" />;
    case "viewCoach":
      return (
        <ViewUserTable
          body={{ role: "coach" }}
          endpoint="/manager/list_all_users"
        />
      );
    case "viewTeam":
      return <ViewTeam role={role} />;
    case "viewPlayer":
      return (
        <ViewUserTable
          body={{ role: "player" }}
          endpoint="/manager/list_all_users"
        />
      );
    case "arrangeSession":
      return <ArrangeSession />;
    case "viewArrangeSession":
      return <ViewArrangeSession />;
    case "viewJoinedSession":
      return <ViewArrangeSession />;
    case "viewPerformance":
      return <Performance role={role} />;
    case "addIdealAngles":
      return <AddIdealAngles />;
    case "bestShotAngle":
      return <BestShotAngle />;
    // case "ideaAnglelRange":
    //   return <IdealAngles />;
    // case "trackProgress":
    //   return <TrackProgress />;
    // case "comparePlayerPerformanceByDate":
    //   return <ComparePlayerPerformanceByDate />;
    default:
      return null;
  }
};

export default MainContent;
