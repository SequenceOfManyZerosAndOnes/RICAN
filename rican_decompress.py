#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RICAN Decompressor - Command Line Interface

Decompress a RICAN compressed .bin file back to decimal digits.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for module import
sys.path.insert(0, str(Path(__file__).parent))

from rican import RICAN


def main():
    """Main entry point for decompression CLI."""
    parser = argparse.ArgumentParser(
        description="RICAN Decompressor - Fixed-rate decimal decompression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1000508pi_RICAN_Comprimido.bin
  %(prog)s -v compressed.bin
  %(prog)s --quiet compressed.bin
        """
    )
    
    parser.add_argument(
        "file",
        help="Input .bin file (RICAN compressed format)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress information"
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
    
    # Decompress
    try:
        decompressor = RICAN(args.file)
        success = decompressor.decompress(verbose=verbose)
        
        if not success:
            sys.exit(1)
        
    except ValueError as e:
        print(f"❌ Format error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()