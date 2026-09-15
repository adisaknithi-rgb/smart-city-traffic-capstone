# NUS AI Capstone Part 3: Progress Report (Task 1 & Task 2)

## 1. Executive Summary & Data Pipeline Overview
- **Dataset Context:** Analyzed 48,184 traffic monitoring records embedded with cyclical time encodings (hour_sin/cos, day_sin/cos).
- **Clinical/Domain Proxy Label:** Constructed a binary `high_risk` event proxy (4.37% positive imbalance), mirroring severe emergency room overcrowding and high-risk patient deterioration profiles in Emergency Department (ED) workflows.

---

## 2. Task 1: Supervised Learning Analysis

### 2.1 Regression (Traffic Volume / ED Surge Forecasting)
- **Baseline (Ridge Regression):** MAE = 437.84, R² = 0.8952. Showed convergence limitations under unscaled features.
- **Main Model (XGBoost Regressor):** MAE = 174.56, R² = 0.9786.
- **Insight:** XGBoost significantly reduced forecast error by ~60%, demonstrating high capacity for predicting operational volume surges.

### 2.2 Classification (High-Risk Event Detection)
- **Baseline (Logistic Regression with StandardScaler Pipeline):**
  - Resolved gradient convergence warnings using `StandardScaler` within `make_pipeline`.
  - Performance: Accuracy = 99.38%, Recall = 92.89%, ROC-AUC = 0.9991.
- **Main Model (XGBoost Classifier with Imbalance Weighting):**
  - Incorporated `scale_pos_weight` (~21.85) to heavily penalize False Negatives under a 4.37% risk imbalance.
  - Performance: Accuracy = 99.75%, **Recall = 97.87%**, ROC-AUC = 0.9998.
- **Strategic EM-AI Alignment (Risk Detection & Patient Safety):**
  - Maximizing Recall to 97.87% directly minimizes False Negatives (under-triage/missed critical risk) down to 2.13%, establishing a safety-first algorithmic baseline suitable for clinical triage support.

---

## 3. Task 2: Unsupervised Learning Analysis

### 3.1 K-Means Clustering (Operational Regime Phenotyping)
Using normalized variables (`traffic_volume`, `temp`, `hour_sin/cos`, `is_low_visibility`) at K=3:
- **Cluster 0 (Evening Rush-Hour Peak):** High volume (~4,346), late afternoon/evening hours (16:00–18:00). High operational congestion.
- **Cluster 1 (Night-Time Off-Peak Flow):** Lowest volume (~1,099), late-night/early-morning hours (01:00–04:00). High capacity headroom.
- **Cluster 2 (Morning Peak Surge):** Maximum volume (~4,755), morning peak hours (08:00–10:00). Peak bottleneck constraint.
- **Strategic EM-AI Alignment (Clinical Phenotyping):**
  - Demonstrates unsupervised stratification of operational workload states (ED Workload Phenotypes). Off-peak regimes (Cluster 1) require heightened safety-net vigilance due to staff fatigue, while peak regimes (Clusters 0 & 2) trigger resource re-allocation protocols.

### 3.2 Association Rule Mining (Congestion Determinants)
- **Discretization:** Transformed time of day, weekday type, and weather severity into discrete transactions.
- **Key Rules (High Lift > 1.2):** Identified strong rules linking specific evening peak windows and severe weather conditions to `Congestion_Severe` outcomes with confidence > 80%.

## 4. Task 3: Deep Learning (LSTM) & SHAP Explainability

### 4.1 LSTM Time-Series Architecture
- **Model Design:** Implemented a PyTorch-based Long Short-Term Memory (LSTM) network utilizing a 6-hour sliding window sequence to predict future traffic volume.
- **Performance:** Demonstration run reached MSE stability within 10 epochs.
- **Strategic EM-AI Alignment (ED Crowd Simulation):** Demonstrates time-series forecasting infrastructure required for predicting Emergency Department (ED) patient arrival surges and bed capacity constraints 6 hours in advance.

### 4.2 Model Explainability via SHAP
- **Methodology:** Applied SHAP (SHapley Additive exPlanations) TreeExplainer on an XGBoost surrogate regression model trained on identical feature sets.
- **Top Feature Attributions:**
  1. `hour_cos` (Mean |SHAP| = 1591.51)
  2. `hour_sin` (Mean |SHAP| = 575.04)
  3. `day_sin` (Mean |SHAP| = 367.17)
- **Insight:** Time-of-day cyclical patterns heavily dominate volume predictions over weather variables (`rain_1h`, `snow_1h`). Fulfills Algorithmic Accountability and Clinical Acceptance requirements for high-stakes decision support.

## 5. Task 4: Advanced AI Technique - MLflow Experiment Tracking

### 5.1 Justification & MLOps Architecture
- **Selected Technique:** MLflow Experiment Tracking.
- **Rationale:** Crucial for establishing algorithmic lineage, reproducibility, and auditability required by Software as a Medical Device (SaMD) standards in clinical deployments.

### 5.2 Implementation & Value Added
- **Implementation:** Structured dual-run logging (`Baseline_LogisticRegression` vs `XGBoost_Imbalance_Weighted`) tracking parameters (`max_iter`, `scale_pos_weight`), performance metrics (`Recall`, `ROC-AUC`), and serialized model artifacts within local tracking stores (`mlruns/`).
- **Logged Metrics:**
  - *Logistic Regression:* Accuracy = 99.38%, Recall = 92.89%, ROC-AUC = 0.9991
  - *XGBoost Classifier:* Accuracy = 99.75%, Recall = 97.87%, ROC-AUC = 0.9998
- **Value Added:** Provides an immutable audit trail and unified UI comparison dashboard, enabling seamless transition from experiment to API/production registry.

### 5.3 Limitations
- **Local Storage Scope:** Local SQLite/artifact logging lacks native cloud-based collaborative features required for multi-institution clinical trials (requires scaling to remote MLflow tracking servers).

## 7. Task 6: MLOps and Deployment Simulation

### 7.1 Model Versioning & MLflow Registry (6.1 & 6.2)
- **Model Lineage:** Tagged and registered `v1.0.0-xgboost` candidate model within MLflow artifact store.
- **Tracked Artifacts:** Hyperparameters (`scale_pos_weight`), metrics (`train_accuracy`), and model binary registry for full reproducibility.

### 7.2 FastAPI Model Deployment Mock-up (6.3)
- **Endpoint Structure:** Developed a RESTful FastAPI endpoint `/predict` accepting JSON payload representing weather and cyclical time features.
- **Inference Response:** Successfully processed inputs and served low-latency risk probability and binary classification predictions.

### 7.3 Data Drift Monitoring & Alerting System (6.4 & 6.5)
- **Monitoring Strategy:** Implemented two-sample Kolmogorov-Smirnov (KS) testing comparing reference baseline features against live inference stream distributions.
- **Drift Simulation Outcome:** Successfully flagged artificially introduced precipitation drift (`rain_1h`, p-value < 0.05).
- **Alerting Output:** System state automatically transitioned from `PASS / Normal` to `ALERT / Requires investigation` upon drift detection.

### 7.4 Strategic EM-AI Alignment (SaMD Governance)
- **Clinical Safety & Drift Guardrails:** In an emergency department deployment (e.g., ER Under-triage Alerting at Vajira Hospital), algorithmic drift caused by seasonal disease outbreaks or triage protocol changes can compromise patient safety. Real-time drift detection and automated alerting serve as essential clinical safety guardrails.

## 7. Task 6: MLOps and Deployment Simulation
- **Model Versioning:** Registered `v1_0_0_XGBoost_Production_Candidate` into MLflow Artifact Registry.
- **RESTful API:** Deployed FastAPI `/predict` endpoint serving low-latency risk probability predictions.
- **Drift Monitoring & Alerting:** Executed two-sample Kolmogorov-Smirnov (KS) testing. Detected feature drift in `rain_1h` (p = 0.0000) and `hour_sin` (p = 0.0381), successfully triggering automated `ALERT / Requires investigation` state.
- **Clinical MLOps Impact:** Establishes SaMD safety guardrails preventing silent algorithmic degradation during seasonal or operational clinical workflow shifts in Emergency Care.


## 8. Task 7: Responsible and Sustainable AI
- **Dataset Coverage & Sampling Bias:** Audited 48,184 records and identified severe environmental imbalance (7.19% rainy samples), leading to elevated predictive uncertainty during adverse weather events.
- **Proxy Label Disparity & Temporal Shift:** Revealed critical temporal disparity in proxy risk distribution—7.77% positivity rate during peak hours versus 0.00% during night shifts (01:00–04:00 AM)—highlighting a high risk of False Negatives (Under-triage) during off-peak hours where traffic volume drops but clinical vulnerability remains high.
- **Pre-Deployment Governance Oversight:** Enforces a mandatory Human-In-The-Loop (HITL) protocol where model outputs act strictly as Clinical Decision Support (CDS) alerts, preserving clinical autonomy and prohibiting autonomous decision-making.
- **Environmental & Compute Sustainability:** Selected lightweight XGBoost tabular inference (~2ms/sample) over continuous deep learning retraining, minimizing carbon footprint and compute energy while preserving target clinical sensitivity (Recall = 97.87%).
- **Clinical SaMD Alignment:** Operationalizes bias audits and resource sustainability into regulatory artifacts, directly reinforcing **Axis 2 (Risk Detection & Prevention)** and **Axis 4 (Digital Health Readiness)** for real-world ER Vajira integration.

### 8.1 Bias and Fairness Audit
- **Coverage & Sampling Limitations:** Audited 48,184 records and identified severe environmental coverage bias, with rainy conditions representing only 7.19% of total samples. This imbalance creates elevated predictive uncertainty during severe weather events.
- **Proxy Label Disparity:** Discovered extreme temporal imbalance in the `high_risk` proxy label—exhibiting a 7.77% positive risk rate during peak hours versus 0.00% during night shifts (01:00–04:00 AM). In clinical ED workflows, low night-time traffic volume does not equal low operational risk; overnight shifts face higher patient vulnerability due to staff fatigue and reduced diagnostic resources, exposing a critical Under-triage (False Negative) hazard.

### 8.2 Governance & Clinical Oversight
- **Human-In-The-Loop (HITL) Protocol:** Enforced mandatory decision-support boundaries where model predictions serve strictly as Clinical Decision Support (CDS) alerts for triage staff and EMS dispatchers. Autonomous algorithmic execution without physician override is strictly prohibited.

### 8.3 Sustainability & Resource Trade-offs
- **Low-Carbon Inference Architecture:** Prioritized lightweight XGBoost tabular inference (~2ms/sample) over continuous deep learning retraining. This significantly minimizes server energy consumption and carbon footprint while preserving the required clinical safety threshold (Recall = 97.87%).

### 8.4 Strategic EM-AI Alignment (SaMD Governance)
- Operationalizes algorithmic bias audits and compute sustainability into regulatory safety artifacts, directly reinforcing **Axis 2 (Risk Detection & Prevention)** and **Axis 4 (Digital Health Readiness)** for real-world ER Vajira deployment.