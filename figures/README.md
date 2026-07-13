# Figures

This directory contains all figures used in the RICAN paper and documentation.

---

## 📊 Figure 1: Convergence of Continued Fractions

**Location:** `fig1_convergence/`

**Description:** 
Shows the approximation error of the convergents of log₂(10) in logarithmic scale. The convergent 2136/643 produces a dramatic reduction in error, dropping from approximately 10⁻⁴ to 10⁻⁷. The dashed line indicates the 10⁻⁶ threshold; 643 is the first denominator that falls below this threshold.

**Files:**
- `convergence_plot.py` - Python script to generate the figure
- `convergence_plot.pdf` - Vector format for publication
- `convergence_plot.png` - Raster format for web/README

**Key Insight:**
The convergent 2136/643 (K = 643) achieves an approximation error below 10⁻⁶, making it the optimal block size for decimal representation.

---

## 📈 Figure 2: Scaling Performance

**Location:** `fig2_scaling/`

**Description:**
Shows encoding time scaling with input size, confirming linear complexity O(L). Measured times follow the O(L) reference line, validating the theoretical complexity analysis.

**Files:**
- `scaling_plot.py` - Python script to generate the figure
- `scaling_plot.pdf` - Vector format for publication
- `scaling_plot.png` - Raster format for web/README

**Key Insight:**
The linear scaling confirms that RICAN maintains constant efficiency regardless of input size, from 1M to 100M digits.

---

## 📊 Benchmark Results

**Location:** `benchmark_results/`

**Description:**
Contains raw data from performance tests across multiple scales, validating the theoretical predictions.

**Files:**
- `benchmark_summary.csv` - Complete benchmark data in CSV format
- `benchmark_times.json` - Timing measurements in JSON format

**Benchmark Data:**

| Input Size | Blocks | Compressed Size | Ratio | Compression Time | Decompression Time |
|------------|--------|-----------------|-------|------------------|-------------------|
| 1,000,508 | 1,556 | 415,474 bytes | 41.5263% | 0.22s | 0.05s |
| 10,000,579 | 15,553 | 4,152,673 bytes | 41.5243% | 3.34s | 0.40s |
| 100,000,003 | 155,521 | 41,524,129 bytes | 41.5241% | 31.71s | 3.89s |

---

## 🔬 Validation on 20 Constants

**Description:**
Validation results showing RICAN produces identical compressed size for any sequence of the same length, confirming independence from source statistics.

**Constants Tested:**
π, e, γ, G, ζ(3), A, K₀, λ, ϖ, α, δ, C₂, M, K, λ, σ, ρ, T, μ, β

**Result:**
All 20 constants (1,000,508 digits each) produced identical compressed size of **415,474 bytes** (41.5263% ratio).

---

## 🚀 Generating Figures

To regenerate all figures:

```bash
# Figure 1: Convergence
cd fig1_convergence
python convergence_plot.py

# Figure 2: Scaling
cd ../fig2_scaling
python scaling_plot.py