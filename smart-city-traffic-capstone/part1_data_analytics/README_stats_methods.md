# Statistical Methodology & Data Audit Log
**Project**: NUS AI Capstone Part 1 (Tasks 2.1 & 2.2)  
**Dataset**: Metro Interstate Traffic Volume ($N = 48,204$)  
**Author**: EM-AI Research Unit, Vajira Hospital  

---

## 1. Data Hygiene & Outlier Handling Rules
* **Sampling Bias Prevention**: Switched Power BI column profiling from default `Top 1000 rows` to `Entire dataset` to guarantee full-sample ($N = 48,204$) statistical precision.
* **Sensor Anomaly Identification**: Exploratory analysis detected erroneous records with `temp = 0 K` (Absolute Zero / $-273.15^\circ\text{C}$), reflecting missing value default coding or sensor failures.
* **Filtering Rule**: Executed SQL condition `WHERE temp > 200` (and Power BI Visual Filter `temp > 200 K`) to eliminate unphysical noise, restoring natural data distribution and resolving axis compression.

---

## 2. Task 2.1: Descriptive Statistics Extraction Methods
All baseline metrics were cross-validated using both SQLite (`DB Browser`) queries and Power BI UI-driven Implicit Measures.

| Metric | SQL / Mathematical Method | Power BI No-Code UI Method | Result |
| :--- | :--- | :--- | :--- |
| **Count ($N$)** | `COUNT(*)` | Column Profile (`Entire dataset`) | 48,204 |
| **Mean ($\mu$)** | `AVG(traffic_volume)` | Table Visual -> Summarize: `Average` | 3,259.82 |
| **Median** | Quantile / Ordered Position | Table Visual -> Summarize: `Median` | 3,380.00 |
| **Std Dev ($\sigma$)** | Sample Standard Deviation | Table Visual -> Summarize: `Standard deviation` | 1,986.86 |
| **Variance ($\sigma^2$)** | Sample Variance Formula | Table Visual -> Summarize: `Variance` | 3,947,615.32 |
| **Range** | `MAX() - MIN()` | Formatted Table (`Max` - `Min`) | 7,280.00 |

---

## 3. Task 2.2: Pearson Correlation Analysis ($r$)
* **Mathematical Formula**: Computed using the expansion of Pearson's $r$ in SQLite:
  $$r = \frac{N \sum (XY) - (\sum X)(\sum Y)}{\sqrt{[N \sum X^2 - (\sum X)^2][N \sum Y^2 - (\sum Y)^2]}}$$
* **Calculated Output**: $r = +0.130$ (Cleaned Dataset: `temp > 200 K`).
* **Visualization Standard**: Generated Power BI Scatter Plot (`temp` on X-axis, `traffic_volume` on Y-axis) with `Don't summarize` detail points and an fitted linear Trend Line.
* **Analytical Interpretation**: Indicates a **very weak positive linear correlation** ($|r| < 0.30$). The co-occurrence is confounded by the diurnal cycle (Time of Day), demonstrating that **Correlation $\neq$ Causation**.