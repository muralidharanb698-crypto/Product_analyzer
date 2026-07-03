import "../Styles/Navbar.css";

function Navbar() {
  return (
    <div>
      <div className="navbar">
        <h3 id="logo">PriceWise</h3>

        <div className="nav">
          <a href="/">Home</a>
          <a href="/compare">Compare</a>
          <button className="login-btn">Login</button>
          <button className="register-btn">Register</button>
        </div>
      </div>
    </div>
  );
}

export default Navbar;