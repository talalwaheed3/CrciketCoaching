import { useState } from "react";
import { Box, Container } from "@mui/material";
import Sidebar from "./Sidebar";
import MainContent from "./MainContent";
import Navbar from "../navbar/Navbar";

const Dashboard = (userDashboard, defaultSection) => {
  const [selectedSection, setSelectedSection] = useState(defaultSection);

  return (
    <>
    <Navbar user={userDashboard} />
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Sidebar setSelectedSection={setSelectedSection} />
      <Box sx={{ flexGrow: 1, p: 3 }}>
        <Container>
          <MainContent selectedSection={selectedSection} />
        </Container>
      </Box>
    </Box>
    </>
  );
};

export default Dashboard;
