-- Capstone Part 1: Task 2.2 Pearson Correlation Analysis (Cleaned Dataset)
SELECT 
    COUNT(*) AS total_records_cleaned,
    ROUND(
        (COUNT(*) * SUM(temp * traffic_volume) - SUM(temp) * SUM(traffic_volume)) /
        (SQRT(COUNT(*) * SUM(temp * temp) - SUM(temp) * SUM(temp)) *
         SQRT(COUNT(*) * SUM(traffic_volume * traffic_volume) - SUM(traffic_volume) * SUM(traffic_volume))),
    4) AS pearson_r_cleaned
FROM Metro_Interstate_Traffic_Volume
WHERE temp > 200;