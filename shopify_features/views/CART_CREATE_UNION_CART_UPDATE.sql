create or replace view RUDDERSTACK_TEST_DB.DATA_APPS_SIMULATED_SHOPIFY.CART_CREATE_UNION_CART_UPDATE(
	ANONYMOUS_ID,
	TOKEN,
	PRODUCTS,
	TIMESTAMP
) as

select anonymous_id, token, to_char(products), timestamp from cart_update
union all
select anonymous_id, token, to_char(products), timestamp from cart_create;