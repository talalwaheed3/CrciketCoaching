import { useState, useEffect } from "react";
import {
  Card,
  Typography,
  TextField,
  MenuItem,
  Button,
} from "@mui/material";
import { LocalizationProvider, DateTimePicker } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import handleRequest from "../../utils/handleRequest";

const ArrangeSessionForm = ({endpoint}) => {
  const [sessionData, setSessionData] = useState({
    shot: "",
    dateTime: null,
    venue: "",
    player: "",
  });

  const [players, setPlayers] = useState([]);

  // Fetch players on mount
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await handleRequest(endpoint, "POST");
        setPlayers(response);
      } catch (error) {
        console.error("Error fetching players:", error);
      }
    };
    fetchPlayers();
  }, []);

  const handleChange = (e) => {
    setSessionData({ ...sessionData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!sessionData.shot || !sessionData.dateTime || !sessionData.venue || !sessionData.player) {
      alert("Please fill in all fields!");
      return;
    }

    try {
      const response = await handleRequest("/coach/arrange_session", "POST", sessionData);
      console.log("Session Created:", response);
      alert("Session arranged successfully!");
      
      // Reset form
      setSessionData({
        shot: "",
        dateTime: null,
        venue: "",
        player: "",
      });
    } catch (error) {
      console.error("Error arranging session:", error);
      alert("Failed to arrange session.");
    }
  };

  return (
    <Card sx={{ p: 3, maxWidth: 500, margin: "auto", mt: 10 }}>
      <Typography variant="h6">Arrange Training Session</Typography>

      {/* Shot Selection */}
      <TextField
        select
        fullWidth
        margin="normal"
        label="Select Shot"
        name="shot"
        value={sessionData.shot}
        onChange={handleChange}
      >
        {["Cover Drive", "Pull Shot", "Straight Drive", "Sweep"].map((shot) => (
          <MenuItem key={shot} value={shot}>
            {shot}
          </MenuItem>
        ))}
      </TextField>

      {/* Date & Time Picker */}
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DateTimePicker
          label="Select Date & Time"
          value={sessionData.dateTime}
          onChange={(newValue) => setSessionData({ ...sessionData, dateTime: newValue })}
          renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
        />
      </LocalizationProvider>

      {/* Venue Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Venue"
        name="venue"
        value={sessionData.venue}
        onChange={handleChange}
      />

      {/* Player Selection */}
      <TextField
        select
        fullWidth
        margin="normal"
        label="Select Player"
        name="player"
        value={sessionData.player}
        onChange={handleChange}
      >
        {players.length > 0 ? (
          players.map((player) => (
            <MenuItem key={player.id} value={player.id}>
              {player.name}
            </MenuItem>
          ))
        ) : (
          <MenuItem disabled>No Players Available</MenuItem>
        )}
      </TextField>

      {/* Submit Button */}
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleSubmit}
        sx={{ mt: 2 }}
      >
        Arrange Session
      </Button>
    </Card>
  );
};

export default ArrangeSessionForm;
