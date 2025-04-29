// import { useState, useEffect } from "react";
// import {
//   Box,
//   Typography,
//   Grid,
//   Card,
//   CardContent,
//   Select,
//   MenuItem,
//   FormControl,
//   InputLabel,
//   Table,
//   TableBody,
//   TableCell,
//   TableContainer,
//   TableHead,
//   TableRow,
//   Paper,
//   Chip,
// } from "@mui/material";
// import handleRequest from "../../utils/handleRequest";

// const SessionResultsTable = ({ endpoint }) => {
//   const [sessions, setSessions] = useState([]);
//   const [selectedSessionId, setSelectedSessionId] = useState("");
//   const [shotsResults, setShotsResults] = useState([]);

//   const fetchSessions = async () => {
//     try {
//       const response = await handleRequest(endpoint, "POST");
//       console.log("Fetched sessions:", response);
//       setSessions(response);
//     } catch (error) {
//       console.error("Error fetching sessions:", error);
//       alert("Error fetching sessions");
//     }
//   };

//   const fetchSessionResults = async (sessionId) => {
//     try {
//       const response = await handleRequest(
//         "http://localhost:5000/coach/get_session_results",
//         "POST",
//         { session_id: sessionId }
//       );
//       console.log("Fetched session results:", response);
//       setShotsResults(response); // response should be an array of shots
//     } catch (error) {
//       console.error("Error fetching session results:", error);
//       alert("Error fetching session results");
//     }
//   };

//   useEffect(() => {
//     fetchSessions();
//   }, []);

//   const handleSessionChange = (event) => {
//     const sessionId = event.target.value;
//     setSelectedSessionId(sessionId);
//     fetchSessionResults(sessionId);
//   };

//   return (
//     <Box sx={{ padding: 4 }}>
//       <Typography
//         variant="h5"
//         sx={{ fontWeight: "bold", textAlign: "center", mb: 4 }}
//       >
//         Session Results
//       </Typography>

//       {/* Session Selector */}
//       <FormControl fullWidth sx={{ mb: 4 }}>
//         <InputLabel>Select Session</InputLabel>
//         <Select
//           value={selectedSessionId}
//           label="Select Session"
//           onChange={handleSessionChange}
//         >
//           {sessions.map((session) => (
//             <MenuItem key={session.id} value={session.id}>
//               {session.name} - {session.date}
//             </MenuItem>
//           ))}
//         </Select>
//       </FormControl>

//       {/* Show Session Info */}
//       {selectedSessionId && (
//         <Box sx={{ mb: 4 }}>
//           {sessions
//             .filter((session) => session.id === selectedSessionId)
//             .map((session) => (
//               <Card
//                 key={session.id}
//                 sx={{
//                   backgroundColor: "#f9f9f9",
//                   boxShadow: 3,
//                   borderRadius: 2,
//                   p: 2,
//                 }}
//               >
//                 <CardContent>
//                   <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
//                     {session.name} - {session.date}
//                   </Typography>
//                   <Grid container spacing={2}>
//                     <Grid item xs={12} sm={6}>
//                       <Typography variant="body2">
//                         <strong>From:</strong> {session.from}
//                       </Typography>
//                       <Typography variant="body2">
//                         <strong>To:</strong> {session.to}
//                       </Typography>
//                     </Grid>
//                     <Grid item xs={12} sm={6}>
//                       <Typography variant="body2">
//                         <strong>Venue:</strong> {session.venue}
//                       </Typography>
//                     </Grid>
//                   </Grid>
//                 </CardContent>
//               </Card>
//             ))}
//         </Box>
//       )}

//       {/* Display shots results */}
//       {shotsResults && shotsResults.length > 0 ? (
//         <Grid container spacing={3}>
//           {shotsResults.map((shot, shotIndex) => (
//             <Grid item xs={12} key={shotIndex}>
//               <Card
//                 sx={{
//                   backgroundColor: "#ffffff",
//                   boxShadow: 3,
//                   borderRadius: 2,
//                   p: 2,
//                   transition: "0.3s",
//                   "&:hover": {
//                     backgroundColor: "#e3f2fd",
//                   },
//                 }}
//               >
//                 <CardContent>
//                   <Typography
//                     variant="h6"
//                     sx={{ fontWeight: "bold", mb: 2 }}
//                   >
//                     Shot {shotIndex + 1}
//                   </Typography>

//                   <ResultTable results={shot} />
//                 </CardContent>
//               </Card>
//             </Grid>
//           ))}
//         </Grid>
//       ) : selectedSessionId ? (
//         <Typography
//           variant="body1"
//           sx={{ textAlign: "center", mt: 5, fontStyle: "italic" }}
//         >
//           No results available for this session.
//         </Typography>
//       ) : null}
//     </Box>
//   );
// };

// const ResultTable = ({ results }) => {
//   return (
//     <TableContainer
//       component={Paper}
//       elevation={2}
//       sx={{ borderRadius: 2 }}
//     >
//       <Table>
//         <TableHead sx={{ backgroundColor: "#1976d2" }}>
//           <TableRow>
//             <TableCell sx={{ color: "white", fontWeight: "bold" }}>
//               Parameter
//             </TableCell>
//             <TableCell sx={{ color: "white", fontWeight: "bold" }}>
//               Ideal Range
//             </TableCell>
//             <TableCell sx={{ color: "white", fontWeight: "bold" }}>
//               Player Value
//             </TableCell>
//             <TableCell sx={{ color: "white", fontWeight: "bold" }}>
//               Result
//             </TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {results.map((res, index) => {
//             const [param] = Object.keys(res).filter((k) =>
//               k.includes("Player")
//             );
//             const paramName = param.replace("Player ", "");

//             const idealFrom =
//               res[`${paramName} Ideal Angle From`] ||
//               res[`${paramName} Ideal From`] ||
//               "—";
//             const idealTo =
//               res[`${paramName} Ideal Angle To`] ||
//               res[`${paramName} Ideal To`] ||
//               "—";

//             return (
//               <TableRow
//                 key={index}
//                 sx={{
//                   backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
//                 }}
//               >
//                 <TableCell>{paramName}</TableCell>
//                 <TableCell>
//                   {idealFrom} - {idealTo}
//                 </TableCell>
//                 <TableCell>{res[param]}</TableCell>
//                 <TableCell>
//                   <Chip
//                     label={res.is_shot_correct ? "Correct" : "Incorrect"}
//                     color={res.is_shot_correct ? "success" : "error"}
//                     size="small"
//                     sx={{ fontWeight: "bold" }}
//                   />
//                 </TableCell>
//               </TableRow>
//             );
//           })}
//         </TableBody>
//       </Table>
//     </TableContainer>
//   );
// };

// export default SessionResultsTable;

import { useState } from "react";
import "./SessionResults.css"; // We'll add some styling separately

const sessionsData = [
  {
    sessionName: "Cover Drive",
    date: "2025-04-25",
    venue: "Cricket Ground A",
    shots: [
      [
        {
          "Elbow Ideal Angle From": 90,
          "Elbow Ideal Angle To": 120,
          "Player Elbow Angle": 157,
          is_shot_correct: false,
        },
        {
          "Player Shoulder Inclination": 64,
          "Shoulder Inclination Ideal From": 60,
          "Shoulder Inclination Ideal To": 90,
          is_shot_correct: true,
        },
        {
          "Player Wrist Angle": 90,
          "Wrist Ideal Angle From": 120,
          "Wrist Ideal Angle To": 150,
          is_shot_correct: false,
        },
        {
          "Hip Ideal Angle From": 125,
          "Hip Ideal Angle To": 155,
          "Player Hip Angle": 141,
          is_shot_correct: true,
        },
        {
          "Knee Ideal Angle From": 100,
          "Knee Ideal Angle To": 140,
          "Player Knee Angle": 161,
          is_shot_correct: false,
        },
        {
          "Bat-Hip Distance Ideal From": 40,
          "Bat-Hip Distance Ideal To": 60,
          "Player Bat-Hip Distance": 127,
          is_shot_correct: false,
        },
      ],
      // You can have more shots inside this array
    ],
  },
  // more sessions...
];

export default function SessionResultsTable({ endpoint }) {
  const [selectedSessionIndex, setSelectedSessionIndex] = useState(0);

  const session = sessionsData[selectedSessionIndex];

  return (
    <div className="session-results">
      {/* Dropdown to select session */}
      <select
        className="session-dropdown"
        value={selectedSessionIndex}
        onChange={(e) => setSelectedSessionIndex(Number(e.target.value))}
      >
        {sessionsData.map((s, index) => (
          <option key={index} value={index}>
            {s.sessionName}
          </option>
        ))}
      </select>

      {/* Session info */}
      <div className="session-info">
        <p>
          <strong>Session:</strong> {session.sessionName}
        </p>
        <p>
          <strong>Date:</strong> {session.date}
        </p>
        <p>
          <strong>Venue:</strong> {session.venue}
        </p>
      </div>

      {/* Shots results */}
      <div className="shots-section">
        {session.shots.map((shot, shotIndex) => (
          <div key={shotIndex} className="shot-block">
            <table className="results-table">
              <thead>
                <tr>
                  <th>Angle Name</th>
                  <th>Player's Angle</th>
                  <th>Ideal Range</th>
                  <th>Correct?</th>
                </tr>
              </thead>
              <tbody>
                {shot.map((res, resIndex) => (
                  <tr key={resIndex}>
                    <td>{getParameterName(res)}</td>
                    <td>{getPlayerValue(res)}</td>
                    <td>{getIdealRange(res)}</td>
                    <td className={res.is_shot_correct ? "correct" : "wrong"}>
                      {res.is_shot_correct ? "✅" : "❌"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}

// Helper functions
function getParameterName(res) {
  if (res["Player Elbow Angle"] !== undefined) return "Elbow Angle";
  if (res["Player Shoulder Inclination"] !== undefined)
    return "Shoulder Inclination";
  if (res["Player Wrist Angle"] !== undefined) return "Wrist Angle";
  if (res["Player Hip Angle"] !== undefined) return "Hip Angle";
  if (res["Player Knee Angle"] !== undefined) return "Knee Angle";
  if (res["Player Bat-Hip Distance"] !== undefined) return "Bat-Hip Distance";
  return "Unknown";
}

function getPlayerValue(res) {
  return (
    res["Player Elbow Angle"] ||
    res["Player Shoulder Inclination"] ||
    res["Player Wrist Angle"] ||
    res["Player Hip Angle"] ||
    res["Player Knee Angle"] ||
    res["Player Bat-Hip Distance"]
  );
}

function getIdealRange(res) {
  return (
    (res["Elbow Ideal Angle From"] &&
      res["Elbow Ideal Angle To"] &&
      `${res["Elbow Ideal Angle From"]} - ${res["Elbow Ideal Angle To"]}`) ||
    (res["Shoulder Inclination Ideal From"] &&
      res["Shoulder Inclination Ideal To"] &&
      `${res["Shoulder Inclination Ideal From"]} - ${res["Shoulder Inclination Ideal To"]}`) ||
    (res["Wrist Ideal Angle From"] &&
      res["Wrist Ideal Angle To"] &&
      `${res["Wrist Ideal Angle From"]} - ${res["Wrist Ideal Angle To"]}`) ||
    (res["Hip Ideal Angle From"] &&
      res["Hip Ideal Angle To"] &&
      `${res["Hip Ideal Angle From"]} - ${res["Hip Ideal Angle To"]}`) ||
    (res["Knee Ideal Angle From"] &&
      res["Knee Ideal Angle To"] &&
      `${res["Knee Ideal Angle From"]} - ${res["Knee Ideal Angle To"]} `) ||
    (res["Bat-Hip Distance Ideal From"] &&
      res["Bat-Hip Distance Ideal To"] &&
      `${res["Bat-Hip Distance Ideal From"]} - ${res["Bat-Hip Distance Ideal To"]} `)
  );
}
