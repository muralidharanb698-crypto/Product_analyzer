import React, { useState } from "react";
import "../Styles/Login.css";
import { useNavigate,Link } from "react-router-dom";
import Loginbg from "./login_bg.jpg";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    const user = JSON.parse(localStorage.getItem("userData"));

    console.log("Stored user:", user);

    if (!user) {
      alert("No user found. Please register first");
      return;
    }

    if (user.email === email && user.password === password) {
      alert("Login Successful");

      navigate("/home");
    } else {
      alert("Invalid email or password");
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

        <div className="forgot">
          <a href="/">Forgot Password?</a>
        </div>

        <button className="main-login" onClick={handleLogin}>
          Login
        </button>
        <br/>
        <br/>
        <br/>
        <button className="signup"> <Link to='/register'>Register</Link></button>
      </div>
    </div>
  );
}

export default Login;