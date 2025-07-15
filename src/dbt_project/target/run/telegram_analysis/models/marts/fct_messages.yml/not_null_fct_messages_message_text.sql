
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_text
from "telegram_data"."raw"."fct_messages"
where message_text is null



  
  
      
    ) dbt_internal_test