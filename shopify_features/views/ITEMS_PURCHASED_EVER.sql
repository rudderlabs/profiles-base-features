create or replace view RUDDERSTACK_TEST_DB.DATA_APPS_SIMULATED_SHOPIFY.ITEMS_PURCHASED_EVER as 

with sku as (select t.value['sku'] as SKU,products,token,ANONYMOUS_ID,USER_ID,TIMESTAMP,order_number
from (select * from order_created ), table(flatten(parse_json(products))) t where products is not null),

cte AS (
   SELECT *
        , row_number() OVER (PARTITION BY token ORDER BY timestamp DESC) AS rn
   FROM   sku
   )
SELECT *
FROM   cte
WHERE  rn = 1;