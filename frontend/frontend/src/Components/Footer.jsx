
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
    <footer>
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
            <a
              href="https://www.facebook.com"
              target="_blank"
              rel="noreferrer"
              aria-label="Facebook"
            >
              <FaFacebookF />
            </a>

            <a
              href="https://www.instagram.com"
              target="_blank"
              rel="noreferrer"
              aria-label="Instagram"
            >
              <FaInstagram />
            </a>

            <a
              href="https://twitter.com"
              target="_blank"
              rel="noreferrer"
              aria-label="Twitter"
            >
              <FaTwitter />
            </a>

            <a
              href="https://www.linkedin.com"
              target="_blank"
              rel="noreferrer"
              aria-label="LinkedIn"
            >
              <FaLinkedinIn />
            </a>

            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              aria-label="GitHub"
            >
              <FaGithub />
            </a>
          </div>
        </div>

        <div className="footer-links">
          <h3>Quick Links</h3>

          <a href="/">Home</a>
          <a href="/#trending">Trending Products</a>
          <a href="/#compare">Compare</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </div>

        <div className="footer-links">
          <h3>Categories</h3>

          <a href="/#compare">Mobiles</a>
          <a href="/#compare">Laptops</a>
          <a href="/#compare">Headphones</a>
          <a href="/#compare">Smart Watches</a>
          <a href="/#compare">Fashion</a>
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
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
          <a href="/cookies">Cookies</a>
        </div>
      </div>
    </footer>
  );
}

