#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RICAN RJ03 Decompression CLI

Command line interface for RICAN decompression.

Uses:
    rican.py

Format:
    RJ03

Features:
    - Exact reconstruction
    - Supports incomplete final blocks
    - Restores original symbol count

Author:
    J. Jesús Martínez Palomo
"""


import argparse
import sys
import os


from rican import RICAN



# ============================================================
# DEFAULT CONFIGURATION
# ============================================================


DEFAULT_ALPHABET = "0123456789"

DEFAULT_K = 643



# ============================================================
# MAIN
# ============================================================


def main():


    parser = argparse.ArgumentParser(

        description=
        "RICAN RJ03 decompressor"

    )


    parser.add_argument(

        "input",

        help=
        "RICAN RJ03 compressed file (.bin)"

    )


    parser.add_argument(

        "-a",

        "--alphabet",

        default=DEFAULT_ALPHABET,

        help=
        "Finite alphabet"

    )


    parser.add_argument(

        "-k",

        "--block-size",

        type=int,

        default=DEFAULT_K,

        help=
        "Block size K"

    )


    args = parser.parse_args()



    if not os.path.exists(
        args.input
    ):


        print()

        print(
            "ERROR:"
        )

        print(
            f"File not found: {args.input}"
        )

        return 1



    print("=" * 70)

    print(
        "RICAN RJ03 DECOMPRESSOR"
    )

    print("=" * 70)


    print(
        f"Input    : {args.input}"
    )


    print(
        f"Alphabet : {args.alphabet}"
    )


    print(
        f"K        : {args.block_size:,}"
    )


    print()



    decoder = RICAN(

        filepath=args.input,

        alphabet=args.alphabet,

        k=args.block_size

    )



    try:


        decoder.decompress(

            verbose=True

        )


    except Exception as e:


        print()

        print(
            "DECOMPRESSION FAILED"
        )


        print(
            str(e)
        )


        return 1



    print()

    print(
        "DECOMPRESSION SUCCESS"
    )

    print("=" * 70)



    return 0





if __name__ == "__main__":


    sys.exit(
        main()
    )