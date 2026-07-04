import { useState } from "react";
import { Link } from "react-router-dom";
import "../Styles/Navbar.css";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="navbar">
      <h3 id="logo">PriceWise</h3>

      <div
        className="hamburger"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        ☰
      </div>

      <div className={`nav ${menuOpen ? "active" : ""}`}>
        <Link to="/home">Home</Link>
        <Link to="/">Compare</Link>

        <button className="login-btn"><Link to='/'>Login</Link></button>
        <button className="register-btn"><Link to='/register'>Register</Link></button>
      </div>
    </div>
  );
}