

SELECT DISTINCT
    ROW_NUMBER() OVER () AS channel_id,
    channel AS channel_name
FROM "telegram_data"."raw"."stg_telegram_messages"
WHERE channel IS NOT NULL