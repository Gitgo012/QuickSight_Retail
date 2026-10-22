# Databricks notebook source
# MAGIC %md
# MAGIC This notebook ingests **Transaction_source.csv** from our Blob Storage and ingests it using Databricks Autoloader
# MAGIC

# COMMAND ----------

# DBTITLE 1,Load CSV files with Autoloader and write as delta table
filepath="/Volumes/quicksight_retail/volume/blob_storage/transaction_source/"
checkpoint_location="/Volumes/quicksight_retail/volume/blob_storage/_checkpoint"
schema_location="/Volumes/quicksight_retail/volume/blob_storage/_schema"

#read the data from source using autoloader and save to df
df=spark.readStream.format("cloudfiles").\
    option("cloudFiles.format","csv").\
    option("header","true").\
    option("inferSchema","true").\
    option("cloudFiles.schemaEvolutionMode", "addNewColumns").\
    option("cloudfiles.schemaLocation",schema_location).\
    load(filepath)

#write the data from df to delta table and read until the end of stream
try:
    stream=(df.writeStream.format("delta").\
        option("checkpointLocation",checkpoint_location).\
        option("mergeSchema","true").\
        trigger(availableNow=True).\
        toTable("quicksight_retail.blob_storage.transaction_source")
    )
    #wait for the batch to terminate
    stream.awaitTermination()
    print(f"Data ingestion successfully done to target location")
except Exception as e:
    print(f"Data ingestion failed with exception {e}")



# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from quicksight_retail.blob_storage.transaction_source;