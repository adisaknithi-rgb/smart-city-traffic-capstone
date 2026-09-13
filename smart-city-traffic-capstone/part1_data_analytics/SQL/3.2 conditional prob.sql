-- Capstone Part 1: Task 3.2 Conditional Probabilities & Contingency Counts
SELECT 
    -- 1. Base Congestion Count
    SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END) AS n_Congestion,
    
    -- 2. P(Clear Weather | Congestion)
    ROUND(CAST(SUM(CASE WHEN traffic_volume > 5500 AND weather_main = 'Clear' THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END), 4) AS P_Clear_given_Congestion,
          
    -- 3. P(High Temperature > 292K | Congestion)
    ROUND(CAST(SUM(CASE WHEN traffic_volume > 5500 AND temp > 292 THEN 1 ELSE 0 END) AS FLOAT) / 
          SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END), 4) AS P_HighTemp_given_Congestion,

    -- 4. Contingency Table for Odds Ratio (Clear vs Clouds)
    SUM(CASE WHEN weather_main = 'Clear' AND traffic_volume > 5500 THEN 1 ELSE 0 END) AS a_Clear_Congest,
    SUM(CASE WHEN weather_main = 'Clear' AND traffic_volume <= 5500 THEN 1 ELSE 0 END) AS b_Clear_NoCongest,
    SUM(CASE WHEN weather_main = 'Clouds' AND traffic_volume > 5500 THEN 1 ELSE 0 END) AS c_Clouds_Congest,
    SUM(CASE WHEN weather_main = 'Clouds' AND traffic_volume <= 5500 THEN 1 ELSE 0 END) AS d_Clouds_NoCongest
FROM Metro_Interstate_Traffic_Volume
WHERE temp > 200;