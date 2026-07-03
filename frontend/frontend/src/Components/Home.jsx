import React, { useState } from "react";
import "../Styles/Home.css";
import Navbar from "./Navbar";
import homeImg from "./home_img.jpg";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const [sites, setSites] = useState({
    amazon: { status: "idle", data: null },
    flipkart: { status: "idle", data: null },
    ajio: { status: "idle", data: null },
    meesho: { status: "idle", data: null },
  });

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);

    // Reset all cards
    setSites({
      amazon: { status: "loading", data: null },
      flipkart: { status: "loading", data: null },
      ajio: { status: "loading", data: null },
      meesho: { status: "loading", data: null },
    });

    try {
      // Start search
      const res = await fetch(
        `http://127.0.0.1:8000/api/start-search/?q=${encodeURIComponent(query)}`
      );

      const { search_id } = await res.json();

      // Poll every second
      const interval = setInterval(async () => {
        const statusRes = await fetch(
          `http://127.0.0.1:8000/api/search-status/${search_id}/`
        );

        const statusData = await statusRes.json();

        setSites(statusData);

        const finished = Object.values(statusData).every(
          (site) => site.status !== "loading"
        );

        if (finished) {
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
          <h2 id="compare">Compare Prices</h2>
          <h2 id="save">Save More</h2>

          <div className="search-box">
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
        </div>

        <div className="right">
          <img src={homeImg} alt="Home" />
        </div>
      </div>

      {loading && (
        <h3 style={{ textAlign: "center", marginTop: "20px" }}>
          Searching...
        </h3>
      )}

      <div className="products">
        {Object.entries(sites).map(([siteName, site]) => (
          <div className="card" key={siteName}>
            <h3>{siteName.toUpperCase()}</h3>

            {site.status === "loading" && (
              <>
                <p>⏳ Loading...</p>
              </>
            )}

            {site.status === "error" && (
              <>
                <p>❌ Failed</p>
              </>
            )}

            {site.status === "done" &&
              site.data &&
              site.data.length > 0 && (
                <>
                  <img
                    src={site.data[0].image}
                    alt={site.data[0].title}
                  />

                  <h4>{site.data[0].title.slice(0, 45)}</h4>

                  <h2>₹{site.data[0].price}</h2>

                  <p>{site.data[0].website}</p>

                  <p>⭐ {site.data[0].rating}</p>

                  <a
                    href={site.data[0].link}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <button>View</button>
                  </a>
                </>
              )}
          </div>
        ))}
      </div>
    </div>
  );
}