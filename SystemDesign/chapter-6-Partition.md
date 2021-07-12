# Partition

also know as:

*   sharding in MongoDB, Elasticsearch
*   region in HBase
*   tablet in Bigtable
*   node in Cassandra and Riak
*   vBucket in Couchbase

It's scalability-driven

## Replication vs Partition

*   Replication: same data, on several nodes
*   Splitting a big database into smaller subsets called partitions.

## How to do partitions?

*   Partition by Range Key

    *   pro: range scans are easy. 
    *   con: can lead to hot spots. (For example, timestamp based, recently added data are more likely to be read)

*   Partition by Hash key

    *   Pro: uniform distributed

    *   Con: lose the ability to efficient range queries

    *   Cassandra makde a compromise: a table in cassandra can be decalared with a compound primary key consisting of several columns. Only the first part of the key is used for partition, the second part is used for sorting. 

        `primary key = (partition key + sort key)`

        (这样的方法能行得通的前提在于partition-key的order往往是不重要的。比如user_id)