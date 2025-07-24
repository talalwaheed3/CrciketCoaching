import {
  Box,
  Button,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Typography,
  TextField,
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  LinearProgress,
} from "@mui/material";
import { useEffect, useState, useContext } from "react";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";

export default function ComparePlayerPerformanceByDate() {
  const { user } = useContext(AuthContext);

  const [players, setPlayers] = useState([]);
  const [shots, setShots] = useState([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState("");
  const [selectedShotId, setSelectedShotId] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [performance, setPerformance] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch players and shots
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const playersData = await handleRequest("/coach/get_all_players", "POST", {
                  coach_id: user.id,
                });
        setPlayers(playersData);

        const shotsData = await handleRequest("/coach/get_all_shots", "GET");
        setShots(shotsData);
      } catch (error) {
        console.error("Error fetching initial data:", error);
      }
    };

    fetchInitialData();
  }, [user]);

  // Fetch performance
  const fetchPerformance = async () => {
    if (!selectedPlayerId || !selectedShotId || !dateFrom || !dateTo) return;
    setLoading(true);
    try {
      const data = await handleRequest("/player/compare_performance", "POST", {
        player_id: selectedPlayerId,
        shot_id: selectedShotId,
        dateFrom,
        dateTo,
      });

      if (data.performance) {
        setPerformance(data.performance);
      } else {
        setPerformance([]);
      }
    } catch (error) {
      console.error("Error fetching performance:", error);
    }
    setLoading(false);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        📊 Compare Player Performance by Date
      </Typography>

      <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mb: 3 }}>
        <FormControl fullWidth>
          <InputLabel>Select Player</InputLabel>
          <Select
            value={selectedPlayerId}
            label="Select Player"
            onChange={(e) => setSelectedPlayerId(e.target.value)}
          >
            {players.map((player) => (
              <MenuItem key={player.id} value={player.id}>
                {player.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth>
          <InputLabel>Select Shot</InputLabel>
          <Select
            value={selectedShotId}
            label="Select Shot"
            onChange={(e) => setSelectedShotId(e.target.value)}
          >
            {shots.map((shot) => (
              <MenuItem key={shot.id} value={shot.id}>
                {shot.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Date From"
          type="date"
          InputLabelProps={{ shrink: true }}
          fullWidth
          value={dateFrom}
          onChange={(e) => setDateFrom(e.target.value)}
        />
        <TextField
          label="Date To"
          type="date"
          InputLabelProps={{ shrink: true }}
          fullWidth
          value={dateTo}
          onChange={(e) => setDateTo(e.target.value)}
        />

        <Button
          variant="contained"
          sx={{ alignSelf: "center", mt: { xs: 1, sm: 0 } }}
          onClick={fetchPerformance}
        >
          Compare
        </Button>
      </Box>

      {loading ? (
        <Box sx={{ mt: 4 }}>
          <LinearProgress />
        </Box>
      ) : performance.length > 0 ? (
        <Paper elevation={3}>
          <TableContainer>
            <Table>
              <TableHead sx={{ bgcolor: "#1976d2" }}>
                <TableRow>
                  <TableCell sx={{ color: "white" }}>Session ID</TableCell>
                  <TableCell sx={{ color: "white" }}>Date</TableCell>
                  <TableCell sx={{ color: "white" }}>Correct</TableCell>
                  <TableCell sx={{ color: "white" }}>Incorrect</TableCell>
                  <TableCell sx={{ color: "white" }}>Total Shots</TableCell>
                  <TableCell sx={{ color: "white" }}>Accuracy (%)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {performance.map((session) => (
                  <TableRow key={session.session_id}>
                    <TableCell>{session.session_id}</TableCell>
                    <TableCell>{session.session_date}</TableCell>
                    <TableCell>{session.correct_shots}</TableCell>
                    <TableCell>{session.incorrect_shots}</TableCell>
                    <TableCell>{session.total_shots}</TableCell>
                    <TableCell>
                      <Box sx={{ display: "flex", flexDirection: "column" }}>
                        <Typography>{session.accuracy}%</Typography>
                        <LinearProgress
                          variant="determinate"
                          value={session.accuracy}
                          color={
                            session.accuracy >= 80
                              ? "success"
                              : session.accuracy >= 50
                              ? "warning"
                              : "error"
                          }
                        />
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      ) : (
        <Typography sx={{ mt: 4 }} color="text.secondary">
          No performance data found for selected filters.
        </Typography>
      )}
    </Box>
  );
}
