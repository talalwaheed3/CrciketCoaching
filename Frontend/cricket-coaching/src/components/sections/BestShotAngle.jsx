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
  Card,
  Fab,
} from "@mui/material";

import ImageIcon from "@mui/icons-material/Image";
import { VideoIcon } from "lucide-react";
import { Funnel } from "lucide-react";
import AssessmentIcon from "@mui/icons-material/Assessment";
import { useContext, useEffect, useState } from "react";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";

export default function BestShotAngle() {
  const { user } = useContext(AuthContext);
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState("");
  const [sessionData, setSessionData] = useState([]);
  const [filteredSessionData, setFilteredSessionData] = useState([]);
  const [currentShotIndex, setCurrentShotIndex] = useState(0);
  const [sessionName, setSessionName] = useState("");
  const [shotCategory, setShotCategory] = useState("all");
  const [showBestFramePathTab, setShowBestFramePathTab] = useState(false);
  const [bestFrame, setBestFrame] = useState("");

  function handleSelectedSession(id) {
    console.log("in handleSelectedSession, id is:", id);
    setSelectedSessionId(id);
    // let s = sessions.find((session) => session.id === id);
    // console.log("sessionData is:", s)
    setSessionData(sessions.find((session) => session.id === id));
    const sName = sessions.find((session) => session.id === id).name;
    console.log("session Name is:", sName);
    setSessionName(sName);
  }

  function handleBestTab() {
    setShowBestFramePathTab(!showBestFramePathTab);
  }

  useEffect(() => {
    async function fetchSessions() {
      const res = await handleRequest("/coach/get_arranged_sessions", "POST", {
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
        const res = await handleRequest("/coach/get_shot_result", "POST", {
          session_id: selectedSessionId,
          coach_id: user.id,
        });
        console.log("sessionData result res is:", res);
        console.log("res[0].best_frame_path is:", res[0]?.best_frame_path);
        setSessionData(res);
        setFilteredSessionData(res);
      }
      // console.log("session_id in SessionResultsTable is:", sessionId);
      if (selectedSessionId) fetchSessionResults();
    },
    [selectedSessionId]
  );

  useEffect(
    function () {
      if (sessionData.length > 0) {
        console.log("True here");
        if (shotCategory === "all") {
          setFilteredSessionData(sessionData);
        } else {
          console.log(
            'sessionData.filter((data) => data.correct_angles.split[","].length === shotCategory) is:',
            sessionData.filter(
              (data) => data.correct_angles.split(",").length === shotCategory
            )
          );
          setFilteredSessionData(
            sessionData.filter(
              (data) => data.correct_angles.split(",").length === shotCategory
            )
          );
        }
      }
    },
    [sessionData, shotCategory]
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
          <>
            {/* <BestToWorstShotsTab
              shotCategory={shotCategory}
              setShotCategory={handleShotCategory}
            /> */}

            {filteredSessionData.length > 0 ? (
              <StatisticsTabs
                sessionData={filteredSessionData}
                best_frame_path={bestFrame}
                setBestFramePath={setBestFrame}
                bestFrameTab={showBestFramePathTab}
                setTab={handleBestTab}
                currentIndex={currentShotIndex}
                setCurrentIndex={setCurrentShotIndex}
                shotName={sessionName}
              />
            ) : (
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
                There is not any shot of this player where only {shotCategory}{" "}
                shots are correct.
              </Typography>
            )}
          </>
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
  setBestFramePath,
  bestFrameTab,
  setTab,
  currentIndex,
  setCurrentIndex,
  shotName,
}) {
  const [value, setValue] = useState(0);
  console.log("bestFrameTab is:", bestFrameTab);

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
        {bestFrameTab ? <Tab icon={<ImageIcon />} label="Best Frame" /> : ""}
        {/* <Tab icon={<VideoIcon />} label="Tutorial" /> */}
      </Tabs>

      {value == 0 ? (
        <SessionResultsTable
          setTab={setTab}
          setBestFramePath={setBestFramePath}
          sessionData={sessionData}
          currentIndex={currentIndex}
          setCurrentIndex={setCurrentIndex}
        />
      ) : (
        ""
      )}
      {value == 1 ? <DisplayBestFrame path={best_frame_path || 0} /> : ""}
      {/* {value == 2 ? <FeedbackVideo path={`/videos/${shotName}.mp4`} /> : ""} */}
    </>
  );
}

// function BestToWorstShotsTab({ shotCategory, setShotCategory }) {
//   return (
//     <Tabs
//       value={shotCategory}
//       onChange={setShotCategory}
//       aria-label="icon label tabs example"
//       sx={{ border: 1, mt: 1, padding: 1 }}
//     >
//       <Tab value="all" label="All" />
//       <Tab value={0} label="Worst" />
//       <Tab value={1} label="Very Poor" />
//       <Tab value={2} label="Poor" />
//       <Tab value={3} label="Average" />
//       <Tab value={4} label="Good" />
//       <Tab value={5} label="Very Good" />
//       <Tab value={6} label="Best" />
//     </Tabs>
//   );
// }

const angleNamesWithId = [
  {
    3: "wrist angle",
  },
  { 1: "elbow angle" },
  { 2: "shoulder inclination" },
  { 4: "hip angle" },
  { 5: "knee angle" },
  { 6: "bat and hip distance" },
];

function SessionResultsTable({
  setTab,
  setBestFramePath,
  sessionData,
  currentIndex,
  setCurrentIndex,
}) {
  // const [showBestFrame, setShowBestFrame] = useState(false);
  const [bestShotAnglePath, setBestShotAnglePath] = useState("");

  function handleShowingBestFrame(angleName) {
    // setSelectedAngleId(angleId);
    console.log("angleName is:", angleName);
    // setShowBestFrame(!showBestFrame);
    setTab(true);
    let s =
      sessionData.find((session) => {
        let correct_angles = session["correct_angles"].split(",");
        for (let index = 0; index < correct_angles.length; index++) {
          const angle = correct_angles[index];
          console.log("angle is:", angle);
          if (angleName === angle.toLowerCase()) {
            return session;
          }
        }
      }) || "";
    console.log("s is:", s);
    const path = s.best_frame_path;
    console.log("path is:", path);
    setBestShotAnglePath(path);
    setBestFramePath(path);
  }
  return (
    <>
      {sessionData.length > 0 ? (
        <AngleComparisonTable
          data={sessionData}
          currentIndex={currentIndex}
          setCurrentIndex={setCurrentIndex}
          setShowingBestFrame={handleShowingBestFrame}
        />
      ) : (
        "Waiting for results"
      )}

      {/* {bestShotAnglePath === <DisplayBestFrame path={0} /> ? (
        ""
      ) : (
        <DisplayBestFrame path={bestShotAnglePath} />
      )} */}
    </>
  );
}

function AngleComparisonTable({
  data,
  currentIndex,
  setCurrentIndex,
  setShowingBestFrame,
}) {
  const current = data[currentIndex];

  // Angle names & mapping
  const angleFields = [
    {
      id: 3,
      name: "Wrist Angle",
      playerValue: current.wrist_angle,
      idealFrom: current.ideal_wrist_angle_from,
      idealTo: current.ideal_wrist_angle_to,
    },
    {
      id: 1,
      name: "Elbow Angle",
      playerValue: current.elbow_angle,
      idealFrom: current.ideal_elbow_angle_from,
      idealTo: current.ideal_elbow_angle_to,
    },
    {
      id: 2,
      name: "Shoulder Inclination",
      playerValue: current.shoulder_inclination,
      idealFrom: current.ideal_shoulder_inclination_from,
      idealTo: current.ideal_shoulder_inclination_to,
    },
    {
      id: 4,
      name: "Hip Angle",
      playerValue: current.hip_angle, // optional, only if included
      idealFrom: current.ideal_hip_angle_from,
      idealTo: current.ideal_hip_angle_to,
    },
    {
      id: 5,
      name: "Knee Angle",
      playerValue: current.knee_angle,
      idealFrom: current.ideal_knee_angle_from,
      idealTo: current.ideal_knee_angle_to,
    },
    {
      id: 6,
      name: "Bat and Hip Distance",
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
      <Card sx={{ display: "flex" }}>
        <Typography variant="h6" gutterBottom>
          Shot ID: {current.id} –{" "}
          <span style={{ color: current.is_shot_correct ? "green" : "red" }}>
            {current.is_shot_correct ? "Correct Shot" : "Incorrect Shot"}
          </span>
        </Typography>
        <Typography variant="h6" gutterBottom sx={{ ml: 16 }}>
          Total Shots: {data.length}
        </Typography>
      </Card>

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
              <TableCell>
                <strong>Action</strong>
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
                <TableCell content="center">
                  <Button
                    variant="outlined"
                    onClick={() =>
                      setShowingBestFrame(angle.name.toLowerCase())
                    }
                  >
                    Best
                  </Button>
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
    <>
      {path !== 0 ? (
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
      ) : (
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
          No Best Shot available for this angle
        </Typography>
      )}
    </>
  );
}
