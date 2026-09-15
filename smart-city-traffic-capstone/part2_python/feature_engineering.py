import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler

# ตั้งค่า Logger (กำหนดเป็น INFO เป็นค่าเริ่มต้น)
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#logger = logging.getLogger(__name__)
# ปรับระดับเป็น DEBUG และระบุ Handlers ให้เขียนลงไฟล์ pipeline.log พร้อมแสดงบน Terminal
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Log Shape ก่อนทำ Feature Engineering (ตามข้อกำหนด NUS)
    logger.info(f"Dataset shape BEFORE feature engineering: {df.shape}")
    
    df_feat = df.copy()
    df_feat['date_time'] = pd.to_datetime(df_feat['date_time'])
    df_feat = df_feat.sort_values('date_time').reset_index(drop=True)
    
    # --- [1. Time Features & Cyclical Encoding] ---
    df_feat['hour'] = df_feat['date_time'].dt.hour
    df_feat['day_of_week'] = df_feat['date_time'].dt.dayofweek
    df_feat['is_weekend'] = df_feat['day_of_week'].isin([5, 6]).astype(int)
    
    # Cyclical Encoding สำหรับ 24 ชั่วโมง (0-23)
    df_feat['hour_sin'] = np.sin(2 * np.pi * df_feat['hour'] / 24.0)
    df_feat['hour_cos'] = np.cos(2 * np.pi * df_feat['hour'] / 24.0)
    
    # --- [2. Weather Features] ---
    # One-Hot Encoding สำหรับ Categorical Weather
    weather_dummies = pd.get_dummies(df_feat['weather_main'], prefix='weather', drop_first=True)
    df_feat = pd.concat([df_feat, weather_dummies], axis=1)
    
    # Derived Weather Indicator
    df_feat['temp_celsius'] = df_feat['temp'] - 273.15
    df_feat['is_severe_weather'] = df_feat['weather_main'].isin(['Thunderstorm', 'Squall', 'Snow']).astype(int)
    
    # --- [3. Numerical Scaling] ---
    scaler = StandardScaler()
    scaled_cols = scaler.fit_transform(df_feat[['temp', 'rain_1h']])
    df_feat['temp_scaled'] = scaled_cols[:, 0]
    df_feat['rain_scaled'] = scaled_cols[:, 1]
    
    # --- [4. Data-driven Target Categorization & DEBUG Logging] ---
    # คำนวณ Quantile Thresholds สำหรับจัดกลุ่ม Traffic Congestion
    q33 = df_feat['traffic_volume'].quantile(0.33)
    q66 = df_feat['traffic_volume'].quantile(0.66)
    
    # Log ค่า Thresholds ในระดับ DEBUG (จะไม่โชว์ในโหมดปกติ ตาม Rubric NUS)
    logger.debug(f"Intermediate Quantile Thresholds - Q1 (33rd): {q33:.2f}, Q2 (66th): {q66:.2f}")
    
    # สร้าง Categorical Target (Low, Medium, High) ด้วย pd.qcut
    labels = ['Low', 'Medium', 'High']
    df_feat['congestion_level'] = pd.qcut(df_feat['traffic_volume'], q=[0, 0.33, 0.66, 1.0], labels=labels)
    
    # --- [5. Lag & Rolling Features] ---
    df_feat['traffic_lag_1h'] = df_feat['traffic_volume'].shift(1)
    df_feat['traffic_rolling_mean_3h'] = df_feat['traffic_volume'].shift(1).rolling(window=3).mean()
    
    # ลบเฉพาะแถวที่เป็น NaN จากการทำ Lag/Rolling (3 แถวแรก)
    df_feat.dropna(subset=['traffic_lag_1h', 'traffic_rolling_mean_3h'], inplace=True)
    
    # Log Shape หลังทำ Feature Engineering (ตามข้อกำหนด NUS)
    logger.info(f"Dataset shape AFTER feature engineering: {df_feat.shape}")
    
    return df_feat

if __name__ == "__main__":
    logger.info("Starting Task 2: Feature Engineering Module...")
    
    # โหลดข้อมูลที่ clean แล้ว
    raw_df = pd.read_csv("cleaned_traffic_data.csv")
    
    # ประมวลผลสร้าง Features
    featured_df = create_features(raw_df)
    
    # บันทึกไฟล์ผลลัพธ์
    featured_df.to_csv("featured_traffic_data.csv", index=False)
    logger.info("Successfully exported fully engineered dataset to 'featured_traffic_data.csv'.")