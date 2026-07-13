#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RICAN Verifier - Command Line Interface

Verify that a decompressed file matches the original.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for module import
sys.path.insert(0, str(Path(__file__).parent))

from rican import RICAN
from rican import find_original_file, extract_digits, log


def main():
    """Main entry point for verification CLI."""
    parser = argparse.ArgumentParser(
        description="RICAN Verifier - Verify decompressed output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1000508pi_RICAN_Descomprimido.txt
  %(prog)s -v decompressed.txt
  %(prog)s --original original.txt decompressed.txt
        """
    )
    
    parser.add_argument(
        "file",
        help="Decompressed .txt file to verify"
    )
    
    parser.add_argument(
        "-o", "--original",
        help="Original file to compare against (auto-detected if not provided)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed verification information"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors"
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    if not Path(args.file).exists():
        print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    # Determine verbosity
    verbose = args.verbose or not args.quiet
    
    # Determine original file
    original_path = args.original
    
    if original_path is None:
        original_path = find_original_file(args.file)
    
    try:
        # Read decompressed file
        with open(args.file, "r", encoding="utf8") as f:
            decompressed = f.read()
        
        decompressed_digits = extract_digits(decompressed)
        
        if verbose:
            print("=" * 70)
            print("RICAN VERIFY")
            print("=" * 70)
            print(f"File to verify: {args.file}")
            print(f"Digits        : {len(decompressed_digits):,}")
        
        # Check if we have an original to compare
        if original_path is None:
            print()
            print("⚠ WARNING: No original file found for comparison")
            print(f"  Decompressed file contains {len(decompressed_digits):,} digits")
            print("  Cannot verify correctness without original")
            sys.exit(0)
        
        if not Path(original_path).exists():
            print()
            print(f"❌ Error: Original file not found: {original_path}", file=sys.stderr)
            sys.exit(1)
        
        # Read original
        with open(original_path, "r", encoding="utf8") as f:
            original_raw = f.read()
        
        original_digits = extract_digits(original_raw)
        
        if verbose:
            print(f"Original file   : {original_path}")
            print(f"Original digits : {len(original_digits):,}")
        
        # Compare
        if original_digits == decompressed_digits:
            print()
            print("✅ VERIFICATION PASSED")
            print("   Files match exactly")
            sys.exit(0)
        else:
            print()
            print("❌ VERIFICATION FAILED")
            print("   Files do not match")
            
            # Show first mismatch
            for i, (a, b) in enumerate(zip(original_digits, decompressed_digits)):
                if a != b:
                    print(f"   First mismatch at position {i}: '{a}' != '{b}'")
                    break
            
            # Length mismatch
            if len(original_digits) != len(decompressed_digits):
                print(f"   Length mismatch: original {len(original_digits)} vs decompressed {len(decompressed_digits)}")
            
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()