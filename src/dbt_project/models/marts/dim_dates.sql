{{ config(materialized='table') }}

WITH raw_dates AS (
    SELECT DISTINCT
        TO_DATE(message_date, 'YYYY-MM-DD"T"HH24:MI:SS') AS message_date
    FROM {{ ref('stg_telegram_messages') }}
    WHERE message_date IS NOT NULL
),

date_range AS (
    SELECT generate_series(
        (SELECT MIN(message_date) - INTERVAL '1 year' FROM raw_dates),
        (SELECT MAX(message_date) + INTERVAL '1 year' FROM raw_dates),
        INTERVAL '1 day'
    )::DATE AS message_date
)

SELECT
    message_date AS date,
    EXTRACT(YEAR FROM message_date) AS year,
    EXTRACT(QUARTER FROM message_date) AS quarter,
    EXTRACT(MONTH FROM message_date) AS month,
    TO_CHAR(message_date, 'Month') AS month_name,
    EXTRACT(WEEK FROM message_date) AS week_of_year,
    EXTRACT(DAY FROM message_date) AS day_of_month,
    EXTRACT(ISODOW FROM message_date) AS day_of_week,
    TO_CHAR(message_date, 'Day') AS weekday_name,
    CASE WHEN EXTRACT(ISODOW FROM message_date) IN (6,7) THEN TRUE ELSE FALSE END AS is_weekend
FROM (
    SELECT message_date FROM raw_dates
    UNION
    SELECT message_date FROM date_range
) AS all_dates
ORDER BY message_date
