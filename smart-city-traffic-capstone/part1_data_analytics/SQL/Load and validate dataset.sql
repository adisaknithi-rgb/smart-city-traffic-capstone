-- Capstone Part 1: Task 1.2 Annual Traffic Trend Analysis
-- ==========================================================
-- Capstone Part 1: Task 1.1 Data Ingestion & Verification
-- Project: Metro Interstate Traffic Volume
-- Author: Emergency Medicine AI Researcher (Vajira Hospital)
-- ==========================================================

-- 1. Verify Table Schema & Column Data Types
PRAGMA table_info("Metro_Interstate_Traffic_Volume");

-- 2. Verify Data Completeness (Expected: 48,205 rows)
SELECT COUNT(*) AS total_records 
FROM "Metro_Interstate_Traffic_Volume";

-- 3. Sample Data Inspection (First 5 records)
SELECT * 
FROM "Metro_Interstate_Traffic_Volume" 
LIMIT 5;

-- 4. Verify Data Missingness (Check NULL counts for all columns)
SELECT 
    COUNT(*) - COUNT(date_time) AS missing_date_time,
    COUNT(*) - COUNT(traffic_volume) AS missing_traffic_volume,
    COUNT(*) - COUNT(temp) AS missing_temp,
    COUNT(*) - COUNT(holiday) AS missing_holiday,
    COUNT(*) - COUNT(rain_1h) AS missing_rain_1h,
    COUNT(*) - COUNT(snow_1h) AS missing_snow_1h,
    COUNT(*) - COUNT(clouds_all) AS missing_clouds_all,
    COUNT(*) - COUNT(weather_main) AS missing_weather_main,
    COUNT(*) - COUNT(weather_description) AS missing_weather_description
FROM "Metro_Interstate_Traffic_Volume";