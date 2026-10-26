class JobParameters:
    template = "gold_aggregate"

    source_table = "silver.orders"
    sink_table = "gold.orders_by_store"

    group_by = ["StoreID", "Status"]
    sum_column = "Amount"
