import React, { useState, useRef } from "react";
import "../Styles/Home.css";
import Navbar from "./Navbar";
import homeImg from "./top-right.png";
import amazon from "./amazon_img.png";
import flipkart from "./flipkart_img.png";
import messho from "./messho-img.png";
import ajio from "./ajio_img.png";
import products from "./Products";
import Footer from "./Footer";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const [comparison, setComparison] = useState([]);
  const [productImage, setProductImage] = useState("");
  const [productTitle, setProductTitle] = useState("");

  const mainProductSet = useRef(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setComparison([]);
    setProductImage("");
    setProductTitle("");
    mainProductSet.current = false;

    try {
    const res = await fetch(
    `https://product-analyzer-4.onrender.com/api/start-search/?q=${encodeURIComponent(query)}`,
  );

      const { search_id } = await res.json();

      const interval = setInterval(async () => {
        try {
        const statusRes = await fetch(
        `https://product-analyzer-4.onrender.com/api/search-status/${search_id}/`,
        );

          const statusData = await statusRes.json();
          console.log("STATUS DATA:", statusData);

          const sites = ["amazon", "flipkart", "ajio", "meesho"];

          const temp = [];

          for (const site of sites) {
            if (
              statusData[site]?.status === "done" &&
              statusData[site]?.data &&
              statusData[site].data.length > 0
            ) {
              temp.push({
                ...statusData[site].data[0],
                site: site,
              });
            }
          }

          console.log("Comparison:", temp);

          setComparison(temp);

          if (temp.length > 0 && !mainProductSet.current) {
            setProductImage(temp[0].image);
            setProductTitle(temp[0].title);
            mainProductSet.current = true;
          }

          const finished = sites.every(
            (site) => statusData[site]?.status !== "loading",
          );

          if (finished) {
            clearInterval(interval);
            setLoading(false);
          }
        } catch (err) {
          console.log(err);
          clearInterval(interval);
          setLoading(false);
        }
      }, 1000);
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <Navbar />
      <div className="top">
        <div className="left">
          <h1 id="compare">
            Find the <span>Best Price</span> EveryTime Save More{" "}
          </h1>
          <p>Compare Price From Amazon , Flipkart , Messho & Ajo</p>
          <p>And Save More on Every Purchase helloo</p>
        </div>
        <div className="right">
          <img src={homeImg} alt="Home" />
        </div>
      </div>

      <div className="search-box" id="compare">
        <input
          type="text"
          placeholder="Compare Products"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button id="search-btn" onClick={handleSearch}>
          Search
        </button>
      </div>
      <div className="ecommerce-site">
        <div className="amazon">
          <img src={amazon} width={200} height={400} />
        </div>
        <div className="flipkart">
          <img src={flipkart} width={200} height={400} />
        </div>
        <div className="ajio">
          <img src={ajio} />
        </div>
        <div className="messho">
          <img src={messho} />
        </div>
      </div>
      {loading && (
        <h3 style={{ textAlign: "center", marginTop: "20px" }}>Searching...</h3>
      )}

      {comparison.length > 0 && (
        <div className="comparison-container">
          <img
            src={productImage}
            alt={productTitle}
            className="product-image"
          />

          <h2>{productTitle}</h2>

          <table className="comparison-table">
            <thead>
              <tr>
                <th>Website</th>
                <th>Rating</th>
                <th>Price</th>
                <th>View Deal</th>
              </tr>
            </thead>

            <tbody>
              {comparison.map((item) => (
                <tr key={item.site}>
                  <td>{item.site.toUpperCase()}</td>

                  <td>{item.rating ?? "-"}</td>

                  <td>₹{item.price ?? "-"}</td>

                  <td>
                    {item.url ? (
                      <a href={item.url} target="_blank" rel="noreferrer">
                        View
                      </a>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="trending-section">
        <h2 id="trending">Trending Products</h2>

        <div className="slider">
          <div className="slide-track">
            {products.concat(products).map((product, index) => (
              <div className="comparison-card" key={index}>
                <img src={product.image} alt={product.title} />

                <h3>{product.title}</h3>

                <table>
                  <thead>
                    <tr>
                      <th>Site</th>
                      <th>Price</th>
                      <th>Link</th>
                    </tr>
                  </thead>

                  <tbody>
                    {product.comparison.map((item, i) => (
                      <tr key={i}>
                        <td>{item.site}</td>
                        <td>₹{item.price}</td>
                        <td>
                          <button>
                            <a href={item.url}>View</a>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
