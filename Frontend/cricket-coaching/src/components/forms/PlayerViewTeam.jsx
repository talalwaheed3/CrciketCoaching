import { useState, useEffect, useContext } from "react";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Grid,
  Avatar,
  Box,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
} from "@mui/material";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";

const PlayerViewTeam = ({ endpoint }) => {
  const [team, setTeam] = useState({});
  const { user } = useContext(AuthContext);
  // console.log("In CoachViewTeam user is:", user);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        console.log("trying to send the request to handleRequest");
        console.log(
          "player id to send the request to handleRequest is:",
          user.id
        );
        const response = await handleRequest(endpoint, "POST", {
          player_id: user.id,
        });
        console.log("Fetched Player's Team:", response);
        console.log(
          "response['team_coach']['coach']['name']:",
          response["team_coach"]["coach"]["name"]
        );
        setTeam(response);
      } catch (error) {
        alert("Error fetching team data:", error);
      }
    };
    fetchTeam();
  }, []);

  useEffect(() => {
    function displayTeam() {
      console.log("team in coach_view_team is:", team);
      console.log("team.name in is:", team ? team.name : null);
      console.log(
        "team['team_coach']['coach']['name']  is:",
        team ? team["team_coach"]["coach"]["name"] : null
      );
    }
    if (Object.keys(team).length > 0) displayTeam();
    console.log("team.name in is:", team ? team.name : null);
  }, [team]);

  return (
    <Box sx={{ p: 3, mt: 10 }}>
      {Object.keys(team).length > 0 ? (
        <Paper sx={{ p: 3, backgroundColor: "#f5f5f5" }} elevation={4}>
          {/* Team Info */}
          <Typography
            variant="h5"
            fontWeight="bold"
            align="center"
            gutterBottom
          >
            {team.name} - Team Overview
          </Typography>
          <Card sx={{ maxWidth: 300, mx: "auto", mb: 3 }}>
            <CardMedia
              component="img"
              height="200"
              image="./Cricket_team logo.png"
              alt={team.name}
            />
            <CardContent>
              <Typography variant="h6" align="center">
                {team.name}
              </Typography>
              <Typography variant="body2" align="center" color="textSecondary">
                Total Players: {10}
              </Typography>
            </CardContent>
          </Card>

          {/* Players List */}
          <Typography variant="h6" fontWeight="bold" gutterBottom>
            Players:
          </Typography>
          <Grid container spacing={2}>
            {team.players
              ? team.players.map((player) => (
                  <Grid item xs={12} sm={6} md={4} key={player.id}>
                    <Card sx={{ display: "flex", alignItems: "center", p: 2 }}>
                      <Avatar
                        src={player.image || "/player-placeholder.jpg"}
                        sx={{ width: 56, height: 56, mr: 2 }}
                      />
                      <CardContent>
                        <Typography variant="body1" fontWeight="bold">
                          {player.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {player.type || "Player"}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))
              : "No players"}
          </Grid>

          {/* Coach Info */}
          <Box mt={4}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Coach Details:
            </Typography>
            <List>
              <ListItem>
                <ListItemAvatar>
                  <Avatar src="./pfp.png" />
                </ListItemAvatar>
                <ListItemText
                  primary={team.team_coach.coach.name}
                  secondary={team.team_coach.coach.contact_no}
                  // secondary={`Contact: ${team.coach.contact_no || "N/A"}`}
                />
              </ListItem>
            </List>
          </Box>
        </Paper>
      ) : (
        <Paper sx={{ p: 3, backgroundColor: "#f5f5f5" }} elevation={4}>
          <Typography
            variant="h5"
            fontWeight="bold"
            align="center"
            gutterBottom
          >
            No Team Assigned Currently
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default PlayerViewTeam;
