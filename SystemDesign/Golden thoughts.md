# Golden thoughts

*   When you see something like "monitoring dashboard", think of using Kafka+Flink (Do not use logs to monitor, because logs aggregation usually allow loss of logs)
    *   Kafka provide durability(replication)
    *   Flink provides rolling window on Kafka