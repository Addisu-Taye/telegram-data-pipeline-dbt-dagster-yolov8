
  create view "telegram_data"."public"."stg_telegram_messages__dbt_tmp"
    
    
  as (
    WITH raw_data AS (
    SELECT * FROM "telegram_data"."public"."telegram_messages"
)
SELECT
    (message_json->>'id')::INT AS message_id,
    message_json->>'message' AS message_text,  -- Changed from 'text' to 'message'
    message_json->>'date' AS message_date,
    channel
FROM raw_data
WHERE message_json->>'message' IS NOT NULL  -- Changed from 'text' to 'message'
  );