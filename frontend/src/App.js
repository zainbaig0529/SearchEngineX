import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    if (!query.trim()) return;

    try {
      const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Search failed", err);
    }
  };

  return (
    <div className="App" style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>SearchEngineX</h1>
      <input
        type="text"
        value={query}
        placeholder="Enter search query..."
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && search()}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={search} style={{ marginLeft: "10px", padding: "10px 20px" }}>
        Search
      </button>

      <div style={{ marginTop: "2rem", textAlign: "left" }}>
        {results.length > 0 ? (
          results.map(([docId, content, score]) => (
            <div key={docId} style={{ marginBottom: "20px" }}>
              <h3>{docId} — Score: {score.toFixed(4)}</h3>
              <p>{content}</p>
            </div>
          ))
        ) : (
          <p>No results yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;
