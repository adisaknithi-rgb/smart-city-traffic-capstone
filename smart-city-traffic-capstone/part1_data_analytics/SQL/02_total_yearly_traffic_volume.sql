-- Capstone Part 1: Task 1.2 Annual Traffic Trend Analysis
-- Objective: Aggregating yearly traffic metrics (2012-2017)
SELECT 
    strftime('%Y', date_time) AS year,
    COUNT(*) AS total_hours_recorded,
    SUM(traffic_volume) AS total_traffic_volume,
    ROUND(AVG(traffic_volume), 0) AS avg_traffic_volume
FROM Metro_Interstate_Traffic_Volume
WHERE strftime('%Y', date_time) BETWEEN '2012' AND '2017'
GROUP BY year
ORDER BY year ASC;