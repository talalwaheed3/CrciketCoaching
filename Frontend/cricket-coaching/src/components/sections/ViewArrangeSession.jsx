import { useContext } from "react"
import ViewArrangedSessions from "../tables/ViewArrangedSessionDataTable"
import AuthContext from "../auth/AuthContext"

const ViewArrangeSession = () => {
  const {user} = useContext(AuthContext);
  console.log('In ViewArrangedSessions, role is:', user.id)
  if(user.role === 'coach') return <ViewArrangedSessions endpoint="/coach/get_arranged_sessions" role={user.role} user_id={{coach_id: user.id}} />
  if(user.role === 'player') return <ViewArrangedSessions endpoint="/player/get_joined_sessions" role={user.role} user_id={{player_id: user.id}} />
}
export default ViewArrangeSession
