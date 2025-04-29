import { useState } from "react";
import {
  Drawer,
  Toolbar,
  Typography,
  List,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Box,
} from "@mui/material";
import SportsCricketIcon from "@mui/icons-material/SportsCricket";
import { styled } from "@mui/material/styles";

const SidebarContainer = styled(Drawer)(({ theme }) => ({
  width: 250,
  flexShrink: 0,
  "& .MuiDrawer-paper": {
    width: 250,
    boxSizing: "border-box",
    backgroundColor: "#0B3D91",
    color: "white",
    position: "fixed",
    height: "calc(100vh - 64px)",
    top: "64px",
    left: 0,
    zIndex: 1200,
  },
}));

const Sidebar = ({ setSelectedSection, userDashboard, menuItems }) => {
  console.log("in Sidebar menuItems is:", menuItems)
  const [activeSection, setActiveSection] = useState(menuItems[0]?.key || "");

  return (
    <SidebarContainer className="relative top-10" variant="permanent">
      {/* Header with Cricket Icon */}
      <Toolbar
        sx={{
          backgroundColor: "#092C6F",
          color: "white",
          display: "flex",
          justifyContent: "center",
          p: 2,
        }}
      >
        <SportsCricketIcon fontSize="large" sx={{ mr: 1, color: "#00E676" }} />
        <Typography variant="h6" fontWeight="bold">
          {userDashboard}
        </Typography>
      </Toolbar>

      {/* Sidebar List */}
      <List>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.key}
            onClick={() => {
              setSelectedSection(item.key);
              setActiveSection(item.key);
            }}
            sx={{
              "&:hover": { backgroundColor: "#00E676", color: "#000" },
              backgroundColor:
                activeSection === item.key ? "#00E676" : "transparent",
              color: activeSection === item.key ? "#000" : "white",
            }}
          >
            <ListItemIcon
              sx={{ color: activeSection === item.key ? "#000" : "white" }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>

      {/* Bottom Logo / Footer */}
      <Box sx={{ flexGrow: 1 }} />
      <Box sx={{ textAlign: "center", p: 2, opacity: 0.7, fontSize: "12px" }}>
        <Typography variant="body2">🏏 Cricket Coaching System</Typography>
        <Typography variant="caption">Powered by BIIT</Typography>
      </Box>
    </SidebarContainer>
  );
};

export default Sidebar;

