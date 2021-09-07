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
    
*   Key Skew/ hot spot

    *   比如在twitter里，有一个名人发了一条微博，这条微博会被读很多次。造成hotspot，一个解决方法就是在key后加一个数字，然后让这个key被distributed。overhead就是write会大大增加。

 ## Secondary Index

*   Local secondary index
    *   Each partition maintains its own secondary index
    *   Read requires more effort, scatter&gather
*   Global secondary index
    *   Reads more efficiently, writes are more complicated
    *   In practice, updates to global secondary indexes are often asynchronous, dynamoDB usually update index within a fragment of seconds

## Rebalance partitions

*   Reblancing minimum requirements:

    *   After rebalancing, the load should be shared fairly between the nodes in the clsuter
    *   During rebalancing, the database should continue accepting reads and writes
    *   No more data than necessary should be moved between nodes.

*   Strategies:

    *   Not to do it: hash mod N
        *   When N changes, most of the data will need to be moved
    *   Fixed number of partitions 
        *   For example: 1000 partitions, 10 nodes, we move partitions entirely

    *   Dynamic partition:
        *   Suitable for key-range partition
        *   When a partition grows to exceed a configured side, it will be split into two partitions
        *   If it shrinks to a certain size, it will be merged

*   Auto/manual rebalancing

## Request routing

*   three ways:
    *   Contact any nodes, if not on that node, relay to others
    *   Add routing layer
    *   Client needs to know the assignments
*   ZooKeeper comes into play
*   