-- Databricks notebook source
-- DBTITLE 1,Create dim_customer gold view
 create or replace view quicksight_retail.quicksight_retail_gold.dim_customer as

 select 
     id as customer_id,
     customer_name,
     type as customer_type,
     billing_city,
     billing_state,
     billing_country,
     phone,
     website,
     industry,
     annual_revenue,
     number_of_employees,
     description

 from quicksight_retail.quicksight_retail_silver.account
 where is_deleted=false and is_active=true;


-- DBTITLE 1,Create dim_product gold view
 create or replace view quicksight_retail.quicksight_retail_gold.dim_product as

 select 
     product_id,
     product_name,
     category,
     subcategory,
     brand,
     product_segment,
     unit_price,
     supplier_name,
     launch_date,
     updated_at

 from quicksight_retail.quicksight_retail_silver.product_catalog
 where is_active=true;


-- DBTITLE 1,Create dim_inventory gold view
 create or replace view quicksight_retail.quicksight_retail_gold.dim_inventory as

 select 
     inventory_id,
     product_id,
     stock_quantity,
     reorder_level,
     inventory_status,
     warehouse_location,
     last_stock_update

 from quicksight_retail.quicksight_retail_silver.inventory;


-- DBTITLE 1,Build dim_calender gold view table
 CREATE OR REPLACE TABLE quicksight_retail.quicksight_retail_gold.dim_calendar AS

 WITH date_range AS (
     SELECT EXPLODE(
         SEQUENCE(
             TO_DATE(:start_date),
             TO_DATE(:end_date),
             INTERVAL 1 DAY
         )
     ) AS date
 )

 SELECT
     date,
     YEAR(date) AS year,
     QUARTER(date) AS quarter,
     MONTH(date) AS month,
     DATE_FORMAT(date, 'MMMM') AS month_name,
     DATE_FORMAT(date, 'MMM') AS month_short_name,
     WEEKOFYEAR(date) AS week_of_year,
     DAYOFMONTH(date) AS day_of_month,
     DAYOFWEEK(date) AS day_of_week,
     DATE_FORMAT(date, 'EEEE') AS day_of_week_name,
     DATE_FORMAT(date, 'EEE') AS day_of_week_short_name,
     DAYOFYEAR(date) AS day_of_year,

     CASE
         WHEN DAYOFWEEK(date) IN (1, 7) THEN TRUE
         ELSE FALSE
     END AS is_weekend,

     CASE
         WHEN DAYOFWEEK(date) NOT IN (1, 7) THEN TRUE
         ELSE FALSE
     END AS is_weekday,

     CONCAT(YEAR(date), '-Q', QUARTER(date)) AS year_quarter,
     DATE_FORMAT(date, 'yyyy-MM') AS year_month,
     LAST_DAY(date) AS last_day_of_month,
     date = LAST_DAY(date) AS is_last_day_of_month,
     date = DATE_TRUNC('MONTH', date) AS is_first_day_of_month

 FROM date_range
 ORDER BY date;
