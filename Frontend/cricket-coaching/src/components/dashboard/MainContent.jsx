import AddCoachForm from "../forms/AddCoachForm";
import AddPlayerForm from "../forms/AddPlayerForm";
import AddTeamForm from "../forms/AddTeamForm";
import ViewCoach from "../sections/ViewCoach";
import ViewPlayer from '../sections/ViewPlayer'
import ViewTeam from '../sections/ViewTeam'
import ArrangeSession from "../sections/ArrangeSession";
import ViewArrangeSession from "../sections/ViewArrangeSession";
import SessionResults from "../sections/SessionResults";

const MainContent = ({ selectedSection, role }) => {
  switch (selectedSection) {
    case "addCoach":
      return <AddCoachForm />;
    case "addTeam":
      return <AddTeamForm />;
    case "addPlayer":
      return <AddPlayerForm />;
    case "viewCoach":
      return <ViewCoach />;
    case "viewTeam":
      return <ViewTeam role={role}/>;
    case "viewPlayer":
      return <ViewPlayer />;
    case "arrangeSession":
      return <ArrangeSession />  
    case "viewArrangeSession":
      return <ViewArrangeSession /> 
    case "viewJoinedSession":
      return <ViewArrangeSession /> 
    case 'viewResults':
      return <SessionResults />
    default:
      return null;
  }
};

export default MainContent;
