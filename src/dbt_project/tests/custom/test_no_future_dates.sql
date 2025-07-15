SELECT *
FROM {{ ref('fct_messages') }}
WHERE message_date::date > CURRENT_DATE
