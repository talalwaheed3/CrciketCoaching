import { useState, useEffect, useContext } from "react";
import { Card, Typography, TextField, MenuItem, Button } from "@mui/material";
import { LocalizationProvider, DatePicker, TimePicker } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";
import dayjs from "dayjs";

const ArrangeSessionForm = ({ endpoint }) => {
  const { user } = useContext(AuthContext);
  const [sessionData, setSessionData] = useState({
    shot_id: "",
    name: "",
    date: "",
    session_from: "",
    session_to: "",
    venue: "",
    player_id: "",
    coach_id: user.id,
  });

  const [players, setPlayers] = useState([]);
  const [shots, setShots] = useState([]);

  // Fetch players on mount
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await handleRequest("/coach/get_all_players", "POST", {
          coach_id: user.id,
        });
        setPlayers(response);
      } catch (error) {
        console.error("Error fetching players:", error);
      }
    };
    fetchPlayers();
  }, []);

  useEffect(() => {
    const fetchShots = async () => {
      try {
        const response = await handleRequest("/coach/get_all_shots", "GET");
        setShots(response);
      } catch (error) {
        console.error("Error while fetching shots:", error);
      }
    };
    fetchShots();
  }, []);

  const handleChange = (e) => {
    setSessionData({ ...sessionData, [e.target.name]: e.target.value });
  };

  const handleShotChange = (e) => {
    const selectedShotId = e.target.value;
    const selectedShot = shots.find((shot) => shot.id === selectedShotId);
    setSessionData({
      ...sessionData,
      shot_id: selectedShotId,
      name: selectedShot.name,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      !sessionData.shot_id ||
      !sessionData.date ||
      !sessionData.session_from ||
      !sessionData.session_to ||
      !sessionData.venue ||
      !sessionData.player_id
    ) {
      alert("Please fill in all fields!");
      return;
    }

    try {
      const response = await handleRequest(endpoint, "POST", sessionData);
      alert("Session arranged successfully!");

      // Reset form
      setSessionData({
        shot_id: "",
        date: "",
        session_from: "",
        session_to: "",
        venue: "",
        player_id: "",
        coach_id: user.id,
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
        onChange={handleShotChange}
      >
        {shots.map((shot) => (
          <MenuItem key={shot.id} value={shot.id}>
            {shot.name}
          </MenuItem>
        ))}
      </TextField>

      {/* Date & Time Pickers */}
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        {/* Date Picker */}
        <DatePicker
          label="Select Date"
          value={sessionData.date ? dayjs(sessionData.date) : null}
          onChange={(newValue) => {
            if (newValue) {
              setSessionData({
                ...sessionData,
                date: newValue.format("YYYY-MM-DD"),
              });
            }
          }}
          renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
        />

        {/* Time Picker - Session From */}
        <TimePicker
          label="Session From"
          value={sessionData.session_from ? dayjs(sessionData.session_from, "HH:mm:ss") : null}
          onChange={(newValue) => {
            if (newValue) {
              setSessionData({
                ...sessionData,
                session_from: newValue.format("HH:mm:ss"),
              });
            }
          }}
          renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
        />

        {/* Time Picker - Session To */}
        <TimePicker
          label="Session To"
          value={sessionData.session_to ? dayjs(sessionData.session_to, "HH:mm:ss") : null}
          onChange={(newValue) => {
            if (newValue) {
              setSessionData({
                ...sessionData,
                session_to: newValue.format("HH:mm:ss"),
              });
            }
          }}
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
        name="player_id"
        value={sessionData.player_id}
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
