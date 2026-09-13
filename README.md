# Metro Interstate Traffic Data Science & AI Capstone (End-to-End Analytics & ML Pipeline)

## 📌 Executive Overview
This repository contains the complete end-to-end Data Science capstone project for the NUS Data Science & AI Program. The project spans the full data analytics lifecycle: from relational database querying and statistical audits (Part 1), to machine learning predictive modeling (Part 2), and interactive executive storytelling (Part 3).

## 🧩 Project Architecture & Deliverables

### Part 1: SQL Data Engineering & Data Governance Audit
* **Exploratory Data Analysis:** Processed 48,204 hourly traffic records to establish diurnal volume baselines ($Mean = 3,259.82$, $SD = 1,986.86$).
* **Data Anomaly Remediation:** Filtered hardware sensor errors ($0\text{ K}$ / $-273.15^\circ\text{C}$) to prevent linear trendline skew.
* **Denominator Fallacy Audit:** Detected massive temporal data gaps in 2012, 2014, and 2015, enforcing normalized hourly metrics over raw annual totals.
* **Statistical Independence:** Calculated Odds Ratios ($\text{OR} \approx 1.0$) and joint probabilities, proving traffic congestion is driven by diurnal work schedules rather than ambient weather conditions.

### Part 2: Machine Learning & Predictive Modeling
* **Feature Engineering:** Extracted temporal features (Hour of Day, Day of Week, Month) and cyclical encodings from timestamp data.
* **Model Development & Evaluation:** Trained and evaluated multiple algorithms (Linear Regression, Decision Trees, Random Forest, XGBoost) to forecast traffic volume and classify high-density congestion ($>5,500$ vehicles/hr).
* **Performance Metrics:** Optimized model parameters targeting Minimum RMSE and Maximum $R^2$ Score for continuous volume forecasting.

### Part 3: Power BI Dashboard & Strategic Insights
* **Executive Dashboard:** Built interactive BI layouts showcasing diurnal congestion patterns, weather condition overlays, and temporal volume trends.
* **Decision Support:** Translated statistical findings into dynamic lane management recommendations and automated IoT data-quality pipelines.

---

## 📁 Complete Repository Structure

├── 01_sql_scripts/       # Part 1: SQL Data Cleaning, Aggregation & Joint Probability Queries
├── 02_statistics/        # Part 1: Statistical Logs, Execution Evidence & Query Screenshots
├── 03_ml_models/         # Part 2: Python Notebooks (.ipynb), Model Training & Feature Engineering
├── 04_power_bi/          # Part 3: Interactive Dashboard Files (.pbix) & Visual Reports
├── 05_reports/           # Final Executive Insights Report & Technical Workbook (.docx/.pdf)
└── README.md             # End-to-End Project Documentation

## 🛠 Tech Stack
* **Language & Querying:** SQL (Data Cleaning & Aggregations), Python (Pandas, NumPy, Scikit-Learn)
* **Visualization & BI:** Power BI, Matplotlib, Seaborn
* **Environment:** Jupyter Notebook, GitHub Version Control

---
Goal:
## 🏥 Medical AI & Clinical Governance Context
*Developed by an Emergency Medicine Academic Physician & AI Researcher (Vajira Hospital). 
The end-to-end framework demonstrated in this repository—from Data Cleaning & Confounder Identification (Part 1), 
to Risk Prediction Modeling (Part 2), and Clinical Decision-Support Visualization (Part 3)—serves as a technical blueprint for building safe, 
accountable, and practice-relevant AI pipelines in Emergency Department operations (e.g., Triage Risk Detection, Patient Flow Simulation, and EHR Data Audit).*
