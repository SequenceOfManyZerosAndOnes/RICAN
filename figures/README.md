# Figures

This directory contains all figures used in the RICAN paper and documentation.

## 📊 Figure 1: Convergence of Continued Fractions for log₂(10)

**Location:** `convergence_plot.pdf` / `convergence_plot.png`

**Description:** Shows the approximation error of the convergents of log₂(10) in logarithmic scale. The convergent 2601184/783032 achieves an error below 10⁻¹², demonstrating the asymptotic tightness of the RICAN construction.

**Key Insight:** The upper convergent denominator K=783032 achieves an absolute representation gap of approximately 5.20×10⁻⁷ bits, corresponding to a normalized per-symbol overhead of 6.64×10⁻¹³ bits/symbol.

**Files:**
- `convergence_plot.py` — Python script to generate the figure
- `convergence_plot.pdf` — Vector format for publication
- `convergence_plot.png` — Raster format for web/README

---

## 📈 Figure 2: Absolute Representation Gap vs. Block Size

**Location:** `gap_plot.pdf` / `gap_plot.png`

**Description:** Shows the absolute representation gap G_B(K) = ⌈K log₂(10)⌉ − K log₂(10) as a function of block size K. The convergent-derived block sizes (K=643, 783032, etc.) exhibit exceptionally small absolute gaps compared to arbitrary block sizes.

**Key Insight:** While the normalized overhead decreases for any growing K, the absolute gap only vanishes along the selected convergent subsequence. This demonstrates the constructive contribution of RICAN.

**Files:**
- `gap_plot.py` — Python script to generate the figure
- `gap_plot.pdf` — Vector format for publication
- `gap_plot.png` — Raster format for web/README

---

## 📊 Benchmark Results

**Location:** `benchmark_results/`

**Description:** Contains raw data from performance tests across multiple scales.

**Files:**
- `benchmark_summary.csv` — Complete benchmark data in CSV format
- `benchmark_times.json` — Timing measurements in JSON format

**Benchmark Data:**

| Input Size | Blocks | Encoded Size | Storage Rate | Time |
|------------|--------|--------------|--------------|------|
| 1,000,508  | 1,556  | 415,474 bytes | 41.5263% | 0.24s |
| 10,000,579 | 15,553 | 4,152,651 bytes | 41.5263% | 2.35s |
| 100,000,003 | 155,521 | 41,522,107 bytes | 41.5263% | 22.8s |

---

## 🚀 Generating Figures

To regenerate all figures:

```bash
# Figure 1: Convergence
python convergence_plot.py

# Figure 2: Absolute Gap
python gap_plot.py