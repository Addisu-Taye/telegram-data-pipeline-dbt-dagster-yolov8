SELECT DISTINCT
    ROW_NUMBER() OVER () AS channel_id,
    channel AS channel_name
FROM {{ ref('stg_telegram_messages') }}