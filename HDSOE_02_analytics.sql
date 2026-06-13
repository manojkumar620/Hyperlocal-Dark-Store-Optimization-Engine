USE darkstore_analytics;

SELECT 
    z.zone_name,
    COUNT(f.order_id) AS total_orders,
    COUNT(CASE WHEN f.operational_status = 'BREACHED_SLA' THEN 1 END) AS delayed_orders,
    ROUND((COUNT(CASE WHEN f.operational_status = 'BREACHED_SLA' THEN 1 END) / COUNT(f.order_id)) * 100, 2) AS delay_percentage
FROM fact_orders f
JOIN dim_zone z ON f.zone_id = z.zone_id
GROUP BY z.zone_name;