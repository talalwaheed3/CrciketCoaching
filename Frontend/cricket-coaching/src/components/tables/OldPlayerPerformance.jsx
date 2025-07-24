import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Tabs,
  Tab,
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Button,
} from "@mui/material";
import ImageIcon from "@mui/icons-material/Image";
import { VideoIcon } from "lucide-react";
import AssessmentIcon from "@mui/icons-material/Assessment";
import { useContext, useEffect, useState } from "react";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";
import "./SessionResults.css"; // We'll add some styling separately

export default function PlayerPerformance({
  shotResultEndpoint,
  sessionsEnpoint,
}) {
  const { user } = useContext(AuthContext);
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState("");
  const [sessionData, setSessionData] = useState([]);
  const [currentShotIndex, setCurrentShotIndex] = useState(0);
  const [sessionName, setSessionName] = useState("");

  function handleSelectedSession(id) {
    console.log("in handleSelectedSession, id is:", id);
    setSelectedSessionId(id);
    // let s = sessions.find((session) => session.id === id);
    // console.log("sessionData is:", s)
    setSessionData(sessions.find((session) => session.id === id));
    const sName = (sessions.find((session) => session.id === id)).name;
    console.log("session Name is:", sName)
    setSessionName(sName);
  }

  useEffect(() => {
    async function fetchSessions() {
      const res = await handleRequest(sessionsEnpoint, "POST", {
        user_id: user.id,
      });
      console.log("sessions are:", res);
      setSessions(res);
    }
    fetchSessions();
  }, []);

  useEffect(
    function () {
      async function fetchSessionResults() {
        const res = await handleRequest(shotResultEndpoint, "POST", {
          session_id: selectedSessionId,
        });
        console.log("sessionData result res is:", res);
        console.log("res[0].best_frame_path is:", res[0].best_frame_path);
        setSessionData(res);
      }
      // console.log("session_id in SessionResultsTable is:", sessionId);
      if (selectedSessionId) fetchSessionResults();
    },
    [selectedSessionId]
  );

  return (
    <>
      <SessionsDropdown
        sessionId={selectedSessionId}
        sessions={sessions}
        setSessionId={handleSelectedSession}
        user_role={user.role}
      />

      {sessionData[0] === false ? (
        <Typography
          sx={{
            mt: 4,
            p: 2,
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
            textAlign: "center",
            fontSize: "1rem",
            color: "#555",
          }}
        >
          No performance video has been uploaded for the selected session yet.
          Please check back later once the video is available.
        </Typography>
      ) : (
        selectedSessionId &&
        sessionData.length > 0 && (
          <StatisticsTabs
            sessionData={sessionData}
            best_frame_path={sessionData[currentShotIndex].best_frame_path}
            currentIndex={currentShotIndex}
            setCurrentIndex={setCurrentShotIndex}
            shotName={sessionName}
          />
        )
      )}
    </>
  );
}

function SessionsDropdown({ sessionId, sessions, setSessionId, user_role }) {
  return (
    <Box sx={{ minWidth: 500, mt: 1 }}>
      <FormControl fullWidth sx={{ mt: 0 }}>
        <InputLabel>Select Session</InputLabel>
        <Select
          sx={{ padding: 2 }}
          value={sessionId}
          label="Select Session"
          onChange={(e) => setSessionId(e.target.value)}
        >
          {sessions.map((session) => (
            <MenuItem
              key={session.id}
              value={session.id}
              sx={{ border: 2, margin: 2 }}
            >
              <Box>
                <Typography variant="h6">
                  Session Name: {session.name}
                </Typography>
                <Typography variant="body2">Date: {session.date}</Typography>
                <Typography variant="body2">From: {session.from}</Typography>
                <Typography variant="body2">To: {session.to}</Typography>
                {user_role === "player" ? (
                  <Typography variant="body2">
                    Coach: {session.coach}
                  </Typography>
                ) : (
                  <Typography variant="body2">
                    Player: {session.player}
                  </Typography>
                )}
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}

function StatisticsTabs({
  sessionData,
  best_frame_path,
  currentIndex,
  setCurrentIndex,
  shotName,
}) {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  console.log("sessionData is:", sessionData);

  return (
    <>
      <Tabs
        value={value}
        onChange={handleChange}
        aria-label="icon label tabs example"
        sx={{ border: 1, mt: 1, padding: 1 }}
      >
        <Tab icon={<AssessmentIcon />} label="Angle Results" />
        <Tab icon={<ImageIcon />} label="Best Frame" />
        <Tab icon={<VideoIcon />} label="Tutorial" />
      </Tabs>

      {value == 0 ? (
        <SessionResultsTable
          sessionData={sessionData}
          currentIndex={currentIndex}
          setCurrentIndex={setCurrentIndex}
        />
      ) : (
        ""
      )}
      {value == 1 ? <DisplayBestFrame path={best_frame_path} /> : ""}
      {value == 2 ? <FeedbackVideo path={`/videos/${shotName}.mp4`} /> : ""}
    </>
  );
}

function SessionResultsTable({ sessionData, currentIndex, setCurrentIndex }) {
  return (
    <>
      {sessionData.length > 0 ? (
        <AngleComparisonTable
          data={sessionData}
          currentIndex={currentIndex}
          setCurrentIndex={setCurrentIndex}
        />
      ) : (
        "Waiting for results"
      )}
    </>
  );
}

function AngleComparisonTable({ data, currentIndex, setCurrentIndex }) {
  const current = data[currentIndex];

  // Angle names & mapping
  const angleFields = [
    {
      name: "Wrist Angle",
      playerValue: current.wrist_angle,
      idealFrom: current.ideal_wrist_angle_from,
      idealTo: current.ideal_wrist_angle_to,
    },
    {
      name: "Elbow Angle",
      playerValue: current.elbow_angle,
      idealFrom: current.ideal_elbow_angle_from,
      idealTo: current.ideal_elbow_angle_to,
    },
    {
      name: "Shoulder Inclination",
      playerValue: current.shoulder_inclination,
      idealFrom: current.ideal_shoulder_inclination_from,
      idealTo: current.ideal_shoulder_inclination_to,
    },
    {
      name: "Hip Angle",
      playerValue: current.hip_angle, // optional, only if included
      idealFrom: current.ideal_hip_angle_from,
      idealTo: current.ideal_hip_angle_to,
    },
    {
      name: "Knee Angle",
      playerValue: current.knee_angle,
      idealFrom: current.ideal_knee_angle_from,
      idealTo: current.ideal_knee_angle_to,
    },
    {
      name: "Bat-Hip Distance",
      playerValue: current.bat_hip_distance,
      idealFrom: current.ideal_bat_hip_distance_from,
      idealTo: current.ideal_bat_hip_distance_to,
    },
  ];

  // Handle correctness
  const isCorrect = (angleName) =>
    current.correct_angles?.toLowerCase().includes(angleName.toLowerCase());

  return (
    <Box sx={{ mt: 0 }}>
      <Typography variant="h6" gutterBottom>
        Shot ID: {current.id} –{" "}
        <span style={{ color: current.is_shot_correct ? "green" : "red" }}>
          {current.is_shot_correct ? "Correct Shot" : "Incorrect Shot"}
        </span>
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead sx={{ backgroundColor: "#f5f5f5" }}>
            <TableRow>
              <TableCell>
                <strong>Angle Name</strong>
              </TableCell>
              <TableCell>
                <strong>Player's Angle</strong>
              </TableCell>
              <TableCell>
                <strong>Ideal Range</strong>
              </TableCell>
              <TableCell>
                <strong>Correct?</strong>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {angleFields.map((angle, idx) => (
              <TableRow key={idx}>
                <TableCell content="center">{angle.name}</TableCell>
                <TableCell content="center">
                  {angle.playerValue ?? "-"}
                </TableCell>
                <TableCell content="center">
                  {angle.idealFrom} – {angle.idealTo}
                </TableCell>
                <TableCell content="center">
                  <Typography color={isCorrect(angle.name) ? "green" : "red"}>
                    {isCorrect(angle.name) ? "Yes" : "No"}
                  </Typography>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Navigation */}
      <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
        <Button
          variant="outlined"
          onClick={() => setCurrentIndex((i) => Math.max(i - 1, 0))}
          disabled={currentIndex === 0}
        >
          Previous
        </Button>
        <Button
          variant="outlined"
          onClick={() =>
            setCurrentIndex((i) => Math.min(i + 1, data.length - 1))
          }
          disabled={currentIndex === data.length - 1}
        >
          Next
        </Button>
      </Box>
    </Box>
  );
}

function DisplayBestFrame({ path }) {
  console.log("in DisplayBestFrame, path is:", path);
  return (
    <Box sx={{ mt: 2, textAlign: "center" }}>
      <img
        src={path}
        alt="Best Frame"
        style={{ maxWidth: "100%", height: "auto", borderRadius: 8 }}
      />
      <Typography variant="body1" sx={{ mt: 1 }}>
        Best Frame from the Shot
      </Typography>
    </Box>
  );
}

function FeedbackVideo({ path }) {
  return (
    <Box sx={{ mt: 2, textAlign: "center" }}>
      <video width="640" height="360" controls muted>
        <source src={path} type="video/mp4" />
      </video>
      <Typography sx={{ mt: 1 }}>Coach Feedback Video</Typography>
    </Box>
  );
}
