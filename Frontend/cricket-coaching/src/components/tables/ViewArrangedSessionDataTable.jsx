import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Box,
} from "@mui/material";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from "@mui/material";
import handleRequest from "../../utils/handleRequest";

const ViewArrangedSessions = ({ endpoint, user_id, role }) => {
  const [angleResults, setAngleResults] = useState([])
  const [sessions, setSessions] = useState([]);
  console.log("user_id is:", user_id);
  const fetchSessions = async () => {
    try {
      const response = await handleRequest(endpoint, "POST", user_id);
      console.log("response from handle handleRequest is:", response);
      setSessions(response);
    } catch (error) {
      alert("error is while fetching response is:", error);
      console.error("Error fetching sessions:", error);
    }
  };

  const handleUpload = (sessionId, sessionName) => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "video/*";
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      // show progress, then upload to server
      console.log("file is:", file);
      console.log("session_Name in ViewArrangedSessions is:", sessionName);
      try {
        const response = await handleRequest(
          "http://localhost:5000/coach/process_video",
          "UPLOAD",
          { file, session_id: sessionId, shot_name: sessionName }
        );
        // setAngleResults(response)
        // {
        //   angleResults && angleResults.length > 0 && (
        //     <ResultTable results={angleResults} />
        //   );
        // }
        console.log("response from handle handleRequest is:", response);
        alert("Upload successful!");
        

        // optionally update session status to 'uploaded'
      } catch (err) {
        console.error(err);
        alert("Upload failed!");
      }
    };
    input.click();
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <Box sx={{ padding: 4 }}>
      <Typography
        variant="h5"
        sx={{ fontWeight: "bold", textAlign: "center", mb: 4 }}
      >
        Arranged Training Sessions
      </Typography>

      <Grid container spacing={3}>
        {sessions && sessions.length > 0 ? (
          sessions.map((session, index) => (
            <Grid item xs={12} sm={6} md={4} key={session.id}>
              <Card
                sx={{
                  backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
                  boxShadow: 3,
                  borderRadius: 2,
                  transition: "0.3s",
                  "&:hover": {
                    boxShadow: 6,
                    backgroundColor: "#e3f2fd",
                  },
                }}
              >
                <CardContent>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: "bold", mb: 1 }}
                    gutterBottom
                  >
                    {session.name}
                  </Typography>

                  <Typography variant="body2">
                    <strong>ID:</strong> {session.id}
                  </Typography>
                  <Typography variant="body2">
                    <strong>{role === "coach" ? "Player" : "Coach"}:</strong>{" "}
                    {role === "coach" ? session.player : session.coach}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Date:</strong> {session.date}
                  </Typography>
                  <Typography variant="body2">
                    <strong>From:</strong> {session.from}
                  </Typography>
                  <Typography variant="body2">
                    <strong>To:</strong> {session.to}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    <strong>Venue:</strong> {session.venue}
                  </Typography>

                  {/* You can add status indicator if needed */}
                  {/* <Chip label="Analyzed" color="success" /> */}

                  <Box display="flex" flexDirection="column" gap={1}>
                    <Button
                      variant="contained"
                      sx={{
                        bgcolor: "black",
                        color: "white",
                        "&:hover": { backgroundColor: "green" },
                      }}
                      onClick={() => handleUpload(session.id, session.name)}
                    >
                      Upload
                    </Button>
                    <Button
                      variant="contained"
                      sx={{
                        bgcolor: "black",
                        color: "white",
                        "&:hover": { backgroundColor: "green" },
                      }}
                    >
                      Record
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Typography variant="body1" sx={{ textAlign: "center", mt: 5 }}>
            No Sessions Available
          </Typography>
        )}
      </Grid>
    </Box>
  );
};

const ResultTable = ({ results }) => {
  return (
    <TableContainer
      component={Paper}
      elevation={2}
      sx={{ mt: 2, borderRadius: 2 }}
    >
      <Table>
        <TableHead sx={{ backgroundColor: "#1976d2" }}>
          <TableRow>
            <TableCell sx={{ color: "white", fontWeight: "bold" }}>
              Parameter
            </TableCell>
            <TableCell sx={{ color: "white", fontWeight: "bold" }}>
              Ideal Range
            </TableCell>
            <TableCell sx={{ color: "white", fontWeight: "bold" }}>
              Player Value
            </TableCell>
            <TableCell sx={{ color: "white", fontWeight: "bold" }}>
              Result
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.map((res, index) => {
            const [param] = Object.keys(res).filter((k) =>
              k.includes("Player")
            );
            const paramName = param.replace("Player ", "");

            const idealFrom =
              res[`${paramName} Ideal Angle From`] ||
              res[`${paramName} Ideal From`] ||
              "—";
            const idealTo =
              res[`${paramName} Ideal Angle To`] ||
              res[`${paramName} Ideal To`] ||
              "—";

            return (
              <TableRow
                key={index}
                sx={{
                  backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
                }}
              >
                <TableCell>{paramName}</TableCell>
                <TableCell>
                  {idealFrom} - {idealTo}
                </TableCell>
                <TableCell>{res[param]}</TableCell>
                <TableCell>
                  <Chip
                    label={res.is_shot_correct ? "Correct" : "Incorrect"}
                    color={res.is_shot_correct ? "success" : "error"}
                    size="small"
                    sx={{ fontWeight: "bold" }}
                  />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
export default ViewArrangedSessions;
