```markdown
# Technical Report: Modular Analytics Pipeline & System Governance

**Course:** NUS AI/ML & Data Science Capstone (Part 2)  
**Environment:** Python 3.12 (`.venv` Isolated Environment)  
**Deliverables:** `main.py`, `feature_engineering.py`, `visualization.py`, `pipeline.log`, `outputs/`

---

## 1. Executive Summary & Infrastructure Governance

This project delivers a production-ready, modular command-line interface (CLI) application for urban traffic analytics. Built to meet strict software engineering standards, the system decouples data transformation logic from invocation interfaces. 

To resolve **Interpreter Drift**—a common issue on Windows systems where global Python executables override local virtual environments—the application strictly binds execution to `.\.venv\Scripts\python.exe`. System observability is maintained via a persistent dual-mode logger (`pipeline.log`), capturing operational flows at the `INFO` level and internal mathematical thresholds at the `DEBUG` level.

---

## 2. Feature Engineering & Quantile Threshold Audit

The feature engineering module (`feature_engineering.py`) transforms 9 raw variables into 31 engineered attributes, incorporating time-cyclical features, historical lags, and binned congestion targets.

```python
# Quantile binning logic for congestion stratification
Q1 = df['traffic_volume'].quantile(0.33)  # Q33 threshold
Q2 = df['traffic_volume'].quantile(0.66)  # Q66 threshold
Auditability Log Verification
To enforce algorithmic transparency, dynamic transformations are recorded directly into the audit stream:
	Row Transition: Dataset updated from 48,187 to 48,184 rows following lag missing-value pruning; column dimension expanded from 9 to 31.
	Audit Trail Entry: 2026-09-14 23:53:22,750 - DEBUG - Intermediate Quantile Thresholds - Q1 (33rd): 2157.00, Q2 (66th): 4546.00
	Congestion Stratification: Mapped into target categories: Low (<2157.00), Medium (2157.00-4546.00), and High (>4546.00).
3. Data Visualization Insights & Interpretations
The visualization module (visualization.py) exports three static plots to outputs/, writing INFO file-path records upon generation.
Output Figure	Plot Type	Key Analytical Findings
traffic_hourly_demand.png	Line Plot (hue='is_weekend')	Displays a distinct double-peak profile on weekdays (07:00–09:00 morning rush, 16:00–18:00 evening rush). Weekend traffic presents a smoother, single unimodal peak around mid-afternoon.
traffic_distribution_congestion.png	Box Plot	Confirms non-overlapping, distinct distributions across Low, Medium, and High congestion bands, verifying clean target separation without distributional anomalies.
traffic_weather_relationship.png	Scatter Plot	Demonstrates that severe adverse weather events (heavy rain/snow) reduce overall volume capacity across temperature ranges (-10^∘ "C"  to 25^∘ "C" ).
4. Mini Analytics CLI Application & Safety Guardrails
The application (main.py) exposes six subcommands built on argparse. Every invocation logs the command name and arguments to pipeline.log.
Input Validation & Defensive Error Handling
To ensure graceful failure, user inputs are sanitized before execution.
	Valid Invocation Example:
.\.venv\Scripts\python.exe main.py query-datetime --date "2018-09-14"
Log: INFO - Command invoked: 'query-datetime' with arguments: {'date': '2018-09-14'}
	Malformed Input Interception:
.\.venv\Scripts\python.exe main.py query-datetime --date "invalid-date"
Log: ERROR - Invalid date format supplied: 'invalid-date'. Expected format: YYYY-MM-DD.
Behavior: The error is caught cleanly; an ERROR message is logged, and the program exits without displaying raw stack tracebacks.
5. Translation to EM-AI Practice (Axis 4: Digital Health Readiness)
This capstone project demonstrates core software engineering practices applicable to clinical software systems in emergency medicine:
	Headless Execution & Microservice Architecture: Decoupling user interfaces from backend scripts allows algorithms to run as automated background tasks (e.g., cron jobs) on hospital servers, continually evaluating patient data or emergency department workflow metrics.
	Clinical Safety Guardrails: Defensive error handling prevents system crashes caused by malformed input data, ensuring system stability during active clinical workflows.
	Audit Trails & Governance: Dual-mode logging provides an immutable record of system execution and decision thresholds, supporting safety audits and algorithmic governance in clinical settings.

