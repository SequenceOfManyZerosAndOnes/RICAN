"""
fig2.py

Reproduces Figure 2 from:

RICAN: A Fixed-Rate Representation Method for
Finite Alphabets via Continued-Fraction Approximation

Reads:
    benchmark_results.csv

Produces:
    Fig2.pdf
    Fig2.png
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOAD EXPERIMENTAL DATA
# ============================================================

csv_file = "benchmark_results.csv"

L = []
times = []

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        L.append(int(row["input_digits"]))
        times.append(float(row["encoding_time_seconds"]))

L = np.array(L, dtype=float)
times = np.array(times, dtype=float)

# ============================================================
# REFERENCE O(L)
# ============================================================

# Least-squares proportional fit:
#
#      time ≈ c · L
#
c = np.sum(L * times) / np.sum(L ** 2)

x_ref = np.logspace(5, 10, 500)
y_ref = c * x_ref

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(7.2, 4.6))

plt.loglog(
    L,
    times,
    "o",
    markersize=7,
    label="Measured"
)

plt.loglog(
    x_ref,
    y_ref,
    "--",
    linewidth=2,
    label=r"$O(L)$ reference"
)

plt.xlabel(r"Input digits $L$")
plt.ylabel("Encoding time (s)")

plt.xlim(1e5, 1e10)
plt.ylim(1e-2, 1e3)

plt.grid(True, which="both", alpha=0.4)

plt.legend(loc="upper left")

plt.tight_layout()

# ============================================================
# EXPORT FIGURES
# ============================================================

plt.savefig("Fig2.pdf", bbox_inches="tight")
plt.savefig("Fig2.png", dpi=300, bbox_inches="tight")

plt.show()

# ============================================================
# REPORT
# ============================================================

print()
print("Figure 2 successfully generated.")
print(f"Experimental points : {len(L)}")
print(f"Estimated slope c   : {c:.3e} s/digit")
print("Generated files:")
print("   Fig2.pdf")
print("   Fig2.png")