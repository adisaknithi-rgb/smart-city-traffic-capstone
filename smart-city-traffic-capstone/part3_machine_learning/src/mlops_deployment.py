import os
import logging
import pandas as pd
import numpy as np
from scipy import stats
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)

# --- 6.3 Deployment: FastAPI Application & Input Schema ---
app = FastAPI(title="EM-AI Mobility Risk Prediction API", version="v1.0.0")

class TrafficInput(BaseModel):
    temp: float
    rain_1h: float
    snow_1h: float
    clouds_all: float
    hour_sin: float
    hour_cos: float
    day_sin: float
    day_cos: float

# Placeholder สำหรับโหลดโมเดลเข้าใช้งานใน API
global_model = None

@app.post("/predict")
def predict_risk(data: TrafficInput):
    """API Endpoint รับข้อมูลสภาวะแวดล้อมเพื่อทำนายความเสี่ยง High-Risk Event"""
    if global_model is None:
        return {"error": "Model not loaded"}
    
    input_df = pd.DataFrame([data.model_dump()])
    prob = float(global_model.predict_proba(input_df)[:, 1][0])
    prediction = int(prob >= 0.5)
    
    return {
        "model_version": "v1.0.0-xgboost",
        "high_risk_prediction": prediction,
        "high_risk_probability": round(prob, 4),
        "status": "PASS" if prob < 0.7 else "HIGH_RISK_ALERT"
    }

# --- 6.4 & 6.5 Monitoring & Alerting Functions ---
def detect_feature_drift(reference_data: pd.DataFrame, current_data: pd.DataFrame, threshold: float = 0.05) -> dict:
    """6.4 Simulate Feature Distribution Drift ด้วย Kolmogorov-Smirnov (KS) Test"""
    logger.info("--- Running Feature Distribution Drift Analysis (KS-Test) ---")
    drift_results = {}
    has_drift = False
    
    for col in reference_data.columns:
        stat, p_value = stats.ks_2samp(reference_data[col], current_data[col])
        is_drifted = p_value < threshold
        drift_results[col] = {"ks_stat": round(stat, 4), "p_value": round(p_value, 4), "drift_detected": is_drifted}
        if is_drifted:
            has_drift = True
            logger.warning("Drift detected in feature '%s' (p-value: %.4f)", col, p_value)
            
    # 6.5 Alerting Mechanism
    system_status = "ALERT / Requires investigation" if has_drift else "PASS / Normal"
    logger.info("System Health Status: [%s]", system_status)
    
    return {"system_status": system_status, "feature_drift_details": drift_results}

def run_mlops_pipeline(df: pd.DataFrame):
    global global_model
    logger.info("--- Starting Task 6: MLOps and Deployment Simulation ---")
    
    feature_cols = ["temp", "rain_1h", "snow_1h", "clouds_all", "hour_sin", "hour_cos", "day_sin", "day_cos"]
    X = df[feature_cols]
    y = df["high_risk"]
    
    # 6.1 & 6.2 Model Versioning & Experiment Tracking (MLflow)
    mlflow.set_experiment("Traffic_Risk_MLOps_Deployment")
    with mlflow.start_run(run_name="v1.0.0_XGBoost_Production_Candidate") as run:
        ratio = (len(y) - sum(y)) / sum(y)
        model = XGBClassifier(n_estimators=50, scale_pos_weight=ratio, random_state=42)
        model.fit(X, y)
        global_model = model
        
        mlflow.log_param("model_version", "v1.0.0")
        mlflow.log_param("algorithm", "XGBoost")
        mlflow.log_metric("train_accuracy", model.score(X, y))
        mlflow.xgboost.log_model(model, "model_v1_0_0")
        logger.info("Model v1.0.0 registered in MLflow Artifact Store. Run ID: %s", run.info.run_id)

    # 6.3 Test FastAPI Deployment Mock-up
    logger.info("--- Testing FastAPI Endpoint (/predict) ---")
    client = TestClient(app)
    sample_payload = {
        "temp": 288.15, "rain_1h": 0.0, "snow_1h": 0.0, "clouds_all": 40.0,
        "hour_sin": -0.866, "hour_cos": -0.5, "day_sin": 0.781, "day_cos": 0.623
    }
    response = client.post("/predict", json=sample_payload)
    logger.info("API Response (Status %d): %s", response.status_code, response.json())

    # 6.4 & 6.5 Simulate Drift and Alerting
    logger.info("--- Simulating Production Feature Drift ---")
    ref_data = X.sample(n=2000, random_state=42)
    curr_data = X.sample(n=2000, random_state=99).copy()
    
    # จำลอง Data Drift โดยเพิ่มค่าฝนตกหนักและอุณหภูมิผิดปกติใน Current Data
    curr_data["rain_1h"] = curr_data["rain_1h"] + np.random.exponential(scale=2.5, size=len(curr_data))
    
    drift_summary = detect_feature_drift(ref_data, curr_data)
    logger.info("Drift Monitoring & Alerting Result: %s", drift_summary["system_status"])

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/mlops_deployment.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    from src.data_processing import process_pipeline
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    run_mlops_pipeline(df_processed)