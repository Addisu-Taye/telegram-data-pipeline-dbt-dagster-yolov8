SELECT
    message_id,
    message_text,
    message_date,
    c.channel_id
FROM "telegram_data"."public"."stg_telegram_messages" m
JOIN "telegram_data"."public"."dim_channels" c ON m.channel = c.channel_name