export default function StepVisualizer({ result }) {
  const { steps, key, iv, mode } = result

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2 style={{ fontSize: "1rem", color: "#aaa", marginBottom: "1rem" }}>Encryption parameters</h2>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem", flexWrap: "wrap" }}>
        <Param label="Key" value={key} />
        {iv && <Param label="IV" value={iv} />}
        {result.hmac_tag && <Param label="HMAC tag" value={result.hmac_tag} color="#44ff88" />}
      </div>

      <h2 style={{ fontSize: "1rem", color: "#aaa", marginBottom: "1rem" }}>
        Block-by-block encryption {mode === "ECB" ? "(no chaining)" : "(CBC chaining)"}
      </h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {steps.map((step, i) => (
          <BlockStep key={i} step={step} mode={mode} />
        ))}
      </div>
    </div>
  )
}

function Param({ label, value, color = "#6c63ff" }) {
  return (
    <div style={{ background: "#111", border: "1px solid #222", borderRadius: 8, padding: "0.6rem 1rem" }}>
      <div style={{ fontSize: "0.7rem", color: "#666", marginBottom: "0.2rem" }}>{label}</div>
      <div style={{ fontSize: "0.75rem", color, wordBreak: "break-all", maxWidth: 300 }}>{value}</div>
    </div>
  )
}

function BlockStep({ step, mode }) {
  const isDuplicate = step.identical_to !== null && step.identical_to !== undefined
  const borderColor = isDuplicate ? "#ff4444" : "#222"
  const bgColor = isDuplicate ? "#ff444411" : "#111"

  return (
    <div style={{ border: `1px solid ${borderColor}`, borderRadius: 8, padding: "0.8rem 1rem", background: bgColor }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
        <span style={{ color: "#666", fontSize: "0.75rem" }}>Block {step.block_index}</span>
        {isDuplicate && (
          <span style={{ color: "#ff4444", fontSize: "0.75rem", fontWeight: "bold" }}>
            ⚠ Identical to block {step.identical_to} — pattern leaks!
          </span>
        )}
      </div>

      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", flexWrap: "wrap", fontSize: "0.75rem" }}>
        <HexBox label="Plaintext" value={step.plaintext_block} color="#fff" />
        {mode === "CBC" && (
          <>
            <Arrow />
            <HexBox label={step.block_index === 0 ? "XOR with IV" : "XOR with prev CT"} value={step.xor_with} color="#aaa" />
            <Arrow />
            <HexBox label="XORed" value={step.xored_block} color="#88aaff" />
          </>
        )}
        <Arrow />
        <HexBox
          label="Ciphertext"
          value={step.ciphertext_block}
          color={isDuplicate ? "#ff6666" : "#6c63ff"}
        />
      </div>
    </div>
  )
}

function HexBox({ label, value, color }) {
  return (
    <div style={{ background: "#0a0a0a", border: "1px solid #333", borderRadius: 6, padding: "0.4rem 0.6rem" }}>
      <div style={{ color: "#555", fontSize: "0.65rem", marginBottom: "0.2rem" }}>{label}</div>
      <div style={{ color, fontFamily: "monospace", wordBreak: "break-all", maxWidth: 160 }}>{value}</div>
    </div>
  )
}

function Arrow() {
  return <span style={{ color: "#444", fontSize: "1rem" }}>→</span>
}