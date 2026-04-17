export default function ModeSelector({ mode, setMode, useHmac, setUseHmac }) {
  return (
    <div style={{ display: "flex", gap: "1rem", alignItems: "center", flexWrap: "wrap" }}>
      {["ECB", "CBC"].map(m => (
        <button
          key={m}
          onClick={() => setMode(m)}
          style={{
            padding: "0.5rem 1.2rem", borderRadius: 8, border: "2px solid",
            borderColor: mode === m ? "#6c63ff" : "#333",
            background: mode === m ? "#6c63ff22" : "transparent",
            color: mode === m ? "#6c63ff" : "#888",
            cursor: "pointer", fontFamily: "monospace", fontWeight: "bold"
          }}
        >
          AES-{m}
        </button>
      ))}

      {mode === "CBC" && (
        <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", color: "#aaa", cursor: "pointer" }}>
          <input
            type="checkbox"
            checked={useHmac}
            onChange={e => setUseHmac(e.target.checked)}
          />
          Enable HMAC integrity check
        </label>
      )}

      <span style={{
        marginLeft: "auto", padding: "0.3rem 0.8rem", borderRadius: 6,
        background: mode === "ECB" ? "#ff444422" : "#44ff8822",
        color: mode === "ECB" ? "#ff6666" : "#44ff88",
        fontSize: "0.8rem"
      }}>
        {mode === "ECB" ? "⚠ Vulnerable mode" : "✓ Secure mode"}
      </span>
    </div>
  )
}