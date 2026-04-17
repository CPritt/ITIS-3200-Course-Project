const explanations = {
  ECB: {
    title: "Why ECB is broken",
    color: "#ff6666",
    body: `ECB encrypts every 16-byte block independently using the same key. 
This means identical plaintext blocks always produce identical ciphertext blocks. 
An attacker who can observe the ciphertext can detect repeated patterns without 
ever breaking the encryption — leaking structural information about the message.`,
    fix: "Use CBC mode with a random IV. The IV ensures the first block is unique every time, and chaining ensures no two blocks ever produce the same output."
  },
  CBC: {
    title: "Why CBC without HMAC is dangerous",
    color: "#ffaa44",
    body: `CBC mode fixes ECB's pattern problem by XORing each plaintext block with 
the previous ciphertext block before encrypting. However, CBC provides 
no integrity guarantee. An attacker who can modify the ciphertext can 
predictably corrupt specific bytes in the decrypted plaintext — a bit-flip attack.`,
    fix: "Always attach an HMAC tag to the ciphertext (Encrypt-then-MAC). Before decrypting, verify the HMAC. If it fails, reject the message entirely."
  }
}

export default function ExplanationPanel({ mode, useHmac }) {
  const exp = explanations[mode]

  return (
    <div style={{ border: `1px solid ${exp.color}44`, borderRadius: 8, padding: "1rem 1.2rem", background: `${exp.color}08` }}>
      <h2 style={{ fontSize: "1rem", color: exp.color, marginBottom: "0.75rem" }}>{exp.title}</h2>
      <p style={{ color: "#aaa", fontSize: "0.85rem", lineHeight: 1.7, marginBottom: "1rem" }}>{exp.body}</p>
      <div style={{ borderTop: "1px solid #222", paddingTop: "0.75rem" }}>
        <span style={{ color: "#44ff88", fontSize: "0.8rem", fontWeight: "bold" }}>Fix: </span>
        <span style={{ color: "#aaa", fontSize: "0.8rem" }}>{exp.fix}</span>
        {mode === "CBC" && useHmac && (
          <div style={{ marginTop: "0.5rem", color: "#44ff88", fontSize: "0.8rem" }}>
            ✓ HMAC is currently enabled — integrity is protected.
          </div>
        )}
      </div>
    </div>
  )
}