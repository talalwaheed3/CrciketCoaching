import { useState, useEffect } from "react";
import {
  Card,
  Typography,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  IconButton,
  Paper,
  Avatar,
  TextField,
  Button,
  Box,
  Menu,
  MenuItem,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import FilterListIcon from "@mui/icons-material/FilterList";
import handleRequest from "../../utils/handleRequest";

const ViewUserTable = ({ body, endpoint }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterAnchor, setFilterAnchor] = useState(null);
  const [users, setUsers] = useState();

  const handleFilterClick = (event) => {
    setFilterAnchor(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchor(null);
  };

  const handleDisplayUsers = async () => {
    try {
      // users(coach/players) list of dictionaries
      const response = await handleRequest(endpoint, "POST", body); // true is for
      console.log("Response from handleRequest is:", response);
      setUsers(response);
      await console.log("users are:", users);
      for (let index = 0; index < 1000; index++) {
        index = index + 1;
      }
      console.log("users are", users);
    } catch (error) {
      console.error(`Error displaying ${body}:`, error);
    }
  };

  function handleSetSearch(e) {
    setSearchTerm(e.target.value);
    console.log("in handleSetSearch, users are", users);
  }

  useEffect(() => {
    handleDisplayUsers();
  }, []);
  return (
    <Box className="relative right-25" sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 10 }}>
      {/* Title & Controls */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h6">{body["role"]}</Typography>

        {/* Search Input */}
        {/* <TextField
          label="Search"
          variant="outlined"
          size="small"
          onChange={(e) => handleSetSearch(e)}
          sx={{ width: "250px" }}
        /> */}

        {/* Filter Button */}
        {/* <Button
          startIcon={<FilterListIcon />}
          variant="outlined"
          onClick={handleFilterClick}
        >
          Filter
        </Button>
        <Menu
          anchorEl={filterAnchor}
          open={Boolean(filterAnchor)}
          onClose={handleFilterClose}
        >
          <MenuItem onClick={handleFilterClose}>Sort by Age</MenuItem>
          <MenuItem onClick={handleFilterClose}>Sort by Experience</MenuItem>
        </Menu> */}
      </Box>

      {/* Data Table */}
      <Card sx={{ p: 0, maxHeight: "500px", overflow: "auto" }}>
        <TableContainer
          component={Paper}
          sx={{ maxHeight: "400px", overflow: "auto" }}
        >
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>Profile</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Password</TableCell>
                <TableCell>Experience</TableCell>
                <TableCell sx={{ whiteSpace: "nowrap", fontSize: "0.875rem" }}>
                  Date of Birth
                </TableCell>
                <TableCell>Contact</TableCell>
                {body.role === "player" && <TableCell>Type</TableCell>}
                <TableCell sx={{ whiteSpace: "nowrap", fontSize: "0.875rem" }}>Team Name</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users && users.length > 0 ? (
                users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <Avatar src="pfp.png" alt={user.name} />
                    </TableCell>
                    <TableCell>{user.name}</TableCell>
                    <TableCell>{user.username}</TableCell>
                    <TableCell>{user.password}</TableCell>
                    <TableCell>{user.experience} years</TableCell>
                    <TableCell>{user.date_of_birth}</TableCell>
                    <TableCell>{user.contact_no}</TableCell>
                    {body.role === "player" && (
                      <TableCell>{user.type}</TableCell>
                    )}
                    <TableCell>
                      {user.team_name ? user.team_name : "Not Assigned"}
                    </TableCell>
                    <TableCell align="right">
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
                      >
                        Archive
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={8} align="center">
                    Loading...
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
    </Box>
  );
};

export default ViewUserTable;
