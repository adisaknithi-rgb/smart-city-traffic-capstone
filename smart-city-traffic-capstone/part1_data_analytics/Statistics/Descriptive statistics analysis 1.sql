-- Capstone Part 1: Task 2.1 Basic Descriptive Statistics & Variance
SELECT 
    COUNT(traffic_volume) AS total_n,
    ROUND(AVG(traffic_volume), 2) AS mean_volume,
    MIN(traffic_volume) AS min_volume,
    MAX(traffic_volume) AS max_volume,
    (MAX(traffic_volume) - MIN(traffic_volume)) AS range_volume,
    
    -- Sample Variance Formula in SQL
    ROUND(
        (SUM(traffic_volume * traffic_volume) - (SUM(traffic_volume) * SUM(traffic_volume) / COUNT(traffic_volume))) 
        / (COUNT(traffic_volume) - 1.0), 
    2) AS variance_volume,
    
    -- Sample Standard Deviation Formula in SQL (SQRT of Variance)
    ROUND(
        SQRT(
            (SUM(traffic_volume * traffic_volume) - (SUM(traffic_volume) * SUM(traffic_volume) / COUNT(traffic_volume))) 
            / (COUNT(traffic_volume) - 1.0)
        ), 
    2) AS std_dev_volume
FROM Metro_Interstate_Traffic_Volume;