class JobParameters:
    template = "silver_batch"

    source_table = "bronze.orders_raw"
    sink_table = "silver.orders"

    key_column = "OrderId"
    time_column = "UpdatedAtUtc"
    sorting_order = "DESC"




