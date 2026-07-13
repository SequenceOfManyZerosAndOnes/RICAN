#!/usr/bin/env python3
# ============================================================
"""
Figure 1.

Approximation error of the continued-fraction convergents
of log2(10).

This script reproduces Figure 1 from

RICAN:
A Fixed-Rate Representation Method for Finite Alphabets
via Continued-Fraction Approximation

Author:
J. Jesús Martínez Palomo
2026
"""
# ============================================================

import matplotlib.pyplot as plt
import math

# ------------------------------------------------------------
# Data
# ------------------------------------------------------------

q = [1, 3, 28, 59, 643, 9416]

x = math.log2(10)

p = [1,3,93,196,2136,31281]
q = [1,1,28,59,643,9416]

error = [abs(x-pi/qi) for pi,qi in zip(p,q)]

# ------------------------------------------------------------
# Figure
# ------------------------------------------------------------

plt.figure(figsize=(6.2, 4.0))

plt.xscale("log")
plt.yscale("log")

# Convergents
plt.plot(
    q,
    error,
    "o",
    markersize=6,
    label="Convergents"
)

# Highlight K = 643
plt.plot(
    643,
    3.654e-7,
    "s",
    markersize=8,
    label=r"$K=643$"
)

# Threshold
plt.axhline(
    1e-6,
    linestyle="--",
    linewidth=1.5
)

plt.text(
    4000,
    2e-6,
    r"Threshold $10^{-6}$",
    fontsize=9
)

plt.xlabel(r"Denominator $q$")
plt.ylabel(r"$|\log_2(10)-p/q|$")

plt.xlim(0.5, 20000)
plt.ylim(1e-8, 1)

plt.grid(True, which="both")

plt.legend(loc="upper left")

plt.tight_layout()

# ------------------------------------------------------------
# Export
# ------------------------------------------------------------

plt.savefig("Fig1.pdf", bbox_inches="tight")
plt.savefig("Fig1.png", dpi=600, bbox_inches="tight")

plt.show()