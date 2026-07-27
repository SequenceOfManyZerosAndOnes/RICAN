#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gap_plot.py

Generates Figure 2: Absolute Representation Gap vs. Block Size.
Shows that the absolute gap only vanishes along the selected convergent subsequence.
"""

import math
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
LOG2_10 = math.log2(10)

# Function to compute the absolute gap
def absolute_gap(K):
    return math.ceil(K * LOG2_10) - K * LOG2_10

# --- Data Generation ---
# 1. Convergent-derived block sizes (from the paper)
K_convergents = [1, 3, 7, 22, 63, 643, 783032]
gaps_convergents = [absolute_gap(K) for K in K_convergents]

# 2. Arbitrary block sizes (for comparison)
K_random = list(range(1, 10000, 500)) + list(range(10000, 100000, 5000))
gaps_random = [absolute_gap(K) for K in K_random]

# --- Create the plot ---
fig, ax = plt.subplots(figsize=(8, 5))

# Plot arbitrary block sizes (scatter)
ax.scatter(K_random, gaps_random, s=5, color='#BDC3C7', alpha=0.6, label='Arbitrary K')

# Plot convergent block sizes (highlighted)
ax.scatter(K_convergents, gaps_convergents, color='#2C3E50', s=80, zorder=5, label='Convergent-derived K')

# Highlight K=643 and K=783032
ax.scatter([643], [absolute_gap(643)], color='#E74C3C', s=120, zorder=10, label='K = 643 (practical)')
ax.scatter([783032], [absolute_gap(783032)], color='#27AE60', s=120, zorder=10, label='K = 783032 (asymptotic)')

# --- Formatting ---
ax.set_xlabel('Block Size K', fontsize=12)
ax.set_ylabel('Absolute Representation Gap G_B(K) [bits]', fontsize=12)
ax.set_title('Absolute Representation Gap vs. Block Size', fontsize=14)
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True, which='both', linestyle='--', alpha=0.5)
ax.legend()

# Save figures
plt.savefig('gap_plot.pdf', format='pdf', bbox_inches='tight')
plt.savefig('gap_plot.png', format='png', dpi=300, bbox_inches='tight')
plt.show()

print("Figure 2 generated: gap_plot.pdf and gap_plot.png")