import os
import logging
import pandas as pd
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

def run_mlflow_experiment(df: pd.DataFrame):
    """Task 4: Advanced AI Technique - MLflow Experiment Tracking for SaMD MLOps"""
    logger.info("--- Starting Task 4: MLflow Experiment Tracking ---")
    
    # 1. Setup MLflow Experiment
    mlflow.set_experiment("Smart_City_Traffic_Risk_Prediction")
    
    # 2. Data Preparation
    drop_cols = ["date_time", "traffic_volume", "high_risk", "congestion_category", "weather_main", "weather_description"]
    feature_cols = [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]
    
    X = df[feature_cols]
    y_cls = df["high_risk"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_cls, test_size=0.2, random_state=42, stratify=y_cls)
    
    # --- Experiment Run 1: Baseline Logistic Regression ---
    with mlflow.start_run(run_name="Baseline_LogisticRegression"):
        logger.info("Logging Run: Baseline Logistic Regression")
        
        # Params
        max_iter = 1000
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("scaler", "StandardScaler")
        mlflow.log_param("max_iter", max_iter)
        
        # Train
        model_log = make_pipeline(StandardScaler(), LogisticRegression(max_iter=max_iter))
        model_log.fit(X_train, y_train)
        
        # Evaluate
        preds = model_log.predict(X_test)
        probs = model_log.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        rec = recall_score(y_test, preds)
        auc = roc_auc_score(y_test, probs)
        
        # Log Metrics & Model
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model_log, "logistic_regression_model")
        
        logger.info("Logged LogisticReg | Recall: %.4f | ROC-AUC: %.4f", rec, auc)

    # --- Experiment Run 2: XGBoost Classifier (Imbalanced Risk Detection) ---
    with mlflow.start_run(run_name="XGBoost_Imbalance_Weighted"):
        logger.info("Logging Run: XGBoost Classifier")
        
        # Params
        n_estimators = 100
        ratio = (len(y_train) - sum(y_train)) / sum(y_train)
        
        mlflow.log_param("model_type", "XGBClassifier")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("scale_pos_weight", ratio)
        
        # Train
        model_xgb = XGBClassifier(n_estimators=n_estimators, scale_pos_weight=ratio, random_state=42)
        model_xgb.fit(X_train, y_train)
        
        # Evaluate
        preds_xgb = model_xgb.predict(X_test)
        probs_xgb = model_xgb.predict_proba(X_test)[:, 1]
        
        acc_xgb = accuracy_score(y_test, preds_xgb)
        rec_xgb = recall_score(y_test, preds_xgb)
        auc_xgb = roc_auc_score(y_test, probs_xgb)
        
        # Log Metrics & Model
        mlflow.log_metric("accuracy", acc_xgb)
        mlflow.log_metric("recall", rec_xgb)
        mlflow.log_metric("roc_auc", auc_xgb)
        mlflow.xgboost.log_model(model_xgb, "xgboost_classifier_model")
        
        logger.info("Logged XGBoost | Recall: %.4f | ROC-AUC: %.4f", rec_xgb, auc_xgb)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/advanced_models.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    from src.data_processing import process_pipeline
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    run_mlflow_experiment(df_processed)