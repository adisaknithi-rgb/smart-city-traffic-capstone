-- Solution: Querying by calendar dates (Jan 1 & 1st Mon of Sep) 
-- to capture all 24 hours regardless of holiday column tagging
SELECT 
    CASE 
        WHEN strftime('%m-%d', date_time) = '01-01' THEN 'New Year''s Day'
        ELSE 'Labor Day'
    END AS holiday_name,
    strftime('%Y', date_time) AS year,
    ROUND(AVG(temp), 2) AS avg_temp_kelvin,
    ROUND(AVG(temp) - 273.15, 2) AS avg_temp_celsius,
    ROUND(AVG(traffic_volume), 0) AS avg_hourly_traffic
FROM Metro_Interstate_Traffic_Volume
WHERE (strftime('%m-%d', date_time) = '01-01' -- New Year's Day
   OR (strftime('%m', date_time) = '09' AND strftime('%w', date_time) = '1' AND CAST(strftime('%d', date_time) AS INT) <= 7)) -- Labor Day (First Mon of Sep)
  AND strftime('%Y', date_time) IN ('2015', '2016', '2017')
GROUP BY holiday_name, year
ORDER BY holiday_name, year ASC;