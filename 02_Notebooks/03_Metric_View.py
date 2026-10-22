# Databricks notebook source
# DBTITLE 1,Create the metric view for semantic layer
# MAGIC
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW quicksight_retail.quicksight_retail_semantic.retail_metrics
# MAGIC WITH METRICS
# MAGIC LANGUAGE YAML
# MAGIC AS $$
# MAGIC version: 1.1
# MAGIC
# MAGIC source: quicksight_retail.quicksight_retail_gold.fact_sales
# MAGIC comment: Retail sales metrics for analyzing revenue, transactions, products, customers, and sales performance.
# MAGIC
# MAGIC joins:
# MAGIC   - name: product
# MAGIC     source: quicksight_retail.quicksight_retail_gold.dim_product
# MAGIC     on: source.product_id = product.product_id
# MAGIC
# MAGIC   - name: calendar
# MAGIC     source: quicksight_retail.quicksight_retail_gold.dim_calendar
# MAGIC     on: source.transaction_date = calendar.date
# MAGIC
# MAGIC   - name: customer
# MAGIC     source: quicksight_retail.quicksight_retail_gold.dim_customer
# MAGIC     on: source.customer_id = customer.customer_id
# MAGIC
# MAGIC fields:
# MAGIC   - name: transaction_date
# MAGIC     expr: calendar.date
# MAGIC     display_name: Transaction Date
# MAGIC     comment: Date when the transaction occurred.
# MAGIC     format:
# MAGIC       type: date
# MAGIC       date_format: year_month_day
# MAGIC     synonyms:
# MAGIC       - date
# MAGIC       - sale date
# MAGIC       - transaction day
# MAGIC
# MAGIC   - name: transaction_month
# MAGIC     expr: CAST(DATE_TRUNC('MONTH', source.transaction_date) AS DATE)
# MAGIC     display_name: Transaction Month
# MAGIC     comment: First calendar day of the transaction month.
# MAGIC     format:
# MAGIC       type: date
# MAGIC       date_format: year_month_day
# MAGIC     synonyms:
# MAGIC       - sales month
# MAGIC       - monthly sales
# MAGIC
# MAGIC   - name: year
# MAGIC     expr: calendar.year
# MAGIC     display_name: Year
# MAGIC     comment: Calendar year of the transaction.
# MAGIC
# MAGIC   - name: quarter
# MAGIC     expr: calendar.quarter
# MAGIC     display_name: Quarter
# MAGIC     comment: Calendar quarter of the transaction.
# MAGIC
# MAGIC   - name: month_name
# MAGIC     expr: calendar.month_name
# MAGIC     display_name: Month
# MAGIC     comment: Name of the transaction month.
# MAGIC     synonyms:
# MAGIC       - month
# MAGIC
# MAGIC   - name: product_category
# MAGIC     expr: product.category
# MAGIC     display_name: Product Category
# MAGIC     comment: Main category of the product sold.
# MAGIC     synonyms:
# MAGIC       - category
# MAGIC
# MAGIC   - name: product_subcategory
# MAGIC     expr: product.subcategory
# MAGIC     display_name: Product Subcategory
# MAGIC     comment: Subcategory of the product sold.
# MAGIC
# MAGIC   - name: product_brand
# MAGIC     expr: product.brand
# MAGIC     display_name: Product Brand
# MAGIC     comment: Brand of the product sold.
# MAGIC     synonyms:
# MAGIC       - brand
# MAGIC
# MAGIC   - name: payment_mode
# MAGIC     expr: source.payment_mode
# MAGIC     display_name: Payment Mode
# MAGIC     comment: Payment method used for the transaction.
# MAGIC     synonyms:
# MAGIC       - payment method
# MAGIC       - payment type
# MAGIC
# MAGIC   - name: sales_channel
# MAGIC     expr: source.sales_channel
# MAGIC     display_name: Sales Channel
# MAGIC     comment: Channel through which the sale was made.
# MAGIC     synonyms:
# MAGIC       - channel
# MAGIC
# MAGIC   - name: stage_name
# MAGIC     expr: source.stage_name
# MAGIC     display_name: Opportunity Stage
# MAGIC     comment: Sales opportunity stage.
# MAGIC
# MAGIC   - name: customer_type
# MAGIC     expr: customer.customer_type
# MAGIC     display_name: Customer Type
# MAGIC     comment: Type or segment of the customer.
# MAGIC     synonyms:
# MAGIC       - customer segment
# MAGIC       - customer category
# MAGIC
# MAGIC   - name: customer_name
# MAGIC     expr: customer.customer_name
# MAGIC     display_name: Customer Name
# MAGIC     comment: Name of the purchasing customer.
# MAGIC     synonyms:
# MAGIC       - customer
# MAGIC
# MAGIC   - name: billing_city
# MAGIC     expr: customer.billing_city
# MAGIC     display_name: Billing City
# MAGIC     comment: Customer billing city.
# MAGIC     synonyms:
# MAGIC       - city
# MAGIC       - customer city
# MAGIC
# MAGIC   - name: billing_state
# MAGIC     expr: customer.billing_state
# MAGIC     display_name: Billing State
# MAGIC     comment: Customer billing state.
# MAGIC     synonyms:
# MAGIC       - state
# MAGIC       - customer state
# MAGIC
# MAGIC   - name: billing_country
# MAGIC     expr: customer.billing_country
# MAGIC     display_name: Billing Country
# MAGIC     comment: Customer billing country.
# MAGIC     synonyms:
# MAGIC       - country
# MAGIC       - customer country
# MAGIC
# MAGIC   - name: customer_industry
# MAGIC     expr: customer.industry
# MAGIC     display_name: Customer Industry
# MAGIC     comment: Industry sector of the customer.
# MAGIC     synonyms:
# MAGIC       - industry
# MAGIC       - sector
# MAGIC
# MAGIC measures:
# MAGIC   - name: transaction_count
# MAGIC     expr: COUNT(1)
# MAGIC     display_name: Transaction Count
# MAGIC     comment: Number of rows in the fact table. Represents transactions only when each row is one transaction.
# MAGIC     format:
# MAGIC       type: number
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 0
# MAGIC     synonyms:
# MAGIC       - transactions
# MAGIC       - transaction rows
# MAGIC       - order count
# MAGIC
# MAGIC   - name: total_revenue
# MAGIC     expr: SUM(source.amount)
# MAGIC     display_name: Total Revenue
# MAGIC     comment: Sum of transaction amounts.
# MAGIC     format:
# MAGIC       type: currency
# MAGIC       currency_code: USD
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 2
# MAGIC     synonyms:
# MAGIC       - revenue
# MAGIC       - sales
# MAGIC       - total sales
# MAGIC
# MAGIC   - name: total_quantity
# MAGIC     expr: SUM(source.quantity)
# MAGIC     display_name: Total Quantity Sold
# MAGIC     comment: Total units sold across all transactions.
# MAGIC     format:
# MAGIC       type: number
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 0
# MAGIC     synonyms:
# MAGIC       - quantity
# MAGIC       - units sold
# MAGIC
# MAGIC   - name: total_discount
# MAGIC     expr: SUM(source.discount_amount)
# MAGIC     display_name: Total Discount
# MAGIC     comment: Total discount amount across transactions.
# MAGIC     format:
# MAGIC       type: currency
# MAGIC       currency_code: USD
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 2
# MAGIC     synonyms:
# MAGIC       - discounts
# MAGIC       - discount amount
# MAGIC
# MAGIC   - name: avg_transaction_value
# MAGIC     expr: SUM(source.amount) / NULLIF(COUNT(1), 0)
# MAGIC     display_name: Average Transaction Value
# MAGIC     comment: Average revenue per fact-table row.
# MAGIC     format:
# MAGIC       type: currency
# MAGIC       currency_code: USD
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 2
# MAGIC     synonyms:
# MAGIC       - average revenue
# MAGIC       - avg revenue
# MAGIC
# MAGIC   - name: unique_customers
# MAGIC     expr: COUNT(DISTINCT customer.customer_id)
# MAGIC     display_name: Unique Customers
# MAGIC     comment: Number of distinct customers represented in the filtered data.
# MAGIC     format:
# MAGIC       type: number
# MAGIC       decimal_places:
# MAGIC         type: exact
# MAGIC         places: 0
# MAGIC     synonyms:
# MAGIC       - customer count
# MAGIC       - distinct customers
# MAGIC $$
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(customer.customer_id) AS matched_customers
# MAGIC FROM quicksight_retail.quicksight_retail_gold.fact_sales source
# MAGIC LEFT JOIN quicksight_retail.quicksight_retail_gold.dim_customer customer
# MAGIC     ON source.customer_id = customer.customer_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     MEASURE(transaction_count) AS transaction_count,
# MAGIC     MEASURE(total_revenue) AS total_revenue,
# MAGIC     MEASURE(total_quantity) AS total_quantity,
# MAGIC     MEASURE(total_discount) AS total_discount
# MAGIC FROM quicksight_retail.quicksight_retail_semantic.retail_metrics;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     customer_industry,
# MAGIC     MEASURE(transaction_count) AS transaction_count,
# MAGIC     MEASURE(total_revenue) AS total_revenue,
# MAGIC     MEASURE(total_quantity) AS total_quantity
# MAGIC FROM quicksight_retail.quicksight_retail_semantic.retail_metrics
# MAGIC GROUP BY customer_industry;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     product_category,
# MAGIC     MEASURE(total_revenue) AS total_revenue,
# MAGIC     MEASURE(transaction_count) AS transaction_count
# MAGIC FROM quicksight_retail.quicksight_retail_semantic.retail_metrics
# MAGIC
# MAGIC
# MAGIC GROUP BY product_category
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     transaction_date,
# MAGIC     product_category,
# MAGIC     customer_industry,
# MAGIC     MEASURE(transaction_count) AS transaction_count,
# MAGIC     MEASURE(total_revenue) AS total_revenue,
# MAGIC     MEASURE(total_quantity) AS total_quantity
# MAGIC FROM quicksight_retail.quicksight_retail_semantic.retail_metrics
# MAGIC WHERE transaction_date = '2026-03-17'
# MAGIC GROUP BY
# MAGIC     transaction_date,
# MAGIC     product_category,
# MAGIC     customer_industry;