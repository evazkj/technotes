# Data retrieval

## Database:

	* Naive database: Append log
	* Improved: add Index

## SSTables and LSM-Trees

*   *Sorted String Table*, or *SSTable*
*   *Log-Structured Merge-Tree* (or LSM-Tree)
*   We can now make our storage engine work as follows:
    -   When a write comes in, add it to an in-memory balanced tree data structure (for example, a red-black tree). This in-memory tree is sometimes called a *memtable*.
    -   When the memtable gets bigger than some threshold—typically a few megabytes—write it out to disk as an SSTable file. This can be done efficiently because the tree already maintains the key-value pairs sorted by key. The new SSTable file becomes the most recent segment of the database. While the SSTable is being written out to disk, writes can continue to a new memtable instance.
    -   In order to serve a read request, first try to find the key in the memtable, then in the most recent on-disk segment, then in the next-older segment, etc.
    -   From time to time, run a merging and compaction process in the background to combine segment files and to discard overwritten or deleted values.
*   Other optimization:
    *   Bloom filter
    *   size-tiered and level compaction
*   B-tree
    *   ![](/Users/khang306/Documents/technotes/SystemDesign/images/ddia_0306.png)

*   Comparison
    *   LSM-trees are typically faster for writes(because it's sequential write), whereas B-trees are thought to be faster for reads 
    *   For LSM-tree, it's tiered storage, frequently updated records can be looked-up faster
    *   LSM-tree compressed better, less fragmentation
    *   LSM-tree has Lower write amplification, A B-tree index must write every piece of data at least twice: once to the write-ahead log, and onceto the tree page itself 
    *    the compaction process can sometimes interfere with the performance of ongoing reads and writes. less predictable than B-tree
    *   for LSM-tree, it existed in several places, add complexity to transaction isolation.

| Property             | Transaction processing systems (OLTP)             | Analytic systems (OLAP)                   |
| :------------------- | :------------------------------------------------ | :---------------------------------------- |
| Main read pattern    | Small number of records per query, fetched by key | Aggregate over large number of records    |
| Main write pattern   | Random-access, low-latency writes from user input | Bulk import (ETL) or event stream         |
| Primarily used by    | End user/customer, via web application            | Internal analyst, for decision support    |
| What data represents | Latest state of data (current point in time)      | History of events that happened over time |
| Dataset size         | Gigabytes to terabytes                            | Terabytes to petabytes                    |

