# Replication

## Motivation

*   Keep data geographically close to the user
*   To allow system to continue working if some of them failed
*   Increase read throughput

## Leader based replication

---

### Single leader replication

*   Read via leader and followers, write via leader

### Async vs Sync replication

*   Sync： 
    *   Pro: follower is guaranteed to have an up-to-date copy
    *   Con: have to wait if replication failed.
    *   Because of that, it's common that there's one sync replication, and multiple async replication

### Setting-up new follower

*   Steps:
    *   Take a snapshot of the leader
    *   Copy the snapshot to the new follower
    *   The follower request all data changes that happened since the snapshot

### Follower failure

*   Recover from the logs

### Leader failure:

*   One of the followers needs to be promoted to be the new leader

 * Steps:
    	* Determing the leader has failed
    * Choose a new leader
    	* Reconfigure the system to use the new leader

### Implementation of replication logs

1.   Statement-based replciation: Forward the SQL statements to the followers  
     *   Con: 
         *   nondeterministic function (like NOW())
         *   Non-deterministic side effect
2.   Write-ahead log 
     *   Used in postgreSQL and Oracle
3.   Logical log replication
     *   Specifically designed for replication
4.   Trigger based replication

### Solve the read lag in async replication:

这是一种eventual consistent的system

 * Read our own write: 
    	* Use a timestamp to record the last update, if it's recent, then read from leader
 * Monotonic reads:
    	* 因为async，有可能用户在不同replica上读到不同的信息。
        	* solution: 对于一个用户，只从一个特定的replica读
 * Consistent prefix read:
     * 在多个writer的情况下，因为async，record在不同replica上的顺序不同，改变了causality。

## Multi-leader replication

---

Compared with single-leader replication, multi-leader replication can have multiple servers accepting writes.

*   在同一个data center中，做multi-leader replication是不make sense的，这其中的complexity多过merits
*   Pro:
    *   performance更好
    *   更好的抵御datacenter failure
    *   更好的抵御network failure
*   con：
    *   当多个data center都收到writes的时候，可能有conflict，需要conflict resolution
*   scenarios:
    *   Clients with offline operation: 比如calendar app，你的device其实是一个local leader，需要asyc replicate到服务器端。
    *   Collaborative editting:

### Handling write conflicts

![iShot2021-09-06 21.22.32](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-09-06 21.22.32.png)

*   在single-leader的db里， 这种情况下，第二个writer会被block，但在mult-leader的情况下不会
*   有一种办法是将replication变成sync的
*   另外一种办法是conflict avoidance，即让所有可能产生conflict的write都被同一个leader handle比如
    *   同一个user的write都被同一个ds来处理
*   还有一种情况是建立一种特定的protocol来确定最终状态: converging toward a consistent state，比如
    *   给所有的write一个uuid，选择最高的uuid作为winner，比如last write wins，(会有data loss)
    *   选择被更多replica的wrtie作为最终的 winner， （会有data loss）
    *   以concatenated的result作为最终结果
    *   或者将conflicts记录下来，用application来resolve conflicts at some later time(可以让用户自己决定)
*   Auto conflicting resolving

## Leaderless replication (Dynamo-like)

---

No leader, no failover.

​	leaderless适用于需要对node failure有极高的tolerent, high-availability, low-latency

*   When write, send write request to many replicas.
*   When read, read from multiple replicas, use the up-to-date value

### Achieve "eventual-consistency"

Two mechanisms:

*   Read repair: 如果在读的时候遇到了stale data，就修复
*   Anti-entropy process: 有background process一直在寻找replica之间的不一致。 

### Quorums for read and write

n: number of replicas, w= write quorums, r = read quorum, to guarantee eventual consistency.

$w + r > n$

*   这其中引出了一个corner case：
    *   比如有5个replica，w=r=3
    *   user发起写，4个fail, value = 0, 1个success, value=1, 此时write被abort
    *   user发起读，此时读到三个值，分别为0, 1, 0，因为1的timestamp比较新， 所以作为了truth
    *   这样就造成了in-consistency
*   也就是说因为leaderless的没有roll-back的transactional mechanism，他是实现不了transaction保证的。

*   选择w,r是一种trade-off

    *   如果是write heavy的，我可以使w=1, r=n
    *   如果是read heavy的，可以使w=n， r=1
    *   但是这样会nullify了leaderless replication的意义，并不能作为常规设置。

*   Sloppy Quorums:

    *   还是要求要w个write，r个read，只是可以临时借用别的非-home nodes
    *   当node恢复之后，再将借用的node上的信息copy到home node上，这叫做hinted hand-off
    *   这种方法可以显著的增加write availability

    





