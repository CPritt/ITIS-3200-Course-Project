import { useState } from "react"

export default function AttackPanel({ result, mode }) {
  const [bytePos, setBytePos] = useState(0)
  const [flipVal, setFlipVal] = useState(1)
  const [attackResult, setAttackResult] = useState(null)
  const [loading, setLoading] = useState(false)

  if (mode !== "CBC") return null

  const runAttack = async () => {
    setLoading(true)
    const res = await fetch("http://localhost:5000/attack/bitflip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ciphertext: result.ciphertext,
        key: result.key,
        iv: result.iv,
        byte_position: parseInt(bytePos),
        flip_value: parseInt(flipVal)
      })
    })
    const data = await res.json()
    setAttackResult(data)
    setLoading(false)
  }

  return (
    <div style={{
      border: "1px solid #ff444444", borderRadius: 8,
      padding: "1rem 1.2rem", marginBottom: "2rem", background: "#ff44440a"
    }}>
      <h2 style={{ fontSize: "1rem", color: "#ff6666", marginBottom: "0.5rem" }}>
        ⚠ Bit-flip attack (no HMAC)
      </h2>
      <p style={{ color: "#888", fontSize: "0.8rem", marginBottom: "1rem" }}>
        Flip a byte in the ciphertext and observe how it corrupts the decrypted plaintext.
        This works because CBC has no integrity protection without HMAC.
      </p>

      <div style={{ display: "flex", gap: "1rem", alignItems: "flex-end", flexWrap: "wrap", marginBottom: "1rem" }}>
        <label style={{ color: "#aaa", fontSize: "0.8rem" }}>
          Byte position
          <input
            type="number" value={bytePos} min={0}
            onChange={e => setBytePos(e.target.value)}
            style={{
              display: "block", marginTop: "0.3rem", width: 80,
              padding: "0.4rem", borderRadius: 6, border: "1px solid #333",
              background: "#111", color: "#fff", fontFamily: "monospace"
            }}
          />
        </label>
        <label style={{ color: "#aaa", fontSize: "0.8rem" }}>
          Flip value (XOR)
          <input
            type="number" value={flipVal} min={1} max={255}
            onChange={e => setFlipVal(e.target.value)}
            style={{
              display: "block", marginTop: "0.3rem", width: 80,
              padding: "0.4rem", borderRadius: 6, border: "1px solid #333",
              background: "#111", color: "#fff", fontFamily: "monospace"
            }}
          />
        </label>
        <button
          onClick={runAttack}
          disabled={loading}
          style={{
            padding: "0.5rem 1.2rem", borderRadius: 8, border: "1px solid #ff4444",
            background: "transparent", color: "#ff6666", cursor: "pointer", fontFamily: "monospace"
          }}
        >
          {loading ? "..." : "Run attack"}
        </button>
      </div>

      {attackResult && (
        <div style={{ background: "#111", borderRadius: 8, padding: "0.8rem 1rem" }}>
          <div style={{ fontSize: "0.75rem", color: "#666", marginBottom: "0.4rem" }}>Corrupted plaintext</div>
          <div style={{ color: "#ff6666", fontFamily: "monospace", wordBreak: "break-all" }}>
            {attackResult.corrupted_plaintext}
          </div>
        </div>
      )}
    </div>
  )
}