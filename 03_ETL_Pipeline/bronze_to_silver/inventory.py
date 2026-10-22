from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(
    name="quicksight_retail.quicksight_retail_silver.inventory",
    comment="Inventory data with profiled columns and data quality checks"
)
@dp.expect_or_drop(
    "valid_inventory_id",
    "inventory_id IS NOT NULL AND LENGTH(TRIM(inventory_id)) > 0"
)
@dp.expect_or_drop(
    "valid_stock_quantity",
    "stock_quantity IS NOT NULL AND stock_quantity >= 0"
)
@dp.expect_or_drop(
    "valid_product_id",
    "product_id IS NOT NULL AND LENGTH(TRIM(product_id)) > 0"
)
@dp.expect_or_drop(
    "valid_store_id",
    "store_id IS NOT NULL AND LENGTH(TRIM(store_id)) > 0"
)
@dp.expect(
    "valid_reorder_level",
    "reorder_level IS NOT NULL AND reorder_level >= 0"
)
def inventory_clean():
    # Read source streaming table
    source_df = spark.readStream.table("quicksight_retail.neon_postgres_bronze.inventory")
    
    # Select relevant columns with lowercase naming
    return (
        source_df.select(
            F.trim(F.col("inventory_id")).alias("inventory_id"),
            F.trim(F.col("product_id")).alias("product_id"),
            F.trim(F.col("store_id")).alias("store_id"),
            F.col("stock_quantity").cast("int").alias("stock_quantity"),
            F.col("reorder_level").cast("int").alias("reorder_level"),
            F.trim(F.col("warehouse_location")).alias("warehouse_location"),
            F.col("last_stock_update").cast("timestamp").alias("last_stock_update"),
            F.when(
                F.col("stock_quantity").isNull(),
                "UNKNOWN"
            ).when(
                F.col("stock_quantity") == 0,
                "OUT_OF_STOCK"
            ).when(
                F.col("reorder_level").isNull(),
                "UNKNOWN"
            ).when(
                F.col("stock_quantity") < F.col("reorder_level"),
                "LOW_STOCK"
            ).otherwise(
                "HEALTHY"
            ).alias("inventory_status"),
            F.col("__START_AT").alias("start_at"),
            F.col("__END_AT").alias("end_at"),
            F.current_timestamp().alias("processed_at")
        )
    )
