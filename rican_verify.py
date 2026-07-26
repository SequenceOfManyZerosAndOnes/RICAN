#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RICAN RJ03 Verification CLI

Verifies that a decompressed RICAN file
is identical to the original source.

Checks:
    - Symbol count
    - Exact content equality

Format:
    RJ03

Author:
    J. Jesús Martínez Palomo
"""


import argparse
import sys
import os


from pathlib import Path


from rican import filter_alphabet



# ============================================================
# HELPERS
# ============================================================


DEFAULT_ALPHABET = "0123456789"



def find_original_file(
    decompressed_file
):


    path = Path(
        decompressed_file
    )


    name = path.stem


    if name.endswith(
        "_RICAN_Descomprimido"
    ):


        base = name.replace(

            "_RICAN_Descomprimido",

            ""

        )


    else:

        base = name



    candidates = [

        base + ".txt",

        os.path.join(
            "examples",
            base + ".txt"
        )

    ]



    for c in candidates:


        if os.path.exists(c):

            return c



    return None





# ============================================================
# VERIFY
# ============================================================


def verify(

    decoded_file,

    alphabet

):


    original_file = find_original_file(

        decoded_file

    )



    if original_file is None:


        print()

        print(
            "ERROR:"
        )

        print(
            "Original file not found."
        )

        return False



    with open(

        original_file,

        "r",

        encoding="utf8"

    ) as f:


        original = filter_alphabet(

            f.read(),

            alphabet

        )



    with open(

        decoded_file,

        "r",

        encoding="utf8"

    ) as f:


        decoded = filter_alphabet(

            f.read(),

            alphabet

        )



    print("=" * 70)

    print(
        "RICAN RJ03 VERIFY"
    )

    print("=" * 70)


    print(
        f"Alphabet : {alphabet}"
    )


    print(
        f"Original : {len(original):,}"
    )


    print(
        f"Decoded  : {len(decoded):,}"
    )



    print()



    if len(original) != len(decoded):


        print(
            "VERIFICATION FAILED"
        )


        print()

        print(
            "Length mismatch:"
        )


        print(
            f"Original length: {len(original):,}"
        )


        print(
            f"Decoded length : {len(decoded):,}"
        )


        print("=" * 70)


        return False



    if original != decoded:


        print(
            "VERIFICATION FAILED"
        )


        print()

        print(
            "Content mismatch."
        )


        # First differing position

        for i, (a, b) in enumerate(
            zip(
                original,
                decoded
            )
        ):


            if a != b:


                print(

                    f"First difference at position: {i}"

                )


                print(

                    f"Original symbol: {a}"

                )


                print(

                    f"Decoded symbol : {b}"

                )

                break



        print("=" * 70)


        return False



    print(
        "VERIFICATION PASSED"
    )


    print()

    print(
        "Files are identical."
    )


    print("=" * 70)


    return True





# ============================================================
# MAIN
# ============================================================


def main():


    parser = argparse.ArgumentParser(

        description=
        "RICAN RJ03 verification tool"

    )


    parser.add_argument(

        "input",

        help=
        "Decompressed RICAN text file"

    )


    parser.add_argument(

        "-a",

        "--alphabet",

        default=DEFAULT_ALPHABET,

        help=
        "Finite alphabet"

    )


    args = parser.parse_args()



    if not os.path.exists(
        args.input
    ):


        print(

            f"File not found: {args.input}"

        )

        return 1



    if verify(

        args.input,

        args.alphabet

    ):


        return 0



    return 1





if __name__ == "__main__":


    sys.exit(
        main()
    )