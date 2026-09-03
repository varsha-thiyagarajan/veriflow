import { useState } from "react";
import "./App.css";

function App() {
  const [content, setContent] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function verifyContent() {
    if (!content.trim()) {
      setError("Please enter an AI-generated answer.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Verification failed.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>VeriFlow AI</h1>
          <p>AI Output Verification Dashboard</p>
        </div>
        <div className="status">
          <span className="status-dot"></span>
          Backend Ready
        </div>
      </header>

      <main className="container">
        <section className="input-card">
          <h2>Verify AI Output</h2>
          <p>
            Enter an AI-generated answer and VeriFlow will extract claims,
            retrieve external evidence, and verify them.
          </p>

          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Example: Java HashMap allows null keys."
          />

          <button onClick={verifyContent} disabled={loading}>
            {loading ? "Verifying..." : "Verify with VeriFlow"}
          </button>

          {error && <div className="error">{error}</div>}
        </section>

        {result && (
          <>
            <section className="phase-card">
              <div className="phase-title">
                <span>01</span>
                <div>
                  <h2>Claim Decomposition</h2>
                  <p>Phase 1</p>
                </div>
              </div>

              <div className="claims">
                {result.phase1.claims.map((claim) => (
                  <div className="claim-item" key={claim.claim_id}>
                    <div>
                      <strong>{claim.claim_id}</strong>
                      <span className="claim-type">
                        {claim.claim_type}
                      </span>
                    </div>
                    <p>{claim.claim_text}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="phase-card">
              <div className="phase-title">
                <span>02</span>
                <div>
                  <h2>Evidence Retrieval</h2>
                  <p>Phase 2 · External Web Search</p>
                </div>
              </div>

              {result.phase2.map((claim) => (
                <div className="evidence-section" key={claim.claim_id}>
                  <h3>{claim.claim_id}</h3>

                  {claim.evidence.map((evidence) => (
                    <div
                      className="evidence-item"
                      key={evidence.source_id}
                    >
                      <div className="evidence-header">
                        <strong>{evidence.title}</strong>
                        <span>
                          Reliability:{" "}
                          {(evidence.reliability * 100).toFixed(0)}%
                        </span>
                      </div>

                      <p>{evidence.text}</p>

                      <a
                        href={evidence.url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Open source
                      </a>
                    </div>
                  ))}
                </div>
              ))}
            </section>

            <section className="phase-card">
              <div className="phase-title">
                <span>03</span>
                <div>
                  <h2>Verification Oracle</h2>
                  <p>Phase 3 · NLI + Consensus</p>
                </div>
              </div>

              {result.phase3.map((verification) => {
                const verdict = verification.verdict;

                return (
                  <div
                    className={`verification-result ${verdict.toLowerCase()}`}
                    key={verification.claim_id}
                  >
                    <div className="result-top">
                      <div>
                        <strong>{verification.claim_id}</strong>
                        <p>{verification.claim_text}</p>
                      </div>

                      <div className="verdict">
                        {verdict}
                      </div>
                    </div>

                    <div className="metrics">
                      <div>
                        <span>Confidence</span>
                        <strong>
                          {(verification.confidence * 100).toFixed(1)}%
                        </strong>
                      </div>

                      <div>
                        <span>Consensus</span>
                        <strong>
                          {(verification.consensus_score * 100).toFixed(1)}%
                        </strong>
                      </div>
                    </div>

                    <div className="nli-results">
                      {verification.nli_results.map((nli) => (
                        <div className="nli-item" key={nli.source_id}>
                          <strong>{nli.source_id}</strong>

                          <span>
                            Entailment:{" "}
                            {(nli.entailment_probability * 100).toFixed(1)}%
                          </span>

                          <span>
                            Neutral:{" "}
                            {(nli.neutral_probability * 100).toFixed(1)}%
                          </span>

                          <span>
                            Contradiction:{" "}
                            {(nli.contradiction_probability * 100).toFixed(
                              1
                            )}
                            %
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;