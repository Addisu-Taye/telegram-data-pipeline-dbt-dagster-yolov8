
    
    

select
    channel_name as unique_field,
    count(*) as n_records

from "telegram_data"."raw"."dim_channels"
where channel_name is not null
group by channel_name
having count(*) > 1


