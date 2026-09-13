-- คำนวณ Pearson Correlation Coefficient (r) ข้อมูลทั้งหมด 48,204 แถว
SELECT 
    COUNT(*) AS total_records,
    ROUND(
        (COUNT(*) * SUM(temp * traffic_volume) - SUM(temp) * SUM(traffic_volume)) /
        (SQRT(COUNT(*) * SUM(temp * temp) - SUM(temp) * SUM(temp)) *
         SQRT(COUNT(*) * SUM(traffic_volume * traffic_volume) - SUM(traffic_volume) * SUM(traffic_volume))),
    4) AS pearson_r_raw
FROM Metro_Interstate_Traffic_Volume;