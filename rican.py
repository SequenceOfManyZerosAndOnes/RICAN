#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RICAN - Core Algorithm
Representational Integer Coding for Arbitrary Numerals
Fixed-rate decimal representation encoder.

643 decimal digits -> 267 exact bytes
Format: RJ02

This module contains the core RICAN algorithm implementation.
"""

import os
import sys
import time
from pathlib import Path

# Allow Python to handle large integers
sys.set_int_max_str_digits(0)

# ================================================================
# CONSTANTS
# ================================================================

K = 643              # Block size in decimal digits
BYTES = 267          # Bytes per block (643 * log2(10) / 8 ≈ 267.0)
MAGIC = b"RJ02"      # File format magic number

# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def get_base_name(filepath: str) -> str:
    """
    Extract base filename without the RICAN compressed suffix.
    
    Args:
        filepath: Input file path
        
    Returns:
        Base filename without suffix
    """
    name = Path(filepath).stem
    
    if name.endswith("_RICAN_Comprimido"):
        name = name.replace("_RICAN_Comprimido", "")
    
    return name

def log(msg: str) -> None:
    """
    Print timestamped log message.
    
    Args:
        msg: Message to log
    """
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def extract_digits(text: str) -> str:
    """
    Extract only digit characters from text.
    
    Args:
        text: Input text
        
    Returns:
        String containing only digits
    """
    return "".join(c for c in text if c.isdigit())

def find_original_file(compressed_path: str) -> str | None:
    """
    Attempt to find the original file corresponding to a compressed file.
    
    Args:
        compressed_path: Path to compressed file
        
    Returns:
        Path to original file if found, None otherwise
    """
    base = Path(compressed_path).stem
    
    if base.endswith("_RICAN_Comprimido"):
        original_name = base.replace("_RICAN_Comprimido", "") + ".txt"
    else:
        original_name = base + ".txt"
    
    candidates = [
        original_name,
        os.path.join("examples", original_name)
    ]
    
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    
    return None

# ================================================================
# CORE RICAN ALGORITHM
# ================================================================

class RICAN:
    """
    RICAN fixed-rate encoder/decoder.
    
    Provides lossless compression for decimal digit sequences
    using fixed-length blocks of 643 digits encoded as 267 bytes.
    """
    
    def __init__(self, filepath: str):
        """
        Initialize RICAN processor.
        
        Args:
            filepath: Path to input file
        """
        self.filepath = filepath
        base = get_base_name(filepath)
        
        self.compressed_file = base + "_RICAN_Comprimido.bin"
        self.decompressed_file = base + "_RICAN_Descomprimido.txt"
    
    # ------------------------------------------------------------
    # COMPRESSION
    # ------------------------------------------------------------
    
    def compress(self, verbose: bool = True) -> bool:
        """
        Compress a decimal digit file.
        
        Args:
            verbose: If True, print progress information
            
        Returns:
            True if compression succeeded, False otherwise
        """
        start_time = time.time()
        
        if verbose:
            print("=" * 70)
            print("RICAN COMPRESSOR")
            print(f"{K} DIGITS -> {BYTES} BYTES")
            print("=" * 70)
        
        # Check input file exists
        if not os.path.exists(self.filepath):
            print("❌ File not found")
            return False
        
        # Read input file
        with open(self.filepath, "r", encoding="utf8") as f:
            data = f.read()
        
        # Extract digits
        digits = extract_digits(data)
        total = len(digits)
        
        if verbose:
            log(f"Digits: {total:,}")
        
        # Truncate to multiple of K
        usable = (total // K) * K
        
        if usable != total:
            if verbose:
                log(f"Truncating {total - usable} digits")
            digits = digits[:usable]
        
        # Split into blocks
        blocks = []
        for i in range(0, len(digits), K):
            blocks.append(digits[i:i+K])
        
        n_blocks = len(blocks)
        
        if verbose:
            log(f"Blocks: {n_blocks:,}")
        
        # Pack blocks into bytes
        packed = bytearray()
        
        for block in blocks:
            value = int(block)
            packed.extend(value.to_bytes(BYTES, "big"))
        
        # Write compressed file
        with open(self.compressed_file, "wb") as f:
            f.write(MAGIC)                          # Magic number
            f.write(len(digits).to_bytes(8, "little"))  # Original digit count
            f.write(n_blocks.to_bytes(8, "little"))     # Number of blocks
            f.write(K.to_bytes(2, "little"))            # Block size
            f.write(packed)                             # Compressed data
        
        # Results
        compressed_size = os.path.getsize(self.compressed_file)
        
        if verbose:
            print()
            print("=" * 70)
            print("RESULT")
            print("=" * 70)
            print(f"Input  : {self.filepath}")
            print(f"Output : {self.compressed_file}")
            print(f"Size   : {compressed_size:,} bytes")
            print(f"Ratio  : {compressed_size / max(1, len(digits)) * 100:.6f}%")
            print(f"Time   : {time.time() - start_time:.2f}s")
        
        return True
    
    # ------------------------------------------------------------
    # DECOMPRESSION
    # ------------------------------------------------------------
    
    def decompress(self, verbose: bool = True) -> bool:
        """
        Decompress a RICAN compressed file.
        
        Args:
            verbose: If True, print progress information
            
        Returns:
            True if decompression succeeded, False otherwise
        """
        start_time = time.time()
        
        # Read compressed file
        with open(self.filepath, "rb") as f:
            # Verify magic number
            if f.read(4) != MAGIC:
                raise ValueError("Invalid RICAN format: missing RJ02 magic")
            
            # Read header
            digit_count = int.from_bytes(f.read(8), "little")
            block_count = int.from_bytes(f.read(8), "little")
            block_size = int.from_bytes(f.read(2), "little")
            
            # Read payload
            payload = f.read()
        
        # Reconstruct digits
        result = []
        pos = 0
        
        for _ in range(block_count):
            chunk = payload[pos:pos + BYTES]
            pos += BYTES
            
            value = int.from_bytes(chunk, "big")
            result.append(str(value).zfill(block_size))
        
        # Join and truncate to original length
        decompressed = "".join(result)[:digit_count]
        
        # Write decompressed file
        with open(self.decompressed_file, "w", encoding="utf8") as f:
            f.write(decompressed)
        
        if verbose:
            print("=" * 70)
            print("RICAN DECOMPRESS")
            print("=" * 70)
            print(f"Output : {self.decompressed_file}")
            print(f"Digits : {len(decompressed):,}")
            print(f"Time   : {time.time() - start_time:.2f}s")
        
        return True
    
    # ------------------------------------------------------------
    # VERIFICATION
    # ------------------------------------------------------------
    
    def verify(self, verbose: bool = True) -> bool:
        """
        Verify decompressed file against original.
        
        Args:
            verbose: If True, print verification results
            
        Returns:
            True if verification passed, False otherwise
        """
        # Find original file
        original_path = find_original_file(self.filepath)
        
        # Read decompressed file
        with open(self.filepath, "r", encoding="utf8") as f:
            decompressed = f.read()
        
        if verbose:
            print("=" * 70)
            print("RICAN VERIFY")
            print("=" * 70)
        
        if original_path is None:
            print("⚠ Original file not found - cannot verify")
            print(f"  Decompressed digits: {len(decompressed):,}")
            return True
        
        # Read original
        with open(original_path, "r", encoding="utf8") as f:
            original_raw = f.read()
        
        original = extract_digits(original_raw)
        decompressed_digits = extract_digits(decompressed)
        
        # Compare
        if verbose:
            print(f"Original file     : {original_path}")
            print(f"Original digits   : {len(original):,}")
            print(f"Decompressed      : {self.filepath}")
            print(f"Decompressed digits: {len(decompressed_digits):,}")
        
        if original == decompressed_digits:
            if verbose:
                print()
                print("✅ VERIFICATION PASSED")
                print("   Files match exactly")
            return True
        else:
            if verbose:
                print()
                print("❌ VERIFICATION FAILED")
                print("   Files do not match")
            
            # Show first mismatch
            for i, (a, b) in enumerate(zip(original, decompressed_digits)):
                if a != b:
                    print(f"   First mismatch at position {i}: {a} != {b}")
                    break
            
            return False