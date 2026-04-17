import { useState } from "react"
import ModeSelector from "./components/ModeSelector"
import StepVisualizer from "./components/StepVisualizer"
import AttackPanel from "./components/AttackPanel"
import ExplanationPanel from "./components/ExplanationPanel"

export default function App() {
  const [mode, setMode] = useState("ECB")
  const [plaintext, setPlaintext] = useState("")
  const [useHmac, setUseHmac] = useState(false)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const encrypt = async () => {
    if (!plaintext) return
    setLoading(true)
    const endpoint = mode === "ECB" ? "/encrypt/ecb" : "/encrypt/cbc"
    const res = await fetch(`http://localhost:5000${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plaintext, hmac: useHmac })
    })
    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "2rem", fontFamily: "monospace" }}>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>Encryption Explorer</h1>
      <p style={{ color: "#888", marginBottom: "2rem" }}>
        Visualize AES encryption step-by-step and explore real attack scenarios.
      </p>

      <ModeSelector mode={mode} setMode={setMode} useHmac={useHmac} setUseHmac={setUseHmac} />

      <div style={{ display: "flex", gap: "0.5rem", margin: "1.5rem 0" }}>
        <input
          value={plaintext}
          onChange={e => setPlaintext(e.target.value)}
          placeholder={mode === "ECB" ? 'Try "YELLOW SUBMARINEYELLOW SUBMARINE"' : "Enter any message..."}
          style={{
            flex: 1, padding: "0.6rem 1rem", borderRadius: 8,
            border: "1px solid #333", background: "#111", color: "#fff", fontFamily: "monospace"
          }}
        />
        <button
          onClick={encrypt}
          disabled={loading || !plaintext}
          style={{
            padding: "0.6rem 1.4rem", borderRadius: 8, border: "none",
            background: "#6c63ff", color: "#fff", cursor: "pointer", fontFamily: "monospace"
          }}
        >
          {loading ? "..." : "Encrypt"}
        </button>
      </div>

      {result && (
        <>
          <StepVisualizer result={result} />
          <AttackPanel result={result} mode={mode} />
          <ExplanationPanel mode={mode} useHmac={useHmac} result={result} />
        </>
      )}
    </div>
  )
}