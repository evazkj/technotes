# Design KV store

 Problem: Design a key value data storage support the following
API: 

*   Support write(K, V) and read(K, V), and delete(K)
*   Support composite primary key as ((Partition Key), key). The partition key will decide where to shard the data

