WITH raw_data AS (
    SELECT * FROM "telegram_data"."public"."telegram_messages"
)

SELECT
    (message_json->>'id')::INT AS message_id,
    message_json->>'text' AS message_text,
    message_json->>'date' AS message_date,
    channel  -- Make sure this line exists
FROM raw_data
WHERE message_json->>'text' IS NOT NULL