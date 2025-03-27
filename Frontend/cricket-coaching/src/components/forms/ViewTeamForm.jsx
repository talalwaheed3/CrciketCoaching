import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Grid,
  Avatar,
  Box,
  Collapse,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import handleRequest from "../../utils/handleRequest";

const ViewTeam = ({ endpoint }) => {
  const [teams, setTeams] = useState([]);
  const [expandedTeam, setExpandedTeam] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await handleRequest(endpoint, "GET");
        console.log("Fetched Teams:", response);
        setTeams(response);
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    };
    fetchTeams();
  }, []);

  const toggleExpand = (teamId) => {
    setExpandedTeam(expandedTeam === teamId ? null : teamId);
  };

  return (
    <Box sx={{ p: 3, mt: 10 }}>
      <Typography variant="h5" gutterBottom>
        Team Overview
      </Typography>
      <Grid container spacing={3}>
        {teams.map((team) => (
          <Grid item xs={12} sm={6} md={4} key={team.id}>
            <Card sx={{ transition: "0.3s", "&:hover": { boxShadow: 6 } }}>
              <CardMedia
                component="img"
                height="180"
                image={team.image || "/team-placeholder.jpg"}
                alt={team.name}
              />
              <CardContent>
                <Typography variant="h6">{team.name}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Total Players: {team.total_players || "N/A"}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Coach: {team.coach_name || "Not Assigned"}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Contact: {team.contact || "N/A"}
                </Typography>
                <IconButton onClick={() => toggleExpand(team.id)} sx={{ mt: 1 }}>
                  <ExpandMoreIcon />
                </IconButton>
              </CardContent>
              <Collapse in={expandedTeam === team.id} timeout="auto" unmountOnExit>
                <CardContent>
                  <Typography variant="subtitle1">Players</Typography>
                  <List>
                    {team.players?.map((player) => (
                      <ListItem key={player.id}>
                        <ListItemAvatar>
                          <Avatar src={player.image || "/player-placeholder.jpg"} />
                        </ListItemAvatar>
                        <ListItemText primary={player.name} secondary={player.position || "Player"} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Collapse>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ViewTeam;
