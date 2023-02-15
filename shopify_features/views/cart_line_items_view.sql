create or replace view RUDDERSTACK_TEST_DB.DATA_APPS_SIMULATED_SHOPIFY.CART_LINE_ITEMS(
		BRAND,
		DISCOUNTED_PRICE,
		GIFT_CARD,
		GRAMS,
		ID,
		KEY,
		LINE_PRICE,
		ORIGINAL_LINE_PRICE,
		ORIGINAL_PRICE,
		PRICE,
		PRODUCT_ID,
		PROPERTIES,
		QUANTITY,
		SKU,
		TAXABLE,
		TITLE,
		TOTAL_DISCOUNT,
		_VARIANT_,
		PRODUCTS,
		ANONYMOUS_ID,
		TIMESTAMP,
		TOKEN,
		RN
	) as WITH cart_items as (
		select to_char(t.value ['brand']) as brand,
			t.value ['discounted_price']::real as discounted_price,
			to_char(t.value ['gift_card']) as gift_card,
			t.value ['grams']::real as grams,
			to_char(t.value ['id']) as id,
			to_char(t.value ['key']) as key,
			t.value ['line_price']::real as line_price,
			t.value ['original_line_price']::real as original_line_price,
			t.value ['original_price']::real as original_price,
			t.value ['price']::real as price,
			to_char(t.value ['product_id']) as product_id,
			to_char(t.value ['properties']) as properties,
			t.value ['quantity']::real as quantity,
			to_char(t.value ['sku']) as sku,
			to_char(t.value ['taxable']) as taxable,
			to_char(t.value ['title']) as title,
			t.value ['total_discount']::real as total_discount,
			to_char(t.value ['variant']) as _VARIANT_,
			products,
			anonymous_id,
			timestamp,
			token
		from (
				select *
				from cart_update
			),
			table(flatten(parse_json(products))) t
		where products is not null
	),
	cte AS (
		SELECT *,
			row_number() OVER (
				PARTITION BY token
				ORDER BY timestamp DESC
			) AS rn
		FROM cart_items
	)
SELECT *
FROM cte
WHERE rn = 1;