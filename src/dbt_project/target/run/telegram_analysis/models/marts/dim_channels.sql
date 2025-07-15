
  
    

  create  table "telegram_data"."public"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    

SELECT DISTINCT
    ROW_NUMBER() OVER () AS channel_id,
    channel AS channel_name
FROM "telegram_data"."public"."stg_telegram_messages"
WHERE channel IS NOT NULL
  );
  