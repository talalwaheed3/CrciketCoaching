import { useState, useEffect } from "react";
import {
  Card,
  Typography,
  TextField,
  MenuItem,
  Button,
  FormControl,
  InputLabel,
  OutlinedInput,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Chip,
  Box,
} from "@mui/material";
import handleRequest from "../../utils/handleRequest";

const AddTeamForm = () => {
  const [teamName, setTeamName] = useState("");
  const [selectedCoach, setSelectedCoach] = useState("");
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [coaches, setCoaches] = useState([]);
  const [players, setPlayers] = useState([]);
  const [playerSelectionWarning, setPlayerSelectionWarning] = useState(false);
  const [addTeamWarning, setAddTeamWarning] = useState(false); // NEW STATE for Add Team button warning

  const [openPlayerDialog, setOpenPlayerDialog] = useState(false);
  const [tempSelectedPlayers, setTempSelectedPlayers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const list_of_coaches = await handleRequest(
          "/manager/list_all_users_by_is_assigned",
          "POST",
          { role: "coach", checkAssigned: "false" }
        );
        const list_of_players = await handleRequest(
          "/manager/list_all_users_by_is_assigned",
          "POST",
          { role: "player", checkAssigned: "false" }
        );
        setCoaches(list_of_coaches);
        setPlayers(list_of_players);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  const handleConfirmPlayers = () => {
    if (tempSelectedPlayers.length < 1  ) {
      setPlayerSelectionWarning(true);
    } else {
      setPlayerSelectionWarning(false);
      setSelectedPlayers(tempSelectedPlayers);
      setOpenPlayerDialog(false);
      setAddTeamWarning(false); // Reset warning when players are confirmed
    }
  };

  const handleOpenPlayerDialog = () => {
    setTempSelectedPlayers(selectedPlayers);
    setOpenPlayerDialog(true);
  };

  const handleClosePlayerDialog = () => {
    setOpenPlayerDialog(false);
  };

  const handlePlayerCheck = (player) => {
    setTempSelectedPlayers((prevSelected) =>
      prevSelected.includes(player)
        ? prevSelected.filter((p) => p !== player)
        : [...prevSelected, player]
    );
  };

  const handleRemovePlayer = (player) => {
    setSelectedPlayers((prevSelected) =>
      prevSelected.filter((p) => p !== player)
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!teamName || !selectedCoach || selectedPlayers.length === 0) {
      alert("Please fill all fields!");
      return;
    }

    if (selectedPlayers.length < 1) {
      setAddTeamWarning(true); // Show warning above "Add Team" button
      return;
    }

    const teamData = {
      name: teamName,
      coach_id: selectedCoach,
      players: selectedPlayers,
    };

    try {
      const response = await handleRequest(
        "/manager/add_team",
        "POST",
        teamData
      );
      console.log("Team Created:", response);
      alert("Team created successfully!");
      setTeamName("");
      setSelectedCoach("");
      setSelectedPlayers([]);
      setAddTeamWarning(false); // Reset warning on successful team creation
    } catch (error) {
      console.error("Error creating team:", error);
      alert("Failed to create team.");
    }
  };

  return (
    <Card sx={{ p: 3, maxWidth: 500, margin: "auto", mt: 10 }}>
      <Typography variant="h6">Add Team</Typography>

      <TextField
        fullWidth
        margin="normal"
        label="Team Name"
        value={teamName}
        onChange={(e) => setTeamName(e.target.value)}
      />

      <TextField
        select
        fullWidth
        margin="normal"
        label="Appoint Coach"
        value={selectedCoach}
        onChange={(e) => setSelectedCoach(e.target.value)}
      >
        {coaches.length > 0 ? (
          coaches.map((coach) => (
            <MenuItem key={coach.id} value={coach.id}>
              {coach.name}
            </MenuItem>
          ))
        ) : (
          <MenuItem disabled>No Coaches Available</MenuItem>
        )}
      </TextField>

      <FormControl fullWidth margin="normal">
        <InputLabel>Select Players</InputLabel>
        <OutlinedInput
          readOnly
          value=""
          onClick={handleOpenPlayerDialog}
          placeholder="Click to select players"
        />
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, mt: 1 }}>
          {selectedPlayers.map((player, index) => (
            <Chip
              key={index}
              label={players.find((p) => p.id === player)?.name || "Unknown"} // Fixed player name issue
              onDelete={() => handleRemovePlayer(player)}
              color="primary"
              sx={{
                fontSize: "14px",
                padding: "5px",
                borderRadius: "5px",
                "@media (max-width: 600px)": {
                  fontSize: "12px",
                },
              }}
            />
          ))}
        </Box>
      </FormControl>

      {addTeamWarning && (
        <Typography sx={{ color: "red", mt: 1 }}>
          Please Select at least 15 players!!!
        </Typography>
      )}

      <Dialog open={openPlayerDialog} onClose={handleClosePlayerDialog}>
        <DialogTitle>Select Players</DialogTitle>
        <DialogContent>
          <FormGroup>
            {players.length > 0 ? (
              players.map((player) => (
                <FormControlLabel
                  key={player.id}
                  control={
                    <Checkbox
                      checked={tempSelectedPlayers.includes(player.id)}
                      onChange={() => handlePlayerCheck(player.id)}
                    />
                  }
                  label={player.name}
                />
              ))
            ) : (
              <Typography>No Players Available</Typography>
            )}
          </FormGroup>

          {playerSelectionWarning && (
            <Typography sx={{ color: "red", mt: 1 }}>
              Please Select at least 15 players.
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePlayerDialog} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleConfirmPlayers} color="primary">
            Add
          </Button>
        </DialogActions>
      </Dialog>

      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleSubmit}
      >
        Add Team
      </Button>
    </Card>
  );
};

export default AddTeamForm;
