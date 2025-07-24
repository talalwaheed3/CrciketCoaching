// components/FullscreenLoader.js
import { Box, LinearProgress, Typography } from "@mui/material";

export default function FullscreenLoader({ message = "Uploading video..." }) {
  return (
    <Box
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 9999,
        width: "100vw",
        height: "100vh",
        bgcolor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Box sx={{ width: "60%", mb: 2 }}>
        <LinearProgress color="secondary" />
      </Box>
      <Typography variant="h6" color="white">
        {message}
      </Typography>
    </Box>
  );
}
