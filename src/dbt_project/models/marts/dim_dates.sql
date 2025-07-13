-- File Path: src/dbt_project/models/marts/dim_dates.sql
-- Date: 10 July 2025
-- Developed by: Addisu Taye Dadi
-- Purpose: Create a date dimension table to support time-based analysis in the data warehouse.
-- Key Features:
-- - Generates a full calendar of dates with attributes useful for reporting and analytics.
-- - Includes year, quarter, month, week, day, and weekday information.
-- - Used as a dimension table joined to fact tables like fct_messages.

{{ config(materialized='table') }}

WITH date_spine AS (
    -- Generate a list of all unique message dates from the staging messages table
    SELECT DISTINCT
        (TO_DATE(message_date::text, 'YYYY-MM-DD')) AS date
    FROM {{ ref('stg_telegram_messages') }}
    WHERE message_date IS NOT NULL

    UNION

    -- Optional: Add future dates or fill gaps using a date range
    SELECT generate_series(
        (SELECT MIN(TO_DATE(message_date::text, 'YYYY-MM-DD')) - INTERVAL '1 year' FROM {{ ref('stg_telegram_messages') }}),
        (SELECT MAX(TO_DATE(message_date::text, 'YYYY-MM-DD')) + INTERVAL '1 year'),
        INTERVAL '1 day'
    )::DATE
)

SELECT
    date,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(MONTH FROM date) AS month,
    TO_CHAR(date, 'Month') AS month_name,
    EXTRACT(WEEK FROM date) AS week_of_year,
    EXTRACT(DAY FROM date) AS day_of_month,
    EXTRACT(ISODOW FROM date) AS day_of_week, -- Monday = 1, Sunday = 7
    TO_CHAR(date, 'Day') AS weekday_name,
    CASE WHEN EXTRACT(ISODOW FROM date) IN (6,7) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine
ORDER BY date