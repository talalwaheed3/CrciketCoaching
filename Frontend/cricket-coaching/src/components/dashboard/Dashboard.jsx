import { useState } from "react";
import { Box, Container } from "@mui/material";
import Sidebar from "./Sidebar";
import MainContent from "./MainContent";
import Navbar from "../navbar/Navbar";

const Dashboard = ({ userDashboard, defaultSection, menuItems, role }) => {
  const [selectedSection, setSelectedSection] = useState(defaultSection);

  return (
    <>
      {/* Navbar - Positioned Fixed at the Top */}
      <Navbar className="color-scheme" />

      <Box sx={{ display: "flex", height: "100vh" }}>
        {/* Sidebar - Fixed on the Left */}
        <Sidebar
          userDashboard={userDashboard}
          setSelectedSection={setSelectedSection}
          menuItems={menuItems}
        />

        {/* Main Content - Adjusted Margin for Sidebar & Navbar */}
        <Box
          sx={{
            flexGrow: 1,
            ml: { xs: 0, sm: "250px" }, // Adjusts margin for smaller screens
            pt: { xs: "64px", sm: "70px" }, // Push content below Navbar
            p: 3,
            width: "100%", // Enables scrolling for long content
          }}
        >
          <Container>
            <MainContent selectedSection={selectedSection} role={role} />
          </Container>
        </Box>
      </Box>
    </>
  );
};

export default Dashboard;
