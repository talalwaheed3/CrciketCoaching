import { useState } from "react";
import {
  Menu,
  MenuItem,
  IconButton,
  Typography,
  Divider,
  Box,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

const UserProfileMenu = ({ user }) => {
  console.log("In UserProfileMenu user is:", user)
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box>
      <IconButton color="inherit" onClick={handleClick}>
        <AccountCircleIcon fontSize="large" />
        <MenuItem>{user.name}</MenuItem>
      </IconButton>

      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem disabled>
          <Typography variant="h6">Name: {user.name}</Typography>
        </MenuItem>
        <MenuItem disabled>Role: {user.role}</MenuItem>
        <MenuItem disabled>Username: {user.username}</MenuItem>
        <MenuItem disabled>Password: {user.password}</MenuItem>
        <MenuItem disabled>Date of birth: {user.age}</MenuItem>
        <MenuItem disabled>Experience: {user.experience}</MenuItem>
        <MenuItem disabled>Contact: {user.contact_no}</MenuItem>
        <Divider />
        <MenuItem onClick={handleClose}>Close</MenuItem>
      </Menu>
    </Box>
  );
};

export default UserProfileMenu;
