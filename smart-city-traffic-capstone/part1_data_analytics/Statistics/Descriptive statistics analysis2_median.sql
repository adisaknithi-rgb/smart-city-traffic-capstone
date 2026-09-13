-- Capstone Part 1: Task 2.1 Median Calculation
WITH OrderedTraffic AS (
    SELECT 
        traffic_volume,
        ROW_NUMBER() OVER (ORDER BY traffic_volume) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM Metro_Interstate_Traffic_Volume
)
SELECT 
    ROUND(AVG(traffic_volume), 2) AS median_volume
FROM OrderedTraffic
WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);