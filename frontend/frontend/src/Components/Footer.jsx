import "../Styles/Footer.css";
import {
  FaFacebookF,
  FaInstagram,
  FaTwitter,
  FaLinkedinIn,
  FaGithub,
  FaMapMarkerAlt,
  FaEnvelope,
  FaPhoneAlt,
} from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        <div className="footer-about">
          <h2>
            Price<span>Wise</span>
          </h2>

          <p>
            Compare prices from Amazon, Flipkart, Ajio and Meesho.
            Find the best deals instantly and save money on every purchase.
          </p>

          <div className="social-icons">
            <a href="#"><FaFacebookF /></a>
            <a href="#"><FaInstagram /></a>
            <a href="#"><FaTwitter /></a>
            <a href="#"><FaLinkedinIn /></a>
            <a href="#"><FaGithub /></a>
          </div>
        </div>

        <div className="footer-links">
          <h3>Quick Links</h3>

          <a href="/">Home</a>
          <a href="/">Trending Products</a>
          <a href="/">Compare</a>
          <a href="/">About</a>
          <a href="/">Contact</a>
        </div>

        <div className="footer-links">
          <h3>Categories</h3>

          <a href="/">Mobiles</a>
          <a href="/">Laptops</a>
          <a href="/">Headphones</a>
          <a href="/">Smart Watches</a>
          <a href="/">Fashion</a>
        </div>

        <div className="footer-contact">
          <h3>Contact Us</h3>

          <div className="contact-item">
            <FaMapMarkerAlt />
            <span>Chennai, Tamil Nadu, India</span>
          </div>

          <div className="contact-item">
            <FaPhoneAlt />
            <span>+91 98765 43210</span>
          </div>

          <div className="contact-item">
            <FaEnvelope />
            <span>support@pricewise.com</span>
          </div>
        </div>

      </div>

      <div className="footer-bottom">
        <p>
          © 2026 <span>PriceWise</span>. All Rights Reserved.
        </p>

        <div className="footer-policy">
          <a href="/">Privacy</a>
          <a href="/">Terms</a>
          <a href="/">Cookies</a>
        </div>
      </div>

    </footer>
  );
}