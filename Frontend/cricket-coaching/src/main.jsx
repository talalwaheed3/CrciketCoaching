import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./components/auth/AuthContext.jsx";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    {" "}
    {/* Router should wrap everything */}
    <AuthProvider>
      {" "}
      {/* AuthProvider inside Router */}
      <StrictMode>
        <App />
      </StrictMode>
    </AuthProvider>
  </BrowserRouter>
);
