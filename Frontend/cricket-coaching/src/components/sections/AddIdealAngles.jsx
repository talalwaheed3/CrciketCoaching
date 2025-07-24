import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  TextField,
  Button,
  Card,
} from "@mui/material";
import { useContext, useEffect, useState } from "react";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";

function AddIdealAngles() {
  const { user } = useContext(AuthContext);
  const [shots, setShots] = useState([]);
  const [selectedShotId, setSelectedShotId] = useState();

  const [elbowAngleFrom, setElbowAngleFrom] = useState();
  const [elbowAngleTo, setElbowAngleTo] = useState();

  const [shoulderInclinationFrom, setShoulderInclinationFrom] = useState();
  const [shoulderInclinationTo, setShoulderInclinationTo] = useState();

  const [wristAngleFrom, setWristAngleFrom] = useState();
  const [wristAngleTo, setWristAngleTo] = useState();

  const [kneeAngleFrom, setKneeAngleFrom] = useState();
  const [kneeAngleTo, setKneeAngleTo] = useState();

  const [hipAngleTo, setHipAngleTo] = useState();
  const [hipAngleFrom, setHipAngleFrom] = useState();

  const [batHipDistanceTo, setBatHipDistanceTo] = useState();
  const [batHipDistanceFrom, setBatHipDistanceFrom] = useState();

  function handleShot(id) {
    setSelectedShotId(id);
  }

  function handleSubmit() {
    const insertIdealAngles = async () => {
      try {
        const response = await handleRequest(
          "/coach/add_ideal_angles",
          "POST",
          {
            coach_id: user.id,
            shot_id: selectedShotId,
            elbow_angle: {
              from: Number(elbowAngleFrom),
              to: Number(elbowAngleTo),
            },
            wrist_angle: {
              from: Number(wristAngleFrom),
              to: Number(wristAngleTo),
            },
            shoulder_inclination: {
              from: Number(shoulderInclinationFrom),
              to: Number(shoulderInclinationTo),
            },
            hip_angle: { from: Number(hipAngleFrom), to: Number(hipAngleTo) },
            knee_angle: {
              from: Number(kneeAngleFrom),
              to: Number(kneeAngleTo),
            },
            bat_hip_distance: {
              from: Number(batHipDistanceFrom),
              to: Number(batHipDistanceTo),
            },
          }
        );
        alert(response);
      } catch (error) {
        console.error("Error while fetching shots:", error);
      }
    };
    insertIdealAngles();
  }

  function handleElbowAngleFrom(value) {
    setElbowAngleFrom(value);
  }

  function handleElbowAngleTo(value) {
    setElbowAngleTo(value);
  }

  function handleWristAngleFrom(value) {
    setWristAngleFrom(value);
  }

  function handleWristAngleTo(value) {
    setWristAngleTo(value);
  }

  function handleKneeAngleFrom(value) {
    setKneeAngleFrom(value);
  }

  function handleKneeAngleTo(value) {
    setKneeAngleTo(value);
  }

  function handleShoulderInclinationFrom(value) {
    setShoulderInclinationFrom(value);
  }

  function handleShoulderInclinationTo(value) {
    setShoulderInclinationTo(value);
  }

  function handleHipAngleFrom(value) {
    setHipAngleFrom(value);
  }

  function handleHipAngleTo(value) {
    setHipAngleTo(value);
  }

  function handleBatHipDistanceFrom(value) {
    setBatHipDistanceFrom(value);
  }

  function handleBatHipDistanceTo(value) {
    setBatHipDistanceTo(value);
  }

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

  return (
    <>
      <ShotDropdown
        shots={shots}
        setShot={handleShot}
        shotId={selectedShotId}
      />

      {selectedShotId ? (
        <Card sx={{ p: 3, maxWidth: 500, margin: "auto", mt: 10 }}>
          <Typography variant="h6" align="center" sx={{ mb: 3 }}>
            Add Ideal Angles
          </Typography>

          <Typography variant="h6">Enter Elbow Angle range:</Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={elbowAngleFrom || ""}
              onChange={(e) => handleElbowAngleFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={elbowAngleTo || ""}
              onChange={(e) => handleElbowAngleTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          <Typography variant="h6">
            Enter Shoulder Inclination range:
          </Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={shoulderInclinationFrom || ""}
              onChange={(e) => handleShoulderInclinationFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={shoulderInclinationTo || ""}
              onChange={(e) => handleShoulderInclinationTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          <Typography variant="h6">Enter Wrist Angle range:</Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={wristAngleFrom || ""}
              onChange={(e) => handleWristAngleFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={wristAngleTo || ""}
              onChange={(e) => handleWristAngleTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          <Typography variant="h6">Enter Hip Angle range:</Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={hipAngleFrom || ""}
              onChange={(e) => handleHipAngleFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={hipAngleTo || ""}
              onChange={(e) => handleHipAngleTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          <Typography variant="h6">Enter Knee Angle range:</Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={kneeAngleFrom || ""}
              onChange={(e) => handleKneeAngleFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={kneeAngleTo || ""}
              onChange={(e) => handleKneeAngleTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          <Typography variant="h6">Enter Bat-Hip Distance range:</Typography>
          <div className="flex">
            <TextField
              fullWidth
              margin="normal"
              label="Angle From:"
              name="angle_from"
              value={batHipDistanceFrom || ""}
              onChange={(e) => handleBatHipDistanceFrom(e.target.value)}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Angle To:"
              name="angle_to"
              value={batHipDistanceTo || ""}
              onChange={(e) => handleBatHipDistanceTo(e.target.value)}
              sx={{ ml: 1 }}
            />
          </div>

          {/* Submit Button */}
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleSubmit}
          >
            Save
          </Button>
        </Card>
      ) : (
        ""
      )}
    </>
  );
}

// function AnglesForm({}) {
//   return (

//   );
// }

function ShotDropdown({ shots, setShot, shotId }) {
  return (
    <Box sx={{ minWidth: 500, mt: 1 }}>
      <FormControl fullWidth sx={{ mt: 0 }}>
        <InputLabel>Select Shot</InputLabel>
        <Select
          sx={{ padding: 2 }}
          value={shotId || ""}
          label="Select Shot"
          onChange={(e) => setShot(e.target.value)}
        >
          {shots.map((shot) => (
            <MenuItem
              key={shot.id}
              value={shot.id}
              sx={{ border: 2, margin: 2 }}
            >
              <Box>
                <Typography variant="h6">{shot.name}</Typography>
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}

export default AddIdealAngles;
