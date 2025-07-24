import PlayerPerformance from "../tables/PlayerPerformance";

const  Performance = ({role}) => {
  
  if (role === 'player') return <PlayerPerformance shotResultEndpoint="/player/get_shot_result" sessionsEnpoint="/player/get_joined_sessions" />;
  if (role === 'coach') return <PlayerPerformance shotResultEndpoint="/coach/get_shot_result" sessionsEnpoint="/coach/get_arranged_sessions" />;
  
};

export default Performance;
