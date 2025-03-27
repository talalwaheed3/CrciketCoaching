import { useState, useEffect } from "react";
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

const CoachViewTeam = ({ endpoint }) => {
  const [team, setTeam] = useState(null);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const response = await handleRequest(endpoint, "GET");
        console.log("Fetched Coach's Team:", response);
        setTeam(response);
      } catch (error) {
        console.error("Error fetching team data:", error);
      }
    };
    fetchTeam();
  }, [endpoint]);

  if (!team) {
    return <Typography>Loading team details...</Typography>;
  }

  return (
    <Box sx={{ p: 3, mt: 10 }}>
      <Paper sx={{ p: 3, backgroundColor: "#f5f5f5" }} elevation={4}>
        {/* Team Info */}
        <Typography variant="h5" fontWeight="bold" align="center" gutterBottom>
          {team.name} - Team Overview
        </Typography>

        <Card sx={{ maxWidth: 500, mx: "auto", mb: 3 }}>
          <CardMedia
            component="img"
            height="200"
            image={team.image || "Cricket_team_logo.png"}
            alt={team.name}
          />
          <CardContent>
            <Typography variant="h6" align="center">
              {team.name}
            </Typography>
            <Typography variant="body2" align="center" color="textSecondary">
              Total Players: {team.total_players}
            </Typography>
          </CardContent>
        </Card>

        {/* Players List */}
        <Typography variant="h6" fontWeight="bold" gutterBottom>
          Players:
        </Typography>
        <Grid container spacing={2}>
          {team.players.map((player) => (
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
          ))}
        </Grid>

        {/* Coach Info */}
        <Box mt={4}>
          <Typography variant="h6" fontWeight="bold" gutterBottom>
            Coach Details:
          </Typography>
          <List>
            <ListItem>
              <ListItemAvatar>
                <Avatar src={team.coach.image || "/coach-placeholder.jpg"} />
              </ListItemAvatar>
              <ListItemText
                primary={team.coach.name}
                secondary={`Contact: ${team.coach.contact_no || "N/A"}`}
              />
            </ListItem>
          </List>
        </Box>
      </Paper>
    </Box>
  );
};

export default CoachViewTeam;
