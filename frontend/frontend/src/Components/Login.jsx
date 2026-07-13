import React, { useState } from "react";
import "../Styles/Login.css";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
    const response = await fetch("https://product-analyzer-4.onrender.com/api/login/", {
    method: "POST",
    headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email,
    password,
  }),
});

      const result = await response.json();

      if (response.ok && result.status) {

        localStorage.setItem("name", result.name);
        localStorage.setItem("email", result.email);

        navigate("/home");
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.log(error);
      alert("Cannot connect to Django server");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">

        <h2>Welcome Back</h2>
        <p>Login to Continue Price Wise.</p>

        <div className="input-box">
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="input-box">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button className="main-login" onClick={handleLogin}>
          Login
        </button>

        <br />
        <br />

        <button className="signup">
          <Link to="/register">Register</Link>
        </button>

      </div>
    </div>
  );
}

export default Login;