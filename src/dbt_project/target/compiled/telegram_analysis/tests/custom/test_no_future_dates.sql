SELECT *
FROM "telegram_data"."raw"."fct_messages"
WHERE message_date::date > CURRENT_DATE