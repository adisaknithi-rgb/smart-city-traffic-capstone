import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# รายการสภาพอากาศรุนแรงตามข้อกำหนด NUS
SEVERE_WEATHER = ['Thunderstorm', 'Squall', 'Tornado', 'Snow', 'Fog']

def create_proxy_label(df: pd.DataFrame) -> pd.DataFrame:
    """สร้าง Proxy Accident-Risk Label (high_risk) ตามข้อกำหนด NUS Part 3"""
    logger.info("Starting proxy accident-risk label construction...")
    df = df.copy()

    # 1. สร้าง congestion_category จาก Quartiles ของ traffic_volume
    q1, q2, q3 = df["traffic_volume"].quantile([0.25, 0.5, 0.75]).values
    
    def bucket(v):
        if v <= q1:
            return "Low"
        elif v <= q2:
            return "Medium"
        elif v <= q3:
            return "High"
        return "Severe"

    df["congestion_category"] = df["traffic_volume"].apply(bucket)
    logger.info("Congestion categories generated using Q1=%.1f, Q2=%.1f, Q3=%.1f", q1, q2, q3)

    # 2. ตรวจสอบเงื่อนไขสภาพอากาศเสี่ยง (Risky Weather)
    if "is_low_visibility" not in df.columns:
        df["is_low_visibility"] = df["visibility"].apply(lambda x: 1 if x < 5000 else 0) if "visibility" in df.columns else 0

    high_congestion = df["congestion_category"].isin(["High", "Severe"])
    risky_weather = (
        df["weather_main"].isin(SEVERE_WEATHER) 
        | (df["is_low_visibility"] == 1)
    )

    # 3. กำหนด Proxy Target
    df["high_risk"] = (high_congestion & risky_weather).astype(int)
    
    high_risk_cnt = df["high_risk"].sum()
    pct = (high_risk_cnt / len(df)) * 100
    logger.info("Proxy label successfully generated: %d high_risk records (%.2f%%)", high_risk_cnt, pct)

    if high_risk_cnt == 0:
        logger.warning("No high_risk cases detected! Verify SEVERE_WEATHER categories and visibility threshold.")

    return df

def add_time_and_cyclical_features(df: pd.DataFrame) -> pd.DataFrame:
    """สร้าง Time-based และ Cyclical Encodings สำหรับ Task 1"""
    logger.info("Adding time-based and cyclical encodings (sin/cos)...")
    df = df.copy()
    
    # ตรวจสอบแปลง date_time เป็น datetime object
    if not pd.api.types.is_datetime64_any_dtype(df['date_time']):
        df['date_time'] = pd.to_datetime(df['date_time'])
        
    df['hour'] = df['date_time'].dt.hour
    df['dayofweek'] = df['date_time'].dt.dayofweek
    
    # Cyclical Encoding สำหรับ Hour (24-hour cycle) และ Day of Week (7-day cycle)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7.0)
    
    logger.info("Cyclical features added: hour_sin, hour_cos, day_sin, day_cos")
    return df

def process_pipeline(file_path: str) -> pd.DataFrame:
    """Master Pipeline สกัดและเตรียม Dataframe พร้อมใช้สำหรับ Task 1"""
    logger.info("Loading dataset from %s", file_path)
    df = pd.read_csv(file_path)
    
    df = add_time_and_cyclical_features(df)
    df = create_proxy_label(df)
    
    return df

if __name__ == "__main__":
    # บล็อกสำหรับทดสอบรันสคริปต์นี้โดยตรงจาก Terminal
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    logger.info("Testing data_processing module directly...")
    
    # ทดลองประมวลผลไฟล์ข้อมูล
    data_path = "data/featured_traffic_data.csv"
    try:
        processed_df = process_pipeline(data_path)
        logger.info("Pipeline completed successfully. Dataset shape: %s", str(processed_df.shape))
    except Exception as e:
        logger.error("Failed to run pipeline: %s", str(e), exc_info=True)