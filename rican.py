#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RICAN RJ03 - Core Algorithm

Representational Isomorphic Coding for Arbitrary Numeration

Universal fixed-rate representation method
for finite alphabets.

Format:
    RJ03

Features:
    - Decimal
    - DNA
    - Hexadecimal
    - ASCII
    - Base64
    - Arbitrary finite alphabets

RJ03 Improvements:
    - Stores original symbol count
    - Supports incomplete final blocks
    - Explicit format version
    - Exact reversible reconstruction

Author:
    J. Jesús Martínez Palomo
"""


import math
import os
import sys
import time

from pathlib import Path


sys.set_int_max_str_digits(0)


# ============================================================
# RJ03 FORMAT CONSTANTS
# ============================================================

MAGIC = b"RJ03"

VERSION = 3


# ============================================================
# HELPERS
# ============================================================


def log(msg):

    print(
        f"[{time.strftime('%H:%M:%S')}] {msg}",
        flush=True
    )



def get_base_name(filepath):

    name = Path(filepath).stem

    if name.endswith(
        "_RICAN_Comprimido"
    ):

        name = name.replace(
            "_RICAN_Comprimido",
            ""
        )

    return name



def filter_alphabet(text, alphabet):

    valid = set(alphabet)

    return "".join(
        c
        for c in text
        if c in valid
    )



def find_original_file(compressed_path):

    base = Path(
        compressed_path
    ).stem


    if base.endswith(
        "_RICAN_Comprimido"
    ):

        original = (
            base.replace(
                "_RICAN_Comprimido",
                ""
            )
            +
            ".txt"
        )

    else:

        original = (
            base
            +
            ".txt"
        )


    candidates = [

        original,

        os.path.join(
            "examples",
            original
        )

    ]


    for c in candidates:

        if os.path.exists(c):

            return c


    return None



# ============================================================
# RICAN CORE
# ============================================================


class RICAN:


    def __init__(
        self,
        filepath,
        alphabet,
        k
    ):


        self.filepath = filepath


        # Alphabet

        self.alphabet = alphabet

        self.base = len(
            alphabet
        )


        # Block size

        self.k = k


        # Number of bits required

        self.bits = math.ceil(

            self.k *
            math.log2(
                self.base
            )

        )


        # Stored bytes per block

        self.bytes = math.ceil(

            self.bits / 8

        )


        # Symbol maps

        self.encode_map = {

            c: i

            for i, c
            in enumerate(
                alphabet
            )

        }


        self.decode_map = {

            i: c

            for i, c
            in enumerate(
                alphabet
            )

        }


        # File names

        base_name = get_base_name(
            filepath
        )


        self.compressed_file = (

            base_name
            +
            "_RICAN_Comprimido.bin"

        )


        self.decompressed_file = (

            base_name
            +
            "_RICAN_Descomprimido.txt"

        )



    # ========================================================
    # RANK
    # ========================================================


    def rank(
        self,
        block
    ):


        value = 0


        for c in block:


            value *= self.base


            value += self.encode_map[c]


        return value



    # ========================================================
    # UNRANK
    # ========================================================


    def unrank(
        self,
        value
    ):


        chars = []


        for _ in range(
            self.k
        ):


            value, digit = divmod(

                value,

                self.base

            )


            chars.append(

                self.decode_map[digit]

            )


        chars.reverse()


        return "".join(
            chars
        )

#finp1

    # ========================================================
    # COMPRESS RJ03
    # ========================================================


    def compress(
        self,
        verbose=True
    ):


        t0 = time.time()


        if verbose:


            print("=" * 70)

            print(
                "RICAN RJ03 COMPRESS"
            )

            print("=" * 70)


            print(
                f"Alphabet : {self.alphabet}"
            )


            print(
                f"Base     : {self.base}"
            )


            print(
                f"K        : {self.k:,}"
            )


            print(
                f"Bits     : {self.bits:,}"
            )


            print(
                f"Bytes    : {self.bytes:,}"
            )



        # ----------------------------------------------------
        # Read source
        # ----------------------------------------------------


        with open(
            self.filepath,
            "r",
            encoding="utf8"
        ) as f:


            data = f.read()



        data = filter_alphabet(
            data,
            self.alphabet
        )


        # IMPORTANT:
        # Preserve the real original length

        original_length = len(data)



        # ----------------------------------------------------
        # Create blocks
        # ----------------------------------------------------

        blocks = []


        for i in range(
            0,
            original_length,
            self.k
        ):


            block = data[
                i:
                i+self.k
            ]


            # Last incomplete block
            # is padded only internally


            if len(block) < self.k:


                padding = (
                    self.alphabet[0]
                    *
                    (
                        self.k -
                        len(block)
                    )
                )


                block += padding



            blocks.append(
                block
            )



        # ----------------------------------------------------
        # Encode blocks
        # ----------------------------------------------------


        packed = bytearray()


        for block in blocks:


            value = self.rank(
                block
            )


            packed.extend(

                value.to_bytes(
                    self.bytes,
                    "big"
                )

            )



        # ----------------------------------------------------
        # Write RJ03 container
        # ----------------------------------------------------


        with open(
            self.compressed_file,
            "wb"
        ) as f:



            # Magic

            f.write(
                MAGIC
            )


            # Version

            f.write(

                VERSION.to_bytes(
                    4,
                    "little"
                )

            )


            # Alphabet base

            f.write(

                self.base.to_bytes(
                    4,
                    "little"
                )

            )


            # K

            f.write(

                self.k.to_bytes(
                    8,
                    "little"
                )

            )


            # Bits

            f.write(

                self.bits.to_bytes(
                    8,
                    "little"
                )

            )


            # Alphabet length

            f.write(

                len(
                    self.alphabet
                ).to_bytes(
                    4,
                    "little"
                )

            )


            # Alphabet

            f.write(

                self.alphabet.encode(
                    "utf8"
                )

            )


            # ORIGINAL LENGTH
            # This is the critical RJ03 fix

            f.write(

                original_length.to_bytes(
                    8,
                    "little"
                )

            )


            # Number of blocks

            f.write(

                len(blocks).to_bytes(
                    8,
                    "little"
                )

            )


            # Encoded payload

            f.write(
                packed
            )



        if verbose:


            size = os.path.getsize(
                self.compressed_file
            )


            print()

            print("=" * 70)


            print(
                f"Symbols : {original_length:,}"
            )


            print(
                f"Blocks  : {len(blocks):,}"
            )


            print(
                f"Output  : "
                f"{self.compressed_file}"
            )


            print(
                f"Size    : "
                f"{size:,}"
            )


            print(
                f"Ratio   : "
                f"{100*size/max(1,original_length):.6f}%"
            )


            print(
                f"Time    : "
                f"{time.time()-t0:.2f}s"
            )



        return True

#finp2

    # ========================================================
    # DECOMPRESS RJ03
    # ========================================================


    def decompress(
        self,
        verbose=True
    ):


        t0 = time.time()


        with open(
            self.filepath,
            "rb"
        ) as f:



            magic = f.read(4)


            if magic != MAGIC:

                raise ValueError(
                    "Invalid RJ03 file."
                )



            version = int.from_bytes(

                f.read(4),

                "little"

            )


            if version != VERSION:

                raise ValueError(

                    f"Unsupported RJ version: {version}"

                )



            base = int.from_bytes(

                f.read(4),

                "little"

            )


            k = int.from_bytes(

                f.read(8),

                "little"

            )


            bits = int.from_bytes(

                f.read(8),

                "little"

            )



            alphabet_len = int.from_bytes(

                f.read(4),

                "little"

            )



            alphabet = (

                f.read(
                    alphabet_len
                )
                .decode(
                    "utf8"
                )

            )



            # Original length saved by RJ03

            original_length = int.from_bytes(

                f.read(8),

                "little"

            )



            block_count = int.from_bytes(

                f.read(8),

                "little"

            )



            payload = f.read()



        # ----------------------------------------------------
        # Restore parameters
        # ----------------------------------------------------


        self.alphabet = alphabet

        self.base = base

        self.k = k

        self.bits = bits


        self.bytes = math.ceil(

            bits / 8

        )


        self.encode_map = {

            c: i

            for i, c in enumerate(
                alphabet
            )

        }


        self.decode_map = {

            i: c

            for i, c in enumerate(
                alphabet
            )

        }



        # ----------------------------------------------------
        # Decode blocks
        # ----------------------------------------------------


        result = []


        pos = 0



        for _ in range(
            block_count
        ):



            chunk = payload[

                pos:
                pos+self.bytes

            ]


            pos += self.bytes



            value = int.from_bytes(

                chunk,

                "big"

            )


            result.append(

                self.unrank(
                    value
                )

            )



        text = "".join(
            result
        )



        # Remove internal padding

        text = text[

            :original_length

        ]



        with open(
            self.decompressed_file,
            "w",
            encoding="utf8"
        ) as f:


            f.write(
                text
            )



        if verbose:


            print("=" * 70)


            print(
                "RICAN RJ03 DECOMPRESS"
            )


            print("=" * 70)


            print(
                f"Alphabet : {alphabet}"
            )


            print(
                f"Base     : {base}"
            )


            print(
                f"K        : {k:,}"
            )


            print(
                f"Blocks   : {block_count:,}"
            )


            print(
                f"Original : {original_length:,}"
            )


            print(
                f"Decoded  : {len(text):,}"
            )


            print(
                f"Time     : "
                f"{time.time()-t0:.2f}s"
            )



        return True





    # ========================================================
    # VERIFY RJ03
    # ========================================================


    def verify(self):


        original = find_original_file(

            self.filepath

        )


        if original is None:


            print(

                "Original file not found."

            )


            return False



        with open(

            original,

            "r",

            encoding="utf8"

        ) as f:


            original_text = filter_alphabet(

                f.read(),

                self.alphabet

            )



        with open(

            self.decompressed_file,

            "r",

            encoding="utf8"

        ) as f:


            decoded_text = filter_alphabet(

                f.read(),

                self.alphabet

            )



        print("=" * 70)


        print(
            "RICAN RJ03 VERIFY"
        )


        print("=" * 70)



        print(
            f"Original : {len(original_text):,}"
        )


        print(
            f"Decoded  : {len(decoded_text):,}"
        )



        if original_text == decoded_text:


            print()

            print(
                "VERIFICATION PASSED"
            )

            print("=" * 70)


            return True



        print()

        print(
            "VERIFICATION FAILED"
        )


        print()

        print(
            "Length mismatch:"
        )


        print(
            len(original_text)
        )


        print(
            len(decoded_text)
        )


        print("=" * 70)


        return False