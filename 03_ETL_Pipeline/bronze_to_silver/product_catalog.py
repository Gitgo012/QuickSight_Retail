from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(
    name="quicksight_retail.quicksight_retail_silver.product_catalog",
    comment="Silver layer product catalog with standardised data and DQ rules",
)
# Rows failing these rules are dropped
@dp.expect_or_drop("valid_product_id", "product_id IS NOT NULL AND length(trim(product_id)) > 0")
@dp.expect_or_drop("valid_product_name", "product_name IS NOT NULL AND length(trim(product_name)) > 0")
@dp.expect_or_drop("valid_category", "category IS NOT NULL AND length(trim(category)) > 0")
@dp.expect_or_drop("valid_price", "unit_price > 0")
@dp.expect_or_drop("valid_launch_date", "launch_date IS NOT NULL")
# Failing rows are kept, but the violation is recorded in the metrics
@dp.expect("valid_supplier", "supplier_name IS NOT NULL")
def product_catalog():
    source_df = spark.read.table("quicksight_retail.neon_postgres_bronze.product_catalog")

    return source_df.select(
        F.upper(F.trim(F.col("product_id"))).alias("product_id"),
        F.initcap(F.trim(F.col("product_name"))).alias("product_name"),
        F.initcap(F.trim(F.col("category"))).alias("category"),
        F.coalesce(F.initcap(F.trim(F.col("subcategory"))), F.lit("Unknown")).alias("subcategory"),
        F.coalesce(F.initcap(F.trim(F.col("brand"))), F.lit("Unknown")).alias("brand"),
        F.round(F.col("unit_price"), 2).alias("unit_price"),
        F.initcap(F.trim(F.col("supplier_name"))).alias("supplier_name"),
        F.col("launch_date"),
        F.when(F.col("unit_price") > 50000, "PREMIUM")
         .when(F.col("unit_price") > 10000, "MID_RANGE")
         .otherwise("BUDGET")
         .alias("product_segment"),
        # CDC tracking columns
        F.col("__START_AT").alias("start_at"),
        F.col("__END_AT").alias("end_at"),
        F.col("__END_AT").isNull().alias("is_active"),
        F.col("updated_at"),
        F.current_timestamp().alias("processed_at"),
    )