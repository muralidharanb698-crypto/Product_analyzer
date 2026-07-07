import { useState ,useEffect} from "react";
import { Link, useNavigate } from "react-router-dom";
import "../Styles/Navbar.css";
import logo from "./logo.png";

export default function Navbar() {
  const username = localStorage.getItem("name");
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

useEffect(() => {
  const handleScroll = () => {
    setScrolled(window.scrollY > 50); 
  };

  window.addEventListener("scroll", handleScroll);

  return () => window.removeEventListener("scroll", handleScroll);
}, []);

  const handleLogout = () => {
    localStorage.removeItem("name");
    navigate("/");
  };


  return (
    <div className={`navbar ${scrolled ? "scrolled" : ""}`}>

      <div className="left">
        <img src={logo} width={60} height={50} alt="logo" />
        <h5 id="logo">Price<span id="wise">Wise</span></h5>
      </div>
      <div className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
        ☰
      </div>

      {/* Right side */}
      <div className={`nav ${menuOpen ? "active" : ""}`}>

        {/* Links */}
        <div className="nav-links">
          <Link to="/home" className="active">Home</Link>
          <a href="#compare">Compare</a>
          <a href="#trending">Trending Products</a>
        </div>

        {/* User section */}
        <div className="user-section">
          <h3>Welcome, {username}! 👋</h3>
          <button onClick={handleLogout}>Logout</button>
        </div>

      </div>
    </div>
  );
}