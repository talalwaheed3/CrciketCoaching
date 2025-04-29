import { useState } from "react";
import { Card, Typography, TextField, MenuItem, Button } from "@mui/material";
import handleRequest from "../../utils/handleRequest"; // Ensure this exists

const UserForm = ({ roleType, apiEndpoint }) => {
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    password: "",
    experience: "",
    date_of_birth: "",
    contact_no: "",
    type: "",
  });
  const [usernameWarning, setUsernameWarning] = useState(false);
  // Handle Input Change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle Form Submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const { name, username, password, experience, date_of_birth, contact_no, type } =
      formData;

    if (
      !name ||
      !username ||
      !password ||
      !experience ||
      !date_of_birth ||
      !contact_no ||
      (roleType === "player" && !type)
    ) {
      alert("Please fill all required fields!");
      return;
    }

    try {
      const response = await handleRequest(apiEndpoint, "POST", {
        ...formData,
        role: roleType,
      });
      console.log("User Added:", response);
      if (!response) {
        setUsernameWarning(true);
        return;
      } else {
        setUsernameWarning(false);
      }
      alert(`${roleType} added successfully!`);

      // Reset Form
      setFormData({
        name: "",
        username: "",
        password: "",
        experience: "",
        date_of_birth: "",
        contact_no: "",
        type: roleType,
      });
    } catch (error) {
      console.error(`Error adding ${roleType}:`, error);
      alert(`Failed to add ${roleType}.`);
    }
  };

  return (
    <Card sx={{ p: 3, maxWidth: 500, margin: "auto", mt: 10 }}>
      <Typography variant="h6">
        Add {roleType === "player" ? "Player" : "Coach"}
      </Typography>

      {/* Name Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
      />

      {/* Username Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Username"
        name="username"
        value={formData.username}
        onChange={handleChange}
      />

      {/* Password Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Password"
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
      />

      {/* Experience Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Experience (years)"
        type="number"
        name="experience"
        value={formData.experience}
        onChange={handleChange}
      />

      {/* date_of_birth Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Date of Birth"
        type="text"
        name="date_of_birth"
        value={formData.date_of_birth}
        onChange={handleChange}
      />

      {/* Contact No Input */}
      <TextField
        fullWidth
        margin="normal"
        label="Contact No"
        name="contact_no"
        value={formData.contact_no}
        onChange={handleChange}
      />

      {/* Player Type Dropdown (Only for Players) */}
      {roleType === "player" && (
        <TextField
          select
          fullWidth
          margin="normal"
          label="Player Type"
          name="type"
          value={formData.type}
          onChange={handleChange}
        >
          <MenuItem value="left-handed batsman">Left-Handed Batsman</MenuItem>
          <MenuItem value="right-handed batsman">Right-Handed Batsman</MenuItem>
        </TextField>
      )}
      {usernameWarning && (
        <Typography sx={{ color: "red", mt: 1 }}>
          Username is already taken!!!
        </Typography>
      )}
      {/* Submit Button */}
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleSubmit}
      >
        Add {roleType === "player" ? "Player" : "Coach"}
      </Button>
    </Card>
  );
};

export default UserForm;
