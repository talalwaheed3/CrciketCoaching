import ManagerViewTeamForm from "../forms/ManagerViewTeamForm";
import CoachViewTeam from "../forms/CoachViewTeam";
import PlayerViewTeam from "../forms/PlayerViewTeam";

const ViewTeam = ({ role }) => {
  if (role === "manager")
    return <ManagerViewTeamForm endpoint="/manager/list_all_teams" />;
  if (role === "coach") return <CoachViewTeam endpoint="/coach/get_team" />;
  if (role === "player") return <PlayerViewTeam endpoint="/player/get_team" />;

  return <ManagerViewTeamForm endpoint="/manager/list_all_teams" />;
};
export default ViewTeam;
