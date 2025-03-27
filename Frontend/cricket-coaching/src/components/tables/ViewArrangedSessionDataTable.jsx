import { useState, useEffect } from "react";
import {
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";
import handleRequest from "../../utils/handleRequest";

const ViewArrangedSessions = ({ endpoint, role }) => {
  const [sessions, setSessions] = useState([]);

  const fetchSessions = async () => {
    try {
      const response = await handleRequest(endpoint, "POST", role);
      console.log("response from handle handleRequest is:", response);
      setSessions(response);
    } catch (error) {
      alert("error is while fetching response is:", error);
      console.error("Error fetching sessions:", error);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <Card sx={{ p: 3, m: "200px 150px 0px 0px", maxWidth: "100%", overflowX: "auto" }}>
      <Typography
        variant="h6"
        sx={{ mb: 0, fontWeight: "bold", textAlign: "center" }}
      >
        Arranged Training Sessions
      </Typography>

      <TableContainer
        component={Paper}
        sx={{ maxHeight: "500px", overflow: "auto" }}
      >
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#1976d2" }}>
              {[
                "ID",
                "Session Name",
                "Player Name",
                "Date",
                "Session From",
                "Session To",
                "Venue",
              ].map((header) => (
                <TableCell
                  key={header}
                  sx={{
                    fontWeight: "bold",
                    color: "white",
                    textAlign: "center",
                  }}
                >
                  {header}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {sessions.length > 0 ? (
              sessions.map((session, index) => (
                <TableRow
                  key={session.id}
                  sx={{
                    backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
                    "&:hover": { backgroundColor: "#e3f2fd" },
                  }}
                >
                  <TableCell>{session.id}</TableCell>
                  <TableCell>{session.name}</TableCell>
                  <TableCell>{session.player}</TableCell>
                  <TableCell>{session.date}</TableCell>
                  <TableCell>{session.from}</TableCell>
                  <TableCell>{session.to}</TableCell>
                  <TableCell sx={{textAlign: 'center'}}>{session.venue}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  No Sessions Available
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Card>
  );
};

export default ViewArrangedSessions;
