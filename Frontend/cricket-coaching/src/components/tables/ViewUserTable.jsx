import { useState } from "react";
import {
  Card,
  Typography,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  IconButton,
  Avatar,
  TextField,
  Button,
  Box,
  Menu,
  MenuItem,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import FilterListIcon from "@mui/icons-material/FilterList";

const ViewUserTable = ({ role, endpoint }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterAnchor, setFilterAnchor] = useState(null);

  const handleFilterClick = (event) => {
    setFilterAnchor(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchor(null);
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2, p: 3, mt: 10 }}>
      {/* Title & Controls */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h6">{role}</Typography>

        {/* Search Input */}
        <TextField
          label="Search"
          variant="outlined"
          size="small"
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ width: "250px" }}
        />

        {/* Filter Button */}
        <Button
          startIcon={<FilterListIcon />}
          variant="outlined"
          onClick={handleFilterClick}
        >
          Filter
        </Button>
        <Menu anchorEl={filterAnchor} open={Boolean(filterAnchor)} onClose={handleFilterClose}>
          <MenuItem onClick={handleFilterClose}>Sort by Age</MenuItem>
          <MenuItem onClick={handleFilterClose}>Sort by Experience</MenuItem>
        </Menu>
      </Box>

      {/* Data Table */}
      <Card sx={{ p: 3 }}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Profile</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Password</TableCell>
                <TableCell>Experience</TableCell>
                <TableCell>Age</TableCell>
                <TableCell>Contact</TableCell>
                {role === "View Players" && <TableCell>Type</TableCell>}
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data
                .filter((item) =>
                  item.name.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Avatar src={item.profilePhoto} alt={item.name} />
                    </TableCell>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>{item.username}</TableCell>
                    <TableCell>{item.password}</TableCell>
                    <TableCell>{item.experience} years</TableCell>
                    <TableCell>{item.age}</TableCell>
                    <TableCell>{item.contact}</TableCell>
                    {title === "View Players" && <TableCell>{item.type}</TableCell>}
                    <TableCell align="right">
                      <IconButton>
                        <VisibilityIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
    </Box>
  );
};

export default ViewUserTable;
