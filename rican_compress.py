#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RICAN RJ03 Compression CLI

Command line interface for RICAN compression.

Uses:
    rican.py

Format:
    RJ03

Default:
    Alphabet : 0123456789
    K        : 643

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
        "RICAN RJ03 compressor"

    )


    parser.add_argument(

        "input",

        help=
        "Input text file"

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
        "RICAN RJ03 COMPRESSOR"
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



    encoder = RICAN(

        filepath=args.input,

        alphabet=args.alphabet,

        k=args.block_size

    )



    try:


        encoder.compress(
            verbose=True
        )


    except Exception as e:


        print()

        print(
            "COMPRESSION FAILED"
        )


        print(
            str(e)
        )


        return 1



    print()

    print(
        "COMPRESSION SUCCESS"
    )

    print("=" * 70)



    return 0





if __name__ == "__main__":


    sys.exit(
        main()
    )