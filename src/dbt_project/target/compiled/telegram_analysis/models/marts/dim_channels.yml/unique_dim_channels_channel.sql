
    
    

select
    channel as unique_field,
    count(*) as n_records

from "telegram_data"."raw"."dim_channels"
where channel is not null
group by channel
having count(*) > 1


