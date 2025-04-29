  import { useState, useContext } from "react";
  import { useNavigate } from "react-router-dom";
  import { FaUser, FaLock } from "react-icons/fa";
  import { IoEye, IoEyeOff } from "react-icons/io5";
  import apiRequest from "../../api";
  import AuthContext from "./AuthContext";

  function SignInPage() {
    const {login} = useContext(AuthContext)
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleSignIn = async () => {
      if (username && password) {
        const data = await apiRequest("/login", "POST", { username, password });
        console.log(username, password);
        // console.log("data.result is:", data.result);
        // console.log("data.user is:", data.user);
        const role = data.user.role.toLowerCase();
        console.log("role is:", role)
        if (data.result == "Login Successful") { 
          alert("Login Successful");
          if (role === "manager") {
            data.user.path = "/managerDashboard"
            login(data.user);
            navigate("/managerDashboard");
          }
          if (role === "coach") {
            data.user.path = "/coachDashboard"
            login(data.user);
            navigate("/coachDashboard");
          }
          if (role === "player") {
            data.user.path = "/playerDashboard"
            login(data.user);
            navigate("/playerDashboard");
          }
        } 
         else alert("Incorrect username or password");
      } else {
        alert("Please enter both username and password");
      }
    };

    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          {/* Back Button */}
          <button onClick={() => navigate("/")} className="text-green-700  mb-4">
            ← Back
          </button>

          {/* Logo */}
          <div className="flex justify-center mb-4">
            <img src="Welcome logo.png" alt="Cricket Logo" className="w-34" />
          </div>

          {/* Heading */}
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-4">
            Sign in
          </h2>

          {/* Username Input */}
          <div className="relative mb-4">
            <FaUser className="absolute left-3 top-3 text-gray-500" />
            <input
              type="text"
              placeholder="User Name"
              name="username"
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          {/* Password Input */}
          <div className="relative mb-4">
            <FaLock className="absolute left-3 top-3 text-gray-500" />
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              name="password"
              className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              className="absolute right-3 top-3 text-gray-500"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <IoEyeOff /> : <IoEye />}
            </button>
          </div>

          {/* Sign-In Button */}
          <button
            className="w-full bg-green-700 text-white py-2 rounded-md text-lg font-semibold hover:bg-green-800 transition"
            onClick={handleSignIn}
          >
            Sign in
          </button>
        </div>
      </div>
    );
  }

  export default SignInPage;
