import { useState } from "react";
import { Link,useNavigate } from "react-router-dom";
import "../Styles/Navbar.css";

export default function Navbar() {
  let username=localStorage.getItem('name')
  let navigate=useNavigate()
  const [menuOpen, setMenuOpen] = useState(false);
  const handleLogout=()=>{
     localStorage.removeItem("name");
      navigate('/')
  }

  return (
    <div className="navbar">
      <h3 id="logo">PriceWise</h3>

      <div
        className="hamburger"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        ☰
      </div>
      
      <div>
    </div>

      <div className={`nav ${menuOpen ? "active" : ""}`}>
        <Link to="/home">Home</Link>
        <Link to="/">Compare</Link>
        <div className="welcome">
    <h3>Welcome, {username}! 👋</h3>
    <div className="logout">
      <button onClick={handleLogout}>Logout</button>
    </div>
  </div>
      </div>
    </div>
  );
}

