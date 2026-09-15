import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.pipeline import make_pipeline             # <--- เพิ่มตัวนี้สำหรับสร้าง Pipeline
from sklearn.preprocessing import StandardScaler       # <--- เพิ่มตัวนี้สำหรับปรับ Scale ข้อมูล
from sklearn.metrics import (
    mean_absolute_error, 
    r2_score, 
    accuracy_score, 
    recall_score, 
    roc_auc_score
)
from xgboost import XGBRegressor, XGBClassifier

logger = logging.getLogger(__name__)

def train_supervised_models(df: pd.DataFrame):
    """ฝึกและประเมินผล Supervised Models ตามข้อกำหนด NUS Task 1"""
    logger.info("Initiating Supervised Model Training (Task 1)...")
    
    # 1. คัดเลือก Feature และแบ่ง Target
    drop_cols = ["date_time", "traffic_volume", "high_risk", "congestion_category", "weather_main", "weather_description"]
    feature_cols = [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]
    
    X = df[feature_cols]
    y_reg = df["traffic_volume"]
    y_cls = df["high_risk"]
    
    logger.info("Selected %d feature columns for training.", len(feature_cols))

    # 2. Train/Test Split (80/20) พร้อม Stratify สำหรับ Target Classification
    X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = train_test_split(
        X, y_reg, y_cls, test_size=0.2, random_state=42, stratify=y_cls
    )
    logger.info("Data split complete: Train=%d, Test=%d", len(X_train), len(X_test))

    # 3. Task 1A: Regression Models (Traffic Volume)
    logger.info("--- Training Regression Models ---")
    
    # Baseline: Ridge Regressor
    ridge = Ridge().fit(X_train, y_reg_train)
    p_ridge = ridge.predict(X_test)
    logger.info("Baseline Ridge Regressor | MAE: %.2f | R2: %.4f", 
                mean_absolute_error(y_reg_test, p_ridge), r2_score(y_reg_test, p_ridge))

    # Main Model: XGBoost Regressor
    xgb_reg = XGBRegressor(n_estimators=100, random_state=42).fit(X_train, y_reg_train)
    p_xgb_reg = xgb_reg.predict(X_test)
    logger.info("XGBoost Regressor        | MAE: %.2f | R2: %.4f", 
                mean_absolute_error(y_reg_test, p_xgb_reg), r2_score(y_reg_test, p_xgb_reg))

    # 4. Task 1B: Classification Models (High Risk Detection)
    logger.info("--- Training Classification Models ---")
    
    # Baseline: Logistic Regression (ใช้ StandardScaler + Pipeline ป้องกัน Convergence Warning)
    log_reg = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    log_reg.fit(X_train, y_cls_train)
    
    p_log = log_reg.predict(X_test)
    prob_log = log_reg.predict_proba(X_test)[:, 1]
    logger.info("Baseline Logistic Reg | Accuracy: %.4f | Recall: %.4f | ROC-AUC: %.4f", 
                accuracy_score(y_cls_test, p_log), recall_score(y_cls_test, p_log), roc_auc_score(y_cls_test, prob_log))

    # Main Model: XGBoost Classifier (ปรับ scale_pos_weight รับมือ Imbalanced Data 4.37%)
    ratio = (len(y_cls_train) - sum(y_cls_train)) / sum(y_cls_train)
    xgb_cls = XGBClassifier(n_estimators=100, scale_pos_weight=ratio, random_state=42).fit(X_train, y_cls_train)
    p_xgb_cls = xgb_cls.predict(X_test)
    prob_xgb_cls = xgb_cls.predict_proba(X_test)[:, 1]
    logger.info("XGBoost Classifier     | Accuracy: %.4f | Recall: %.4f | ROC-AUC: %.4f", 
                accuracy_score(y_cls_test, p_xgb_cls), recall_score(y_cls_test, p_xgb_cls), roc_auc_score(y_cls_test, prob_xgb_cls))

    return {"ridge": ridge, "xgb_reg": xgb_reg, "log_reg": log_reg, "xgb_cls": xgb_cls}

if __name__ == "__main__":
    import os
    
    # 1. สร้างโฟลเดอร์ logs อัตโนมัติหากยังไม่มีในระบบ
    os.makedirs("logs", exist_ok=True)
    
    # 2. ตั้งค่า Centralized Logging บันทึกลงไฟล์ logs/supervised_models.log และแสดงบน Terminal
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/supervised_models.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    logger.info("Starting Supervised Models Execution Trail...")
    
    # 3. เรียกประมวลผล Pipeline ข้อมูลและฝึกโมเดล
    from src.data_processing import process_pipeline
    
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    models = train_supervised_models(df_processed)
    
    logger.info("Supervised Model Training completed successfully. Log saved to logs/supervised_models.log")