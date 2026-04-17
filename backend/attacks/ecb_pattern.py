def find_duplicate_blocks(ciphertext_hex: str) -> dict:
    """
    Scans ciphertext for identical 16-byte blocks.
    Returns the positions of any duplicates found.
    """
    BLOCK_SIZE = 32  # 16 bytes = 32 hex chars

    blocks = [ciphertext_hex[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext_hex), BLOCK_SIZE)]
    
    seen = {}
    duplicates = []

    for i, block in enumerate(blocks):
        if block in seen:
            duplicates.append({
                "block_index": i,
                "duplicate_of": seen[block],
                "ciphertext_block": block
            })
        else:
            seen[block] = i

    return {
        "total_blocks": len(blocks),
        "duplicate_blocks": duplicates,
        "vulnerable": len(duplicates) > 0
    }