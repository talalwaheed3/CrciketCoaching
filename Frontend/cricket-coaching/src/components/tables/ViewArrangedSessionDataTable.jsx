import { useState, useEffect, useContext } from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Box,
  List,
  ListItem,
} from "@mui/material";
import handleRequest from "../../utils/handleRequest";
import MiniLoaderPopup from "../Loader";
import AuthContext from "../auth/AuthContext";

const ViewArrangedSessions = ({ endpoint, user_id, role }) => {
  const { user } = useContext(AuthContext);
  const [sessions, setSessions] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [apiResponse, setApiResponse] = useState([]);
  const [showResults, setShowResults] = useState(false);

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

      console.log("file is:", file);
      console.log("session_Name in ViewArrangedSessions is:", sessionName);
      try {
        setIsUploading(true);
        const response = await handleRequest("/coach/process_video", "UPLOAD", {
          file,
          session_id: sessionId,
          shot_name: sessionName,
          coach_id: user.id,
        });
        console.log("response is:", response);
        setApiResponse(response);

        console.log("response from handle handleRequest is:", response);
        if (response) {
          alert("Upload successful!");
        }
      } catch (err) {
        console.error(err);
        alert("Upload failed! Error is:", err);
      } finally {
        setIsUploading(false);
        setShowResults(true);
      }
    };
    input.click();
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <>
      <Box sx={{ padding: 4 }}>
        <Typography
          variant="h5"
          sx={{ fontWeight: "bold", textAlign: "center", mb: 4 }}
        >
          Arranged Training Sessions
        </Typography>

        <Grid container spacing={sessions.length < 3 ? 25 : 3}>
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
                    width: 300,
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

                    {role === "coach" && (
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
                        {isUploading ? <MiniLoaderPopup /> : ""}
                        {/* {showResults ? (
                          <MiniResultPopup
                            results={apiResponse}
                            onClose={() => setShowResults(false)}
                          />
                        ) : (
                          ""
                        )} */}
                      </Box>
                    )}
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
    </>
  );
};

function MiniResultPopup({ results = [], onClose }) {
  return (
    <Box
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        bgcolor: "rgba(0, 0, 0, 0.3)",
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Card
        sx={{
          width: 400,
          maxHeight: "60vh",
          overflowY: "auto",
          padding: 2,
          boxShadow: 3,
          borderRadius: 2,
          textAlign: "left",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ textAlign: "center" }}>
            ✅ Video Upload Results
          </Typography>

          <List dense>
            {results["Result"].map((res, index) => (
              <ListItem key={index} sx={{ mb: 1 }}>
                <Typography variant="body2" sx={{ color: "#4caf50" }}>
                  {Object.values(res)[0]}
                </Typography>
              </ListItem>
            ))}
          </List>

          <Button
            sx={{
              display: "block",
              mt: 2,
              textAlign: "center",
              color: "white",
              fontStyle: "italic",
              backgroundColor: "red",
            }}
            onClick={onClose}
          >
            Close
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}

export default ViewArrangedSessions;
