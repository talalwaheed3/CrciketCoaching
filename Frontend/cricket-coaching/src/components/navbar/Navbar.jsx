import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import UserProfileMenu from "./UserProfileMenu";
// import { useAuth } from "../auth/AuthContext";
import AuthContext from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  console.log("in Navbar user is:", user);
  const navigate = useNavigate();

  const handleLogout = () => {
    alert("Logging out...");
    logout();
    navigate("/signin");
  };

  return (
    <AppBar
      sx={{
        backgroundColor: "#0B3D91",
        height: "64px",
        zIndex: 1201, // Ensures it's above Sidebar
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        margin: 0, // Ensure no margin is applied
        padding: 0,
      }}
    >
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Cricket Coaching System
        </Typography>

        {/* Profile Menu */}
        <UserProfileMenu user={user} />

        {/* Logout Button */}
        <Button
          variant="contained"
          color="error"
          sx={{
            ml: 2,
            px: 3,
            py: 1,
            fontSize: "0.875rem",
            fontWeight: "bold",
            borderRadius: "8px",
            textTransform: "none",
            backgroundColor: "#d32f2f",
            "&:hover": {
              backgroundColor: "#b71c1c",
            },
            boxShadow: "0px 3px 5px rgba(0,0,0,0.2)",
          }}
          onClick={()=>handleLogout()}
        >
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
