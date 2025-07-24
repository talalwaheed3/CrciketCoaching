import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  FormControlLabel,
} from "@mui/material";
import { useContext, useEffect, useState } from "react";
import handleRequest from "../../utils/handleRequest";
import AuthContext from "../auth/AuthContext";
export default function PlayerPerformance() {
  const { user } = useContext(AuthContext);
  // const [shots, setShots] = useState([]);
  // const [selectedShot, setSelectedShot] = useState("");
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState({});

  // function handleSelectedShot(value) {
  //   setSelectedShot(value);
  // }

  function handleSelectedSession(id) {
    console.log("in handleSelectedSession, id is:", id);
    let s = sessions.filter((session) => session.id === id);
    console.log("s is:", s);
    setSelectedSession(sessions.filter((session) => session.id === id));
  }

  // useEffect(() => {
  //   async function fetchShots() {
  //     const res = await handleRequest("/coach/get_all_shots", "GET");
  //     console.log("shots are:", res);
  //     setShots(res);
  //   }
  //   if (selectedShot) {
  //     console.log("selectedShot is:", selectedShot);
  //   } else {
  //     fetchShots();
  //   }
  // }, [selectedShot]);

  useEffect(() => {
    async function fetchSessions() {
      const res = await handleRequest("/coach/get_arranged_sessions", "POST", {
        coach_id: user.id,
      });
      console.log("sessions are:", res);
      setSessions(res);
    }
    fetchSessions();
  }, []);

  return (
    <Box sx={{ minWidth: 500, mt: 5 }}>
      <FormControl fullWidth sx={{ mt: 2 }}>
        <InputLabel>Select Session</InputLabel>
        <Select
          sx={{ padding: 2 }}
          value={session}
          label="Select Session"
          onChange={(e) => handleSelectedSession(e.target.value)}
        >
          {sessions.map((session) => (
            <MenuItem
              key={session.id}
              value={session.id}
              sx={{ border: 2, margin: 2 }}
            >
              <FormControlLabel
                value={session.id}
                control={<Box />}
                label={
                  <>
                    <Typography variant="h6">
                      Session Name: {session.name}
                    </Typography>
                    <Typography variant="body2">
                      Date: {session.date}
                    </Typography>
                    <Typography variant="body2">
                      From: {session.from}
                    </Typography>
                    <Typography variant="body2">To: {session.to}</Typography>
                    <Typography variant="body2">
                      Player: {session.player}
                    </Typography>
                  </>
                }
              />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>

    // <Box sx={{ minWidth: 500, mt: 5 }}>
    //   {/* <Dropdown
    //     selectedValue={selectedShot}
    //     values={shots}
    //     setSelectedValue={handleSelectedShot}
    //     label="Select Shot"
    //     marginTop={0}
    //   /> */}
    //   {/* {sessions ? <Dropdown
    //     selectedValue={selectedSession.name}
    //     values={sessions}
    //     setSelectedValue={handleSelectedSession}
    //     label="Select Session"
    //     marginTop={2}
    //   /> : ""} */}

    // </Box>
  );
}

// function Dropdown({
//   selectedValue,
//   values,
//   setSelectedValue,
//   label,
//   marginTop,
// }) {
//   return (
//     <FormControl fullWidth sx={{ mt: marginTop }}>
//       <InputLabel
//       // id="select-shot-name-label"
//       >
//         {label}
//       </InputLabel>
//       <Select
//         // labelId="select-shot-label"
//         // id="select-shot"
//         sx={{padding: 2}}
//         value={selectedValue}
//         label={label}
//         onChange={(e) => setSelectedValue(e.target.value)}
//       >
//         {values.map((session) => (
//           <MenuItem
//             key={session.id}
//             value={session.id}
//             sx={{ border: 2, margin: 2 }}

//           >
//             <FormControlLabel
//               value={session.id}
//               control={<Box/>}
//               label={
//                 <>
//                   <Typography variant="h6">
//                     Session Name: {session.name}
//                   </Typography>
//                   <Typography variant="body2">Date: {session.date}</Typography>
//                   <Typography variant="body2">From: {session.from}</Typography>
//                   <Typography variant="body2">To: {session.to}</Typography>
//                   <Typography variant="body2">
//                     Player: {session.player}
//                   </Typography>
//                 </>
//               }
//             />
//           </MenuItem>
//         ))}
//       </Select>
//     </FormControl>
//   );
// }
