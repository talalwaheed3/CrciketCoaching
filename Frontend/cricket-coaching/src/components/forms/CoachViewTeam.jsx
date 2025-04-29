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

const CoachViewTeam = ({ endpoint }) => {
  const [team, setTeam] = useState(null);
  const { user } = useContext(AuthContext);
  // console.log("In CoachViewTeam user is:", user);

  const fetchTeam = async () => {
    try {
      console.log("trying to send the reqeuest to handleRequest");
      const response = await handleRequest(endpoint, "POST", {
        coach_id: user.id,
      });
      console.log("Fetched Coach's Team:", response);
      setTeam(response[0]);
    } catch (error) {
      console.error("Error fetching team data:", error);
    }
  };
  useEffect(() => {
    fetchTeam();
  }, []);

  useEffect(() => {
    displayTeam();
    console.log("team.name in is:", team ? team.name : null);
  }, [team]);

  function displayTeam() {
    console.log("team in coach_view_team is:", team);
    console.log("team.name in is:", team ? team.name : null);
  }

  if (!team) {
    return <Typography>Loading team details...</Typography>;
    // fetchTeam();
  }

  return (
    <Box sx={{ p: 3, mt: 10 }}>
      {team ? (
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
                Total Players: {team.players.length}
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
                  primary={user.name}
                  secondary={user.contact_no}
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

export default CoachViewTeam;
