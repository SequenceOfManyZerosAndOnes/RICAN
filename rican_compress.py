#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RICAN Compressor - Command Line Interface

Compress a decimal digit file using RICAN fixed-rate encoding.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for module import
sys.path.insert(0, str(Path(__file__).parent))

from rican import RICAN


def main():
    """Main entry point for compression CLI."""
    parser = argparse.ArgumentParser(
        description="RICAN Compressor - Fixed-rate decimal compression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1000508pi.txt
  %(prog)s -v my_data.txt
  %(prog)s --quiet data.txt
        """
    )
    
    parser.add_argument(
        "file",
        help="Input file containing decimal digits"
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
    
    # Compress
    try:
        compressor = RICAN(args.file)
        success = compressor.compress(verbose=verbose)
        
        if not success:
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()