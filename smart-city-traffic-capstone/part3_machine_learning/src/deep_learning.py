import os
import logging
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import shap
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

logger = logging.getLogger(__name__)

# 1. นิยามโครงสร้าง LSTM Model ด้วย PyTorch
class TrafficLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=32, num_layers=1):
        super(TrafficLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # ดึง Output ของ Timestep สุดท้าย
        return out

def create_sequences(data, target, seq_length=6):
    """แปลงข้อมูล Tabular ให้เป็น Sliding Windows (3D Sequences)"""
    X_seq, y_seq = [], []
    for i in range(len(data) - seq_length):
        X_seq.append(data[i : i + seq_length])
        y_seq.append(target[i + seq_length])
    return np.array(X_seq), np.array(y_seq)

def train_lstm_and_explain(df: pd.DataFrame, seq_length: int = 6):
    logger.info("--- Starting Task 3: Deep Learning (LSTM) & SHAP Explainability ---")
    
    feature_cols = ["temp", "rain_1h", "snow_1h", "clouds_all", "hour_sin", "hour_cos", "day_sin", "day_cos"]
    target_col = "traffic_volume"
    
    # 2. Preparation & Scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[feature_cols])
    target_vals = df[target_col].values
    
    X_seq, y_seq = create_sequences(scaled_features, target_vals, seq_length=seq_length)
    
    train_size = int(len(X_seq) * 0.8)
    X_train_seq = torch.tensor(X_seq[:train_size], dtype=torch.float32)
    y_train_seq = torch.tensor(y_seq[:train_size], dtype=torch.float32).unsqueeze(1)
    X_test_seq = torch.tensor(X_seq[train_size:], dtype=torch.float32)
    y_test_seq = torch.tensor(y_seq[train_size:], dtype=torch.float32).unsqueeze(1)
    
    # 3. Train PyTorch LSTM Model
    model = TrafficLSTM(input_dim=len(feature_cols))
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    logger.info("Training LSTM Model for %d sequences...", len(X_train_seq))
    model.train()
    for epoch in range(1, 11):  # Run 10 epochs for quick capability demonstration
        optimizer.zero_grad()
        output = model(X_train_seq)
        loss = criterion(output, y_train_seq)
        loss.backward()
        optimizer.step()
        if epoch % 2 == 0:
            logger.info("Epoch %d/10 | Loss (MSE): %.4f", epoch, loss.item())
            
    # Evaluate LSTM
    model.eval()
    with torch.no_grad():
        preds = model(X_test_seq)
        mae = torch.mean(torch.abs(preds - y_test_seq)).item()
        logger.info("LSTM Test MAE: %.2f", mae)

    # 4. Model Explainability via SHAP (Applying on XGBoost baseline as proxy per NUS guideline)
    logger.info("--- Computing SHAP Explainability on Baseline Tree Model ---")
    X_tab = df[feature_cols]
    y_tab = df[target_col]
    
    xgb = XGBRegressor(n_estimators=50, random_state=42).fit(X_tab[:train_size], y_tab[:train_size])
    explainer = shap.TreeExplainer(xgb)
    shap_values = explainer(X_tab[train_size:train_size+500]) # Sample 500 records for fast computation
    
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    shap_df = pd.DataFrame({"Feature": feature_cols, "Mean_|SHAP|": mean_abs_shap}).sort_values(by="Mean_|SHAP|", ascending=False)
    
    logger.info("Top Feature Importances (SHAP Attributions):\n%s", shap_df.to_string(index=False))
    return model, shap_df

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/deep_learning.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    from src.data_processing import process_pipeline
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    train_lstm_and_explain(df_processed)