-- Capstone Part 1: Task 3.1 Basic Probability Analysis
SELECT 
    COUNT(*) AS Total_N,
    
    -- Absolute Counts (n)
    SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END) AS n_Congestion,
    SUM(CASE WHEN weather_main = 'Clear' THEN 1 ELSE 0 END) AS n_Clear,
    SUM(CASE WHEN traffic_volume > 5500 AND weather_main = 'Clear' THEN 1 ELSE 0 END) AS n_Congestion_AND_Clear,
    
    -- Probabilities (P)
    ROUND(CAST(SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*), 4) AS P_Congestion,
    ROUND(CAST(SUM(CASE WHEN weather_main = 'Clear' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*), 4) AS P_Clear,
    ROUND(CAST(SUM(CASE WHEN traffic_volume > 5500 AND weather_main = 'Clear' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*), 4) AS P_Congestion_AND_Clear
FROM Metro_Interstate_Traffic_Volume;