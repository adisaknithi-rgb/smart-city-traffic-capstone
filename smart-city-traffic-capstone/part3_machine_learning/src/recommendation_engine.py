import os
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def generate_travel_recommendation(df: pd.DataFrame, day_type: str = "Weekday", weather_condition: str = "Clear") -> dict:
    """
    Task 5: Traffic Timing Recommendation System
    ค้นหาช่วงเวลาเดินทางที่ปริมาณจราจรต่ำที่สุดตามประเภทวันและสภาพอากาศ
    """
    logger.info("--- Starting Task 5: Recommendation System Execution ---")
    logger.info("Searching optimal window for Day Type: '%s' | Weather: '%s'", day_type, weather_condition)
    
    # 1. กรองประเภทวัน (Weekday vs Weekend)
    if day_type.lower() == "weekday":
        filtered_df = df[df["date_time"].dt.dayofweek < 5].copy()
    else:
        filtered_df = df[df["date_time"].dt.dayofweek >= 5].copy()
        
    # 2. กรองสภาพอากาศ (ถ้าไม่มีข้อมูลตรงเป้า ให้ใช้ข้อมูลรวมของประเภทวันนั้น)
    weather_match = filtered_df[filtered_df["weather_main"].str.lower() == weather_condition.lower()]
    if not weather_match.empty:
        filtered_df = weather_match
    else:
        logger.warning("Weather condition '%s' not found. Falling back to all weather types for %s.", weather_condition, day_type)
        
    # 3. คำนวณปริมาณจราจรเฉลี่ยแยกตามชั่วโมง (เน้นช่วงเวลากลางวัน/กะทำงาน 07:00 - 19:00 น.)
    hourly_stats = filtered_df.groupby(filtered_df["date_time"].dt.hour)["traffic_volume"].mean().reset_index()
    hourly_stats.columns = ["hour", "avg_traffic_volume"]
    
    daytime_stats = hourly_stats[(hourly_stats["hour"] >= 7) & (hourly_stats["hour"] <= 19)]
    
    best_row = daytime_stats.loc[daytime_stats["avg_traffic_volume"].idxmin()]
    best_hour = int(best_row["hour"])
    min_volume = float(best_row["avg_traffic_volume"])
    
    start_time_str = f"{best_hour:02d}:00"
    end_time_str = f"{(best_hour + 1):02d}:00"
    
    # 4. สร้างข้อความแนะนำภาษาธรรมชาติ (Plain-Language Recommendation)
    rec_text = (
        f"For a {day_type.lower()} journey under {weather_condition.lower()} weather, "
        f"consider travelling between {start_time_str} and {end_time_str}, "
        f"when historical traffic volumes are typically at their lowest daytime level (avg. {int(min_volume)} vehicles/hr)."
    )
    
    logger.info("Generated Recommendation: %s", rec_text)
    
    return {
        "day_type": day_type,
        "weather_condition": weather_condition,
        "recommended_window": f"{start_time_str} - {end_time_str}",
        "avg_volume": min_volume,
        "plain_language_recommendation": rec_text
    }

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/recommendation_engine.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    from src.data_processing import process_pipeline
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    
    # ทดสอบประมวลผลคำแนะนำ 2 สถานการณ์
    rec1 = generate_travel_recommendation(df_processed, day_type="Weekday", weather_condition="Clear")
    rec2 = generate_travel_recommendation(df_processed, day_type="Weekday", weather_condition="Rain")
    
    print("\n--- SAMPLE RECOMMENDATION OUTPUTS ---")
    print(f"[Clear Weather]: {rec1['plain_language_recommendation']}")
    print(f"[Rainy Weather]: {rec2['plain_language_recommendation']}")
    
    logger.info("Task 5 completed successfully. Audit log saved to logs/recommendation_engine.log")