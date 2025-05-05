import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    if (!query.trim()) return;

    try {
      const res = await fetch(`http://localhost:5000/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Search failed", err);
    }
  };

  return (
    <div className="App">
      <h1>SearchEngineX</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && search()}
        placeholder="Enter search query..."
        style={{ padding: "8px", width: "300px" }}
      />
      <button onClick={search} style={{ marginLeft: "10px", padding: "8px" }}>
        Search
      </button>

      <div style={{ marginTop: "20px" }}>
        {results.length > 0 ? (
          results.map(([docId, content, score]) => (
            <div key={docId} style={{ marginBottom: "10px", textAlign: "left" }}>
              <strong>{docId}</strong> — Score: {score.toFixed(4)}
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
