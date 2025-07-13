SELECT
    message_id,
    message_text,
    message_date,
    c.channel_id
FROM {{ ref('stg_telegram_messages') }} m
JOIN {{ ref('dim_channels') }} c ON m.channel = c.channel_name