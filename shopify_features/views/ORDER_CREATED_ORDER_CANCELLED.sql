create or replace view RUDDERSTACK_TEST_DB.DATA_APPS_SIMULATED_SHOPIFY.ORDER_CREATED_ORDER_CANCELLED(
	ANONYMOUS_ID,
	USER_ID,
	TOTAL_PRICE_USD,
	PRODUCTS,
	PAYMENT_DETAILS_CREDIT_CARD_COMPANY,
	ORDER_NUMBER,
	TIMESTAMP,
	CART_TOKEN,
	FULFILLMENT_STATUS,
	FINANCIAL_STATUS,
	ANONYMOUS_ID_ORDER_CANCELLED,
	USER_ID_ORDER_CANCELLED,
	TOTAL_PRICE_USD_ORDER_CANCELLED,
	ORDER_NUMBER_ORDER_CANCELLED,
	FINANCIAL_STATUS_ORDER_CANCELLED,
	CART_TOKEN_ORDER_CANCELLED,
	TIMESTAMP_ORDER_CANCELLED,
	PRODUCTS_ORDER_CANCELLED
) as 

with order_status as  
(select 
a.ANONYMOUS_ID,
a.user_id,
a.total_price_usd,
a.products,
 a.payment_details_credit_card_company,
 a.order_number,
 a.timestamp,
 a.cart_token,
 a.fulfillment_status,
 a.financial_status,
 b.anonymous_id as anonymous_id_order_cancelled,
 b.user_id as user_id_order_cancelled ,
 b.total_price_usd as total_price_usd_order_cancelled,
 b.order_number as order_number_order_cancelled,
 b.financial_status as financial_status_order_cancelled,
 b.cart_token as cart_token_order_cancelled,
 b.timestamp as timestamp_order_cancelled,
 b.products as products_order_cancelled 
 from order_created a left join order_cancelled b 
 on a.user_id = b.user_id and a.order_number = b.order_number)
 select * from order_status;