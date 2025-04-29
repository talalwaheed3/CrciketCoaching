import ManagerViewTeamForm from "../forms/ManagerViewTeamForm";
import CoachViewTeam from "../forms/CoachViewTeam";

const ViewTeam = ({role}) => {
  if (role === "manager") return <ManagerViewTeamForm endpoint="/manager/list_all_teams" />;
  if (role === "coach") return <CoachViewTeam endpoint="/coach/get_team" />;
  if (role === "player") return <ManagerViewTeamForm endpoint="/manager/list_all_teams" />;

  return <ManagerViewTeamForm endpoint="/manager/list_all_teams" />;
};
export default ViewTeam;
